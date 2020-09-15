# PicoCTF 2019 - mus1c
Author: PinkNoize

General Skills - 300

> I wrote you a song. Put it in the picoCTF{} flag format

# Writeup

This challenge provides us with the text file below.

```
Pico's a CTFFFFFFF
my mind is waitin
It's waitin

Put my mind of Pico into This
my flag is not found
put This into my flag
put my flag into Pico


shout Pico
shout Pico
shout Pico

My song's something
put Pico into This

Knock This down, down, down
put This into CTF

shout CTF
my lyric is nothing
Put This without my song into my lyric
Knock my lyric down, down, down

shout my lyric

Put my lyric into This
Put my song with This into my lyric
Knock my lyric down

shout my lyric

Build my lyric up, up ,up

shout my lyric
shout Pico
shout It

Pico CTF is fun
security is important
Fun is fun
Put security with fun into Pico CTF
Build Fun up
shout fun times Pico CTF
put fun times Pico CTF into my song

build it up

shout it
shout it

build it up, up
shout it
shout Pico
```

The challenge here is to realize that these are not actually lyrics to a song but instead code for the programming language rockstar. You can run it [here](https://codewithrockstar.com/online). The output is the flag in decimal format. I converted it using [CyberChef](https://gchq.github.io) and got the flag, `picoCTF{rrrocknrn0113r}`.