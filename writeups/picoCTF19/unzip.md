# PicoCTF 2019 - unzip
Author: PinkNoize

Forensics - 50

> Can you unzip this file and get the flag?

# Writeup

This challenge provides us with a zip file. We can unzip the file with the command, `unzip`.

```bash
$ unzip flag.zip 
Archive:  flag.zip
  inflating: flag.png
```

This provides us with the image below.

![](assets/unzipFlag.png)

The flag is `picoCTF{unz1pp1ng_1s_3a5y}`.