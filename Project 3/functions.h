/******************************
*Jeremy Marks                 *
*CPSC 2310 Spring 21          *
*UserName: jtmarks            *
*Instructor: Dr. Yvon Feaster *
******************************/
#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

//struct for birthday values
typedef struct bday_t{
    int day;
    int month;
    int year;
} bday_t;

//struct for node in linked list
typedef struct node_t{
    char firstName[15];
    char lastName[15];
    char favSong[50];
    struct bday_t* bday;
    struct node_t* next;
} node_t;

/* Parameters: node - node_t double pointer to the new nodes to be added to the
 * list
 * head - node_t double pointer to the first node in the linked list
 * Return: void
 * Description: The function starts at the head node and iterates to the end of 
 * the list and adds the new node
 */
void add(node_t** node, node_t** head);
/* Parameters: input - file pointer that points to the opened input file
 * Return: node_t* - returns a pointer to the new node allocated and filled out 
 * node to be added to the list
 * Description: This function reads in a line/record from the input file and 
 * allocates a new node and fills in the node values with the read record 
 * values and then returns to the new node to be added to the linked list
 */
node_t* readNodeInfo(FILE* input);
/* Parameters: FILE* - file pointer that points to the opened input file
 * node_t** - node_t double pointer to the head of the linked list
 * Return: node_t* - returns a pointer to the head of the linked list
 * Description: This function calls readNodeInfo to read each line of the input 
 * file and then checks the birthday with checkDate and if it is a valid date 
 * it adds the new node from readNodeInfo to the linked list
 */
node_t* createList(FILE*, node_t**);
/* Parameters: FILE* - file pointer that points to the opened input file
 * node_t* - node_t pointer to the head of the linked list
 * Return: void
 * Description: This function starts at the head of the list and iterates 
 * through and prints the info for each node in the linked list to the output 
 * file. It prints the values in the following format:
 * last name, first name, birthday ((string month) day, year), favorite song
 */
void PrintList(FILE*, node_t*);
/* Parameters: FILE* - file pointer that points to the opened output file
 * node_t* - node_t pointer to the head of the linked list
 * Return: void
 * Description: This function starts at the head of the list and iterates 
 * through and prints the names for each node in the linked list to the output 
 * file. It prints the values in the following format:
 * last name, first name
 */
void PrintName(FILE*, node_t*);
/* Parameters: FILE* - file pointer that points to the opened output file
 * node_t* - node_t pointer to the head of the linked list
 * Return: void
 * Description: This function starts at the head of the list and iterates 
 * through and prints the birthday values for each node in the linked list to 
 * the output 
 * file. It prints the values in the following format:
 * first name last name's date of birth is (string month) day, year
 */
void PrintBDay(FILE*, node_t*);
/* Parameters: FILE* - file pointer that points to the opened output file
 * node_t* - node_t pointer to the head of the linked list
 * Return: void
 * Description: This function starts at the head of the list and iterates 
 * through and prints the favorite song for each node in the linked list to the 
 * output 
 * file. It prints the values in the following format:
 * first name last name's favorite song is favorite song
 */
void Song(FILE*, node_t*);
/* Parameters: FILE* - file pointer that points to the opened ouput file
 * Return: void
 * Description: This function prints a line of 80 *
 */
void printBorder(FILE*);
/* Parameters: void(*fp)(FILE*, node_t*) - function pointer to any of the print 
 * functions
 * FILE* - file pointer that points to the opened ouput file
 * node_t* - node_t pointer to the head of the linked list
 * Return: void
 * Description: This function uses a function pointer to call the input print 
 * function
 */
void print(void(*fp)(FILE*, node_t*), FILE*, node_t*);
/* Parameters: int - number of given command line arguments 
 * Return: void
 * Description: This function checks if the correct number of command line 
 * arguments was given, should have the input and output file given at command 
 * line. Prints error to stderr and exits program if incorrect number
 */
void checkArgs(int);
/* Parameters: FILE* - file pointer that points to the opened file
 * char* - name of the file
 * Return: void
 * Description: checks if the file opened successfully, if not prints error to 
 * stderr with the name of the file that failed to open and exits program
 */
void checkFile(FILE*, char*);
/* Parameters: node_t** - node_t double pointer to head of the linked list
 * Return: void
 * Description: starts at head and loops through the linked list and frees each 
 * node. This function gives back all the memory from the linked list
 */
void deleteList(node_t**);
/* Parameters: bday_t - bday struct containing the day month and year ints
 * Return: bool - returns true for valid date and false for invalid date
 * Description: This function checks the validity of the birthday, if the 
 * birthday is february 29th the isLeapYear function checks if the year was a 
 * leap year or not
 */
bool checkDate(bday_t);
/* Parameters: int - year
 * Return: bool - returns true if is leap year and false for not leap year
 * Description: This function checks if the given year is a leap year or not
 */
bool isLeapYear(int);
#endif