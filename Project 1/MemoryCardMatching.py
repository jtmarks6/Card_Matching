import mss, keyboard, time, sys, pyautogui, pytesseract, cv2, datetime
from PIL import ImageGrab, ImageOps, ImageChops, ImageColor, Image
from numpy import *

#variables for image recognition thresholds:
addition = 84
blackThresh = 50
majorityBlack = 4000
delay = 0
round = 1
blankTopThresh= 600
blankBottomThresh = 300
clearPicThreshHold = 35

highScore = True #true if should stop when reaches scoreGoal
scoreGoal = 158940

#class to refer to for getting coordinates of where to take pictures from
class coordinates():
    rows = (
        (300, 370), 
        (383, 453), 
        (467, 537), 
        (551, 621), 
        (635, 705), 
        (719, 789))

    columns = (
        (742, 816),
        (826, 900),
        (910, 984),
        (994, 1068),
        (1078, 1152),
        (1161, 1235),
        (1245, 1319))

    cardCheckBoxes = (
        (993, 292, 994, 293),
        (993, 376, 994, 377),
        (993, 460, 994, 461),
        (993, 544, 994, 545),
        (993, 628, 994, 629),
        (993, 712, 994, 713))

    blankRows = (292, 376, 460, 544, 628, 712)
    blankColumns = (765, 846, 933, 1017, 1101, 1185, 1269)

    middleRows = (334, 418, 502, 586, 670, 754)
    middleColumns = (779, 863, 947, 1031, 1115, 1199, 1283)

    #Array to keep track of where cards are, also I know would be more effiecient to loop to set all these to false
    #But initializing like this helped me visualize during debugging where the cards actually were
    currentCards = [
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False]]
    
    rowsLeft = [False, False, False, False, False, False, False]

#main function of program, prints the high score goal and starts the first round
def main():
    if highScore:
        print("Goal Score:",scoreGoal)
    startNewRound()
    run = True

#checks whether user has pressed p to pause or q to quit
def checkQuitPause():
    if keyboard.is_pressed('q'):
        sys.exit("Quit")
    if keyboard.is_pressed('p'):
        pause()

#matches the picture of the cards by looping through available cards and calling checkMatch function
def matchCards():
    #records start time
    startTime = datetime.datetime.now()
    for r in range(6):
        for c in range(7):
            #checks if card is in position
            if coordinates.currentCards[r][c]:
                for y in range(6):
                    for x in range(7):
                        checkQuitPause()
                        #checks if card is in position
                        if coordinates.currentCards[y][x]:
                            #checks if is trying to match current card
                            if not(y == r and x == c):
                                if checkMatch("Documents\Programming\Python\Wizard101\Cards\card" + str(r) + "_" + str(c) + ".png", "Documents\Programming\Python\Wizard101\Cards\card" + str(y) + "_" + str(x) + ".png"):
                                    #clicks the 2 cards if matched
                                    pyautogui.click(coordinates.middleColumns[c],coordinates.middleRows[r])
                                    time.sleep(delay)
                                    pyautogui.click(coordinates.middleColumns[x],coordinates.middleRows[y])
                                    time.sleep(delay)
                                    coordinates.currentCards[r][c] = False
                                    coordinates.currentCards[y][x] = False
    #prints difference between start time; I used this to help optimize how fast matches were being calculated
    print("Matching Took:", datetime.datetime.now()-startTime)

#at end of round, resets the rows left to check array and checks if high score goal has been met
def endRound():
    print("Round Ended")
    for c in range(7):
        coordinates.rowsLeft[c] = False
    count = 0
    checkScore()
    while count < 50000:
        count +=1
        checkQuitPause()
    startNewRound()

#
def pause():
    print("Paused")
    time.sleep(1)
    while True:
        if keyboard.is_pressed('q'):
            sys.exit("Quit")
        if keyboard.is_pressed('p'):
            print("Resumed")
            time.sleep(1)
            break

def checkCardsLeft():
    for r in range(6):
        for c in range(7):
            if coordinates.currentCards[r][c]:
                return True
    print("Matched All cards")
    return False

def checkRowsLeft():
    for r in range(7):
        if coordinates.rowsLeft[r]:
            return True 
    return False

def clickRandom():
    pyautogui.moveTo(coordinates.middleColumns[4],coordinates.middleRows[3])
    time.sleep(delay)
    pyautogui.click()
    time.sleep(delay)
    pyautogui.moveTo(coordinates.middleColumns[3],coordinates.middleRows[3])
    time.sleep(delay)
    pyautogui.click()

