/******************************
*Jeremy Marks                 *
*Class: -- Spring 21          *
*UserName: -------            *
*Instructor: ---------------- *
******************************/
#include "functions.h"

//array of days of month for checking if day is in correct range for the month
int days[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
//array of month strings for printing the month
const char* monthString[] = {" ", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
//enum of months to help convert month int into string for printing
enum month{January, February, March, April, May, June, July, August, September, October, November, December};

//adds new node to linked list
void add(node_t** node, node_t** head){
    //makes new node head if list is empty
    if(*head == NULL){
        *head = *node;
    } else{
        struct node_t * iterateNode = *head;
        //iterates to end of list to add new node
        while(iterateNode->next != NULL){
            iterateNode = iterateNode->next;
        }
        iterateNode->next = *node;
    }
}

//reads in a record of the input file and returns a new node with read values
node_t* readNodeInfo(FILE* input){
    //variables to hold read in record values
    char line[90];
    char firstName[15];
    char lastName[15];
    char strday[3];
    char strmonth[3];
    char stryear[5];
    char favSong[50];
    //sets new node to NULL if end of file and returns
    if(fscanf(input, "%[^\n]\n", line) != 1){
        struct node_t* newNode = NULL;
        return  newNode;
    }
    //reads in all values from line
    sscanf(line, "%[^,],%[^,],%[^,],%[^,],%[^,],%[^,]", lastName, firstName,strmonth, strday, stryear, favSong);
    //converts the number data from string to int
    int day = atoi(strday);
    int month = atoi(strmonth);
    int year = atoi(stryear);
    //allocates new node to be added to list
    struct node_t* newNode = (struct node_t*) malloc(sizeof(struct node_t));
    //allocates bday_t for the new node
    newNode->bday = (struct bday_t*) malloc(sizeof(struct bday_t));
    //put values into new node
    strcpy(newNode->firstName, firstName);
    strcpy(newNode->lastName, lastName);
    strcpy(newNode->favSong, favSong);
    newNode->bday->day = day;
    newNode->bday->month = month;
    newNode->bday->year = year;
    newNode->next = NULL;
    //returns new node
    return newNode;
}

//creates linked list from input file
node_t* createList(FILE* file, node_t** head){
    node_t * nodeptr;
    //gets new node from readNodeInfo for each line in file
    //if new node is not null checks date and adds to list if valid bday
    while(nodeptr = readNodeInfo(file), nodeptr != NULL){
        //checks birthday validity 
        if(checkDate(*nodeptr->bday)){
            add(&nodeptr, head);
        }
    }
    //closes input file
    fclose(file);
    return *head;
}

//prints all values for each node in linked list
void PrintList(FILE* outFile, node_t* head){
    //if list is empty prints to sterr, closes ouput file, and exits program
    if(head == NULL){
        printf("List is empty\n");
        fclose(outFile);
        exit(0);
    }
    printBorder(outFile);
    fputs("\nLIST INFO:\n", outFile);
    struct node_t * iterateNode = head;
    //loops through all nodes in linked list
    while(iterateNode != NULL){
        //enum of month to convert int month to string month
        enum month monthEnum = iterateNode->bday->month;
        fprintf(outFile, "%s, %s, %s %i, %i, %s\n",iterateNode->lastName, iterateNode->firstName, monthString[monthEnum], iterateNode->bday->day, iterateNode->bday->year, iterateNode->favSong);
        iterateNode = iterateNode->next;
    }
    printBorder(outFile);
}

//prints the first and last name for each node in list
void PrintName(FILE* outFile, node_t* head){
    //if list is empty prints to sterr, closes ouput file, and exits program
    if(head == NULL){
        printf("List is empty\n");
        fclose(outFile);
        exit(0);
    }
    printBorder(outFile);
    fputs("\nNAMES:\n", outFile);
    struct node_t * iterateNode = head;
    //loops through all nodes in linked list
    while(iterateNode != NULL){
        fprintf(outFile, "%s, %s\n",iterateNode->lastName, iterateNode->firstName);
        iterateNode = iterateNode->next;
    }
    printBorder(outFile);
}

//prints birthday and names for each node in list
void PrintBDay(FILE* outFile, node_t* head){
    //if list is empty prints to sterr, closes ouput file, and exits program
    if(head == NULL){
        printf("List is empty\n");
        fclose(outFile);
        exit(0);
    }
    printBorder(outFile);
    fputs("\nBIRTHDAY:\n", outFile);
    struct node_t * iterateNode = head;
    //loops through all nodes in linked list
    while(iterateNode != NULL){
        enum month monthEnum = iterateNode->bday->month;
        fprintf(outFile, "%s %s's date of birth is %s %i, %i\n",iterateNode->firstName, iterateNode->lastName, monthString[monthEnum], iterateNode->bday->day, iterateNode->bday->year);
        iterateNode = iterateNode->next;
    }
    printBorder(outFile);
}

//prints name and favorite song for each node in list
void Song(FILE* outFile, node_t* head){
    //if list is empty prints to sterr, closes ouput file, and exits program
    if(head == NULL){
        printf("List is empty\n");
        fclose(outFile);
        exit(0);
    }
    printBorder(outFile);
    fputs("\nSONG:\n", outFile);
    struct node_t * iterateNode = head;
    //loops through all nodes in linked list
    while(iterateNode != NULL){
        fprintf(outFile, "%s %s's favorite song is %s\n",iterateNode->firstName, iterateNode->lastName, iterateNode->favSong);
        iterateNode = iterateNode->next;
    }
    printBorder(outFile);
}

//prints line of 80 *
void printBorder(FILE* outFile){
    for(int i=0; i<80; i++){
        fputc('*', outFile);
    }
}

//uses function pointer to call a print function
void print(void(*fp)(FILE*, node_t*), FILE* outFile, node_t* head){
    (*fp)(outFile, head);
}

//checks if correct number of command line arguments
void checkArgs(int numArgs){
    if(numArgs != 3){
        printf("Incorrect number of command line arguments\n");
        exit(0);
    }
}

//checks if file opened successfully, prints error and exits if not
void checkFile(FILE* file, char* fileName){
    if(file == NULL){
        printf("%s %s", "Failed to open", fileName);
        exit(0);
    }
}

//returns memory for linked list by freeing each node
void deleteList(node_t** head){
    struct node_t * iterateNode = *head;
    //loops through each node in list
    while(iterateNode != NULL){
        iterateNode = iterateNode->next;
        free(*head);
        *head = iterateNode;
    }
}

//checks if birthday values are in correct range
bool checkDate(bday_t bday){
    //checks leap year
    if(bday.month == 2 && bday.day == 29 && isLeapYear(bday.year)){
        return true;
    }
    //checks the month validity
    if(!(bday.month <= 12 && bday.month > 0)){
        printf("Month is not a valid date\n");
        return false;
    }
    //checks the day validity
    if(!(bday.day <= days[bday.month] && bday.day > 0)){
        printf("Day is not a valid date\n");
        return false;
    }
    //checks the year validity
    if(!(bday.year <= 2020  && bday.year >= 1900)){
        printf("Year is not a valid date\n");
        return false;
    }
    return true;
}

//checks if year is a leap year
bool isLeapYear(int year){
    if(year%4 == 0 && year%100 == 0 && year%400 == 0){
        return true;
    } else if(year%4 == 0 && year%100 != 0){
        return true;
    } else{
        return false;
    }
}
