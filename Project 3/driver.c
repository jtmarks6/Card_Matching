/******************************
*Jeremy Marks                 *
*CPSC 2310 Spring 21          *
*UserName: jtmarks            *
*Instructor: Dr. Yvon Feaster *
******************************/
#include "functions.h"

int main(int argc, char *argv[]){
    checkArgs(argc);
    //makes head of linked list and sets to NULL
    struct node_t* head = NULL;
    //opens and checks if files opened successfully
    FILE* file = fopen(argv[1], "r");
    checkFile(file, argv[1]);
    FILE* outFile = fopen(argv[2], "w");
    checkFile(outFile, argv[2]);
    //creates list from input file
    createList(file, &head);
    //uses function pointers to print each type of print function
    print(&PrintList, outFile, head);
    print(&PrintName, outFile, head);
    print(&PrintBDay, outFile, head);
    print(&Song, outFile, head);
    //closes output file
    fclose(outFile);
    //deletes list
    deleteList(&head);
}