def startNewRound():
    global round
    print("\nStarting Round ", round)
    round += 1
    blackThresh = 2250
    checkBlankCards()
    counter = 0
    matchDebounce = True
    checkRowsDebounce = True
    while checkCardsLeft():
        while checkRowsLeft():
            if checkRowsDebounce:
                print("Taking Pictures")
                checkRowsDebounce = False
            checkQuitPause()
            checkRows()
        if matchDebounce:
            if not highScore:
                clickRandom()
            print("Matching")
            matchDebounce = False
        counter += 1
        matchCards()
        checkQuitPause()
    endRound()

def getMiddleOfBox(row, column):
    x1 = coordinates.middleColumns[column]
    x2 = x1 + 1
    y1 = coordinates.middleRows[row]
    y2 = y1 + 1
    box = (x1, y1, x2, y2)

    return box

def getCorner(row, column):
    x1 = coordinates.blankColumns[column]
    x2 = x1 + 1
    y1 = coordinates.blankRows[row]
    y2 = y1 + 1
    box = (x1, y1, x2, y2)

    return box

def getBox(row, column):
    x1 = coordinates.columns[column][0]
    x2 = coordinates.columns[column][1]
    y1 = coordinates.rows[row][0]
    y2 = coordinates.rows[row][1]
    box = (x1, y1, x2, y2)

    return box

def checkScore():
    picScore()
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    image = cv2.imread("Documents\Programming\Python\Wizard101\Cards\score.png")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Preprocessing
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    score = pytesseract.image_to_string(threshold_img, config = r'--oem 3 --psm 6')
    
    if int(score) > scoreGoal:
        print("Reached Goal Score:", score)
        sys.exit("Yoinkkkk")

def checkBlankCards():
    for r in range(6):
        for c in range(7):
            if blankTopThresh > getSumOf(getCorner(r,c)) > blankBottomThresh:
                coordinates.currentCards[r][c] = False
            else:
                coordinates.currentCards[r][c] = True
                coordinates.rowsLeft[r] = True

def checkBlanks():
    for r in range(6):
        for c in range(7):
            if blankTopThresh > getSumOf(getCorner(r,c)) > blankBottomThresh:
                coordinates.currentCards[r][c] = False
            else:
                coordinates.currentCards[r][c] = True

def checkMatch(pic1, pic2):
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)
    image = ImageChops.difference(image1, image2)
    #for debugging, shows the result picture of difference
    #image.save( 'Documents\Programming\Python\Wizard101\Cards\yoink.png', 'png') 
    pixels = image.getdata()
    blackPixels = 0 
    for pixel in pixels:
        if pixel[0] < blackThresh:
            blackPixels += 1
    if(blackPixels > majorityBlack):
        return True
    else:
        return False

def checkRows():
    if coordinates.rowsLeft[0] and getSumOf(coordinates.cardCheckBoxes[0]) < clearPicThreshHold:
        takeRowPics(0)
        coordinates.rowsLeft[0] = False
    elif coordinates.rowsLeft[1] and getSumOf(coordinates.cardCheckBoxes[1]) < clearPicThreshHold:
        takeRowPics(1)
        coordinates.rowsLeft[1] = False
    elif coordinates.rowsLeft[2] and getSumOf(coordinates.cardCheckBoxes[2]) < clearPicThreshHold:
        takeRowPics(2)
        coordinates.rowsLeft[2] = False
    elif coordinates.rowsLeft[3] and getSumOf(coordinates.cardCheckBoxes[3]) < clearPicThreshHold:
        takeRowPics(3)
        coordinates.rowsLeft[3] = False
    elif coordinates.rowsLeft[4] and getSumOf(coordinates.cardCheckBoxes[4]) < clearPicThreshHold:
        takeRowPics(4)
        coordinates.rowsLeft[4] = False
    elif coordinates.rowsLeft[5] and getSumOf(coordinates.cardCheckBoxes[5]) < clearPicThreshHold:
        takeRowPics(5)
        coordinates.rowsLeft[5] = False

def takeRowPics(row):
    coordinates.rowsLeft[row] = False
    for c in range(7):
        mssCapture(getBox(row, c), row, c)


def getSumOf(captureArea):
    with mss.mss() as sct:
        image = sct.grab(captureArea)
        pixels = image.pixels
        pix = array(pixels)
        sum = pix.sum()
        return sum

def mssCapture(captureArea, row, column):
    with mss.mss() as sct:
        image = sct.grab(captureArea)
        picName = "Documents\Programming\Python\Wizard101\Cards\card" + str(row) + "_" + str(column) + ".png"
        mss.tools.to_png(image.rgb, image.size, output=picName)
        return image

def picScore():
    with mss.mss() as sct:
        image = sct.grab((840, 858, 1000, 900))
        picName = "Documents\Programming\Python\Wizard101\Cards\score.png"
        mss.tools.to_png(image.rgb, image.size, output=picName)

def getMousePosition():
    return mouse.position

main()