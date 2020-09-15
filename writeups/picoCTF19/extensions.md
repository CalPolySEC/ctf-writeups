# PicoCTF 2019 - extensions
Author: PinkNoize

Forensics - 150

> This is a really weird text file TXT? Can you find the flag?

# Writeup

This challenge provides us with a file called `flag.txt`. If we try to `cat` the file we get random garbage.

```bash
$ cat flag.txt 
�PNG
�
IHDR���^�sRGB���gAMA��
                      �a	pHYs
```

Near the top of the garbage, we see "PNG" this suggests that this may be a PNG file. We can check this with the `file` command.

```bash
$ file flag.txt 
flag.txt: PNG image data, 1697 x 608, 8-bit/color RGB, non-interlaced
```

This confirms that this really is a PNG file and the .txt extension really has no effect on the actual file structure. We can rename the file to flag.png and view for the flag.

The flag is `picoCTF{now_you_know_about_extensions}`.
