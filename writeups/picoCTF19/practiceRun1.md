# PicoCTF 2019 - practice-run-1
Author: PinkNoize

Binary Exploitation - 50

> You're going to need to know how to run programs if you're going to get out of here. Navigate to /problems/practice-run-1_0_62b61488e896645ebff9b6c97d0e775e on the shell server and run this program to receive a flag.

## TL;DR

The challenge provides a program that prints the flag. Run the program to solve the challenge.

# Writeup

The challenge directs us to `/problems/practice-run-1_0_62b61488e896645ebff9b6c97d0e775e` and tells us that we need to run this program to get the flag.

Let's start by listing this directory. The `ls` command lets us list files in a directory. The `-a` flag tells `ls` to show hidden files. The `-l` flag tell `ls` to show permissions, owner, group, file size, modification dates and file name.

```bash
user@pico-2019-shell1:~$ ls -al /problems/practice-run-1_0_62b61488e896645ebff9b6c97d0e775e
total 84
drwxr-xr-x   2 root       root              4096 Sep 28  2019 .
drwxr-x--x 684 root       root             69632 Oct 10  2019 ..
-rwxr-sr-x   1 hacksports practice-run-1_0  7252 Sep 28  2019 run_this
```

We see that there is an executable in that directory named `run_this`. As the description told us to do, let's run the program.

```bash
user@pico-2019-shell1:~$ /problems/practice-run-1_0_62b61488e896645ebff9b6c97d0e775e/run_this 
picoCTF{g3t_r3adY_2_r3v3r53}
```
The program prints the flag and all thats left is to submit the flag.