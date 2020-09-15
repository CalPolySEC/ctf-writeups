# PicoCTF 2019 - seed-sPRiNG
Author: PinkNoize

Binary Exploitation - 350

> The most revolutionary game is finally available: seed sPRiNG is open right now! seed_spring. Connect to it with `nc 2019shell1.picoctf.com 32233`.

## TL;DR

This challenge provides a program that generates random numbers and asks to guess them. Use the current time to seed the PRNG to recover the random numbers to get the flag.

# Writeup

This challenge provides us with a binary and a netcat command, `nc 2019shell1.picoctf.com 32233`. The binary is a 32-bit binary and I will be using [Cutter](https://cutter.re/) to reverse engineer it. When we connect, we get a prompt asking us how high we will fly.

```bash
┌─[user@hostname]─[~]
└──╼ $nc 2019shell1.picoctf.com 32233


                                                                             
                          #                mmmmm  mmmmm    "    mm   m   mmm 
  mmm    mmm    mmm    mmm#          mmm   #   "# #   "# mmm    #"m  # m"   "
 #   "  #"  #  #"  #  #" "#         #   "  #mmm#" #mmmm"   #    # #m # #   mm
  """m  #""""  #""""  #   #          """m  #      #   "m   #    #  # # #    #
 "mmm"  "#mm"  "#mm"  "#m##         "mmm"  #      #    " mm#mm  #   ##  "mmm"
                                                                             


Welcome! The game is easy: you jump on a sPRiNG.
How high will you fly?

LEVEL (1/30)

Guess the height: 24
WRONG! Sorry, better luck next time!
```

Connecting show us that we have to guess the height right 30 times in a row. If we want to accurately predict that we should start by reverse engineering the binary. Below is `main` decompiled.

```c
// WARNING: Variable defined which should be unmapped: var_8h
// WARNING: [r2ghidra] Failed to match type time_t for variable seed to Decompiler type: Unknown type identifier time_t
// WARNING: [r2ghidra] Failed to match type signed int for variable var_ch to Decompiler type: Unknown type identifier
// signed
// WARNING: [r2ghidra] Var argv is stack pointer based, which is not supported for decompilation.

undefined4 main(void)
{
    uint32_t uVar1;
    int32_t unaff_EBX;
    int32_t **ppiVar2;
    int32_t *apiStack44 [3];
    int32_t iStack32;
    int32_t var_18h;
    uint32_t var_14h;
    int32_t seed;
    undefined *var_ch;
    int32_t var_8h;
    
    var_ch = &stack0x00000004;
    __x86.get_pc_thunk.bx();
    puts(unaff_EBX + 0x2ca);
    puts(unaff_EBX + 0x2ca);
    puts(unaff_EBX + 0x2da);
    puts(unaff_EBX + 0x32a);
    puts(unaff_EBX + 0x37a);
    puts(unaff_EBX + 0x3ca);
    puts(unaff_EBX + 0x41a);
    puts(unaff_EBX + 0x46a);
    puts(unaff_EBX + 0x2da);
    puts(unaff_EBX + 0x2ca);
    puts(unaff_EBX + 0x2ca);
    puts(unaff_EBX + 0x4ba);
    puts(unaff_EBX + 0x4eb);
    puts(unaff_EBX + 0x2ca);
    fflush(**(undefined4 **)(unaff_EBX + 0x187e));
    var_14h = time(0);
    srand(var_14h);
    ppiVar2 = apiStack44 + 3;
    seed = 1;
    while (seed < 0x1f) {
        *(int32_t *)((int32_t)ppiVar2 + -0xc) = seed;
        *(int32_t *)((int32_t)ppiVar2 + -0x10) = unaff_EBX + 0x502;
        *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x8c9;
        printf();
        *(int32_t *)((int32_t)ppiVar2 + -0x10) = unaff_EBX + 0x2ca;
        *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x8db;
        puts();
        *(undefined4 *)((int32_t)ppiVar2 + -4) = 0x8e3;
        uVar1 = rand();
        var_18h = uVar1 & 0xf;
        *(int32_t *)((int32_t)ppiVar2 + -0x10) = unaff_EBX + 0x511;
        *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x8f8;
        printf();
        *(undefined4 *)((int32_t)ppiVar2 + -0x10) = **(undefined4 **)(unaff_EBX + 0x187e);
        *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x90c;
        fflush();
        *(int32_t ***)((int32_t)ppiVar2 + -0xc) = apiStack44 + 3;
        *(int32_t *)((int32_t)ppiVar2 + -0x10) = unaff_EBX + 0x524;
        *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x922;
        __isoc99_scanf();
        *(undefined4 *)((int32_t)ppiVar2 + -0x10) = **(undefined4 **)(unaff_EBX + 0x187a);
        *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x936;
        fflush();
        if (var_18h != iStack32) {
            *(int32_t *)((int32_t)ppiVar2 + -0x10) = unaff_EBX + 0x52a;
            *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x950;
            puts();
            *(undefined4 *)((int32_t)ppiVar2 + -0x10) = **(undefined4 **)(unaff_EBX + 0x187e);
            *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x964;
            fflush();
            *(undefined4 *)((int32_t)ppiVar2 + -0x10) = 0xffffffff;
            *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x971;
            exit();
            ppiVar2 = (int32_t **)((int32_t)ppiVar2 + -0x10);
        }
        seed = seed + 1;
    }
    *(int32_t *)((int32_t)ppiVar2 + -0x10) = unaff_EBX + 0x552;
    *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x98e;
    puts();
    *(undefined4 *)((int32_t)ppiVar2 + -4) = 0x996;
    get_flag();
    *(undefined4 *)((int32_t)ppiVar2 + -0x10) = **(undefined4 **)(unaff_EBX + 0x187e);
    *(undefined4 *)((int32_t)ppiVar2 + -0x14) = 0x9a7;
    fflush();
    return 0;
}
```

Although the decompilation is messed up, we can still get the important information out of it. First, we can see that there is a large while loop. In the while loop we can see that `if var_18h != iStack32` then the program exits. `iStack32` is probably the user input from the call to `__isoc99_scanf` as `var_18h` is assigned further above. `var_18h` is set by a call to `rand() & 0xF`. If we guessed randomly we would have a 1/16 chance per each level, which means it would be unlikely that we get all 30 levels correct. So in order to guess all 30 levels correct we are going to have to predict `rand`. This is actually pretty easy to do as all software based random number generators are what are known as pseudorandom number generators (PRNGs), which are deterministic based on the seed value. By reading the man page for `rand` we learn that the random generator is seeded by a call to `srand`. As this program seeds the generator with the current time, we can seed a generator on our machine with the same value to predict the random numbers. `var_14h = time(0); srand(var_14h);`

As much as I would like to solve this  using python, it would introduce many problems as the binary is 32 bit (if you have 32-bit python this doesn't apply). If the binary was 64-bit we would be able to use ctypes to call `srand` and `rand` in python. Since it is 32 bit we have to build a 32-bit binary that generates the random numbers for us. The code for this is below and can be compiled with `gcc -m32 rand_gen.c -o rand_gen`. This binary must be 32-bit to use the same 32-bit libc that seed_spring does.

```c
// rand_gen.c
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

int main() {
	srand(time(0));
	for(int i=0;i<30;i++)
		printf("%d\n", rand()&0xF);
}
```

Then to solve you can run `./rand_gen | nc 2019shell1.picoctf.com 32233`.

NOTE: Running this on a machine other then 2019shell1.picoctf.com may not work as the other machine may have a different time or libc.

```bash
PinkNoize@pico-2019-shell1:~$ ./rand_gen | nc 2019shell1.picoctf.com 32233


                                                                             
                          #                mmmmm  mmmmm    "    mm   m   mmm 
  mmm    mmm    mmm    mmm#          mmm   #   "# #   "# mmm    #"m  # m"   "
 #   "  #"  #  #"  #  #" "#         #   "  #mmm#" #mmmm"   #    # #m # #   mm
  """m  #""""  #""""  #   #          """m  #      #   "m   #    #  # # #    #
 "mmm"  "#mm"  "#mm"  "#m##         "mmm"  #      #    " mm#mm  #   ##  "mmm"
                                                                             


Welcome! The game is easy: you jump on a sPRiNG.
How high will you fly?

LEVEL (1/30)

Guess the height: LEVEL (2/30)

Guess the height: LEVEL (3/30)

Guess the height: LEVEL (4/30)

Guess the height: LEVEL (5/30)

Guess the height: LEVEL (6/30)

Guess the height: LEVEL (7/30)

Guess the height: LEVEL (8/30)

Guess the height: LEVEL (9/30)

Guess the height: LEVEL (10/30)

Guess the height: LEVEL (11/30)

Guess the height: LEVEL (12/30)

Guess the height: LEVEL (13/30)

Guess the height: LEVEL (14/30)

Guess the height: LEVEL (15/30)

Guess the height: LEVEL (16/30)

Guess the height: LEVEL (17/30)

Guess the height: LEVEL (18/30)

Guess the height: LEVEL (19/30)

Guess the height: LEVEL (20/30)

Guess the height: LEVEL (21/30)

Guess the height: LEVEL (22/30)

Guess the height: LEVEL (23/30)

Guess the height: LEVEL (24/30)

Guess the height: LEVEL (25/30)

Guess the height: LEVEL (26/30)

Guess the height: LEVEL (27/30)

Guess the height: LEVEL (28/30)

Guess the height: LEVEL (29/30)

Guess the height: LEVEL (30/30)

Guess the height: picoCTF{pseudo_random_number_generator_not_so_random_6c0fef32265de90489279a99eec7743c}Congratulation! You've won! Here is your flag:

```
