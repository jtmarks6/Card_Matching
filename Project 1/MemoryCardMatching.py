###############################
# Name: Jeremy Marks          #
# Purpose: bot to match cards #
###############################
import mss, keyboard, time, sys, pyautogui, pytesseract, cv2, datetime, os
from PIL import ImageGrab, ImageOps, ImageChops, ImageColor, Image
from numpy import *

#variables for image recognition thresholds:
addition = 84
blackThresh = 50 #changes as matches are missed, moves threshold down until all cards are matched
majorityBlack = 4000
blankTopThresh= 600
blankBottomThresh = 300
clearPicThreshHold = 35

currentDirectory = os.getcwd()
if not os.path.exists(currentDirectory + '\Cards'): os.makedirs(currentDirectory + '\Cards')
cardPicturePath = currentDirectory + "\Cards\card{}_{}.png"
cardFolderPath = currentDirectory + "\Cards\{}"
round = 1 #keeps track of which round of the game is running
delay = 0 #delay between clicking and moving mouse, used for debugging to actually see mouse movement
highScore = True #true if should stop when reaches scoreGoal
scoreGoal = 158940 #target score to stop at

#class to refer to for getting coordinates of where to take pictures from for a 1920x1080 screen
class coordinates():
    #pixel coordinates for the y positions of each row
    rows = (
        (300, 370), 
        (383, 453), 
        (467, 537), 
        (551, 621), 
        (635, 705), 
        (719, 789))

    #pixel coordinates for the x positions of each column
    columns = (
        (742, 816),
        (826, 900),
        (910, 984),
        (994, 1068),
        (1078, 1152),
        (1161, 1235),
        (1245, 1319))

    #pixel coordinates for the top corn of each row used for testing if the card is flipped over or not
    cardCheckBoxes = (
        (993, 292, 994, 293),
        (993, 376, 994, 377),
        (993, 460, 994, 461),
        (993, 544, 994, 545),
        (993, 628, 994, 629),
        (993, 712, 994, 713))

    #pixel coordinates for the y value to check if a card is in location or not
    blankRows = (292, 376, 460, 544, 628, 712)
    #pixel coordinates for the x value to check if a card is in location or not
    blankColumns = (765, 846, 933, 1017, 1101, 1185, 1269)

    #pixel coordinates for y of where to click the card for matches
    middleRows = (334, 418, 502, 586, 670, 754)
    #pixel coordinates for x of where to click the card for matches
    middleColumns = (779, 863, 947, 1031, 1115, 1199, 1283)

    #List to keep track of where cards are, also I know would be more effiecient to loop to set all these to false
    #But initializing like this helped me visualize during debugging where the cards actually were
    currentCards = [
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False]]
    
    #List to keep track of which rows are left to take pictures of
    rowsLeft = [False, False, False, False, False, False, False]

################################################################################
#main function of program, prints the high score goal and starts the first round
def main():
    if highScore: print("Goal Score:",scoreGoal)
    startNewRound()
    run = True
################################################################################

#checks whether user has pressed p to pause or q to quit
def checkQuitPause():
    if keyboard.is_pressed('q'): sys.exit("Quit")
    if keyboard.is_pressed('p'): pause()

#matches the picture of the cards by looping through available cards and calling checkMatch function
def matchCards():
    #records start time
    startTime = datetime.datetime.now()
    #loops through each card position as first card in match comparison
    for r in range(6):
        for c in range(7):
            #checks if card is in position
            if coordinates.currentCards[r][c]:
                #loops through each card position as second card in match comparison
                for y in range(6):
                    for x in range(7):
                        checkQuitPause()
                        #checks if card is in position
                        if coordinates.currentCards[y][x]:
                            #checks if is trying to match current card
                            if not(y == r and x == c):
                                if checkMatch(cardPicturePath.format(r,c), cardPicturePath.format(y,x)):
                                    #clicks the 2 cards if matched
                                    pyautogui.click(coordinates.middleColumns[c],coordinates.middleRows[r])
                                    time.sleep(delay)
                                    pyautogui.click(coordinates.middleColumns[x],coordinates.middleRows[y])
                                    time.sleep(delay)
                                    #marks the cards as matched
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
    #waits for new round to load
    while count < 50000:
        count +=1
        checkQuitPause()
    startNewRound()

#While loop to run until user unpauses the program or quits
def pause():
    print("Paused")
    time.sleep(1)
    while True:
        if keyboard.is_pressed('q'): sys.exit("Quit")
        if keyboard.is_pressed('p'):
            print("Resumed")
            time.sleep(1)
            break

#checks if any cards are left as false which means unmatched cards
def checkCardsLeft():
    for r in range(6):
        for c in range(7):
            if coordinates.currentCards[r][c]: return True
    print("Matched All cards")
    return False

#checks if any rows left to take pictures of
def checkRowsLeft():
    for r in range(7):
        if coordinates.rowsLeft[r]: return True 
    return False

#function to click to cards that most likely don't match to get a match wrong on purpose for anti cheat purposes
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
    #debounce variables to only print status once at start of while loops
    matchDebounce = True
    checkRowsDebounce = True
    #runs until all cards are matched
    while checkCardsLeft():
        #runs until all rows have successfully had a picture taken of flipped cards
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
        matchCards() #matches cards once all rows have had pictures taken
        checkQuitPause()
    endRound()

#combines the x and y coordinates from the class together and returns the pixel box coordinates
def getMiddleOfBox(row, column):
    x1 = coordinates.middleColumns[column]
    x2 = x1 + 1
    y1 = coordinates.middleRows[row]
    y2 = y1 + 1
    box = (x1, y1, x2, y2)
    return box

#combines the x and y coordinates from the class together and returns the pixel box coordinates
def getCorner(row, column):
    x1 = coordinates.blankColumns[column]
    x2 = x1 + 1
    y1 = coordinates.blankRows[row]
    y2 = y1 + 1
    box = (x1, y1, x2, y2)
    return box

#combines the x and y coordinates from the class together and returns the pixel box coordinates
def getBox(row, column):
    x1 = coordinates.columns[column][0]
    x2 = coordinates.columns[column][1]
    y1 = coordinates.rows[row][0]
    y2 = coordinates.rows[row][1]
    box = (x1, y1, x2, y2)
    return box

#checks if target score has been reached
def checkScore():
    picScore()
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    image = cv2.imread(cardFolderPath.format("score.png"))

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Preprocessing
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    score = pytesseract.image_to_string(threshold_img, config = r'--oem 3 --psm 6') #converts processed picture to string
    
    #exits if current score is more than target score
    if int(score) > scoreGoal:
        print("Reached Goal Score:", score)
        sys.exit("TargetGoal")

#loops through card positions and checks with card is in position and sets list with all current cards
def checkBlankCards():
    for r in range(6):
        for c in range(7):
            if blankTopThresh > getSumOf(getCorner(r,c)) > blankBottomThresh:
                coordinates.currentCards[r][c] = False
            else:
                coordinates.currentCards[r][c] = True
                coordinates.rowsLeft[r] = True

#checks if 2 input cards match
def checkMatch(pic1, pic2):
    #opens both images
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)
    #creates an image that represents the difference between the images
    image = ImageChops.difference(image1, image2)
    #image.save( 'Documents\Programming\Python\Wizard101\Cards\yoink.png', 'png')   #for debugging, shows the result picture of difference

    #analyze pizels of resultant image to see how alike the 2 cards were
    pixels = image.getdata()
    blackPixels = 0 
    for pixel in pixels:
        if pixel[0] < blackThresh: blackPixels += 1
    if(blackPixels > majorityBlack): return True
    else: return False

#checks all rows to see if card is currently flipped over and if so takes picture of the row
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

#takes picture of all cards in row that exist
def takeRowPics(row):
    coordinates.rowsLeft[row] = False
    for c in range(7):
        if coordinates.currentCards[row][c]: mssCapture(getBox(row, c), row, c)

#adds pixels together into sum to compare
#I found comparing with sums is significantly faster than comparing actual full pictures and with this project at least was still accurate
def getSumOf(captureArea):
    with mss.mss() as sct:
        image = sct.grab(captureArea)
        pixels = image.pixels
        pix = array(pixels)
        sum = pix.sum()
        return sum

#Uses Mss to capture screenshot of certain size, I found Mss to be the fastest python method for screenshots
def mssCapture(captureArea, row, column):
    with mss.mss() as sct:
        image = sct.grab(captureArea)
        picName = cardPicturePath.format(row, column)
        mss.tools.to_png(image.rgb, image.size, output=picName)
        return image

#takes picture of the score
def picScore():
    with mss.mss() as sct:
        image = sct.grab((840, 858, 1000, 900))
        picName = cardFolderPath.format("score.png")
        mss.tools.to_png(image.rgb, image.size, output=picName)

main()