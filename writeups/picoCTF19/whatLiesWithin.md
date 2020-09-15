# PicoCTF 2019 - What Lies Within
Author: PinkNoize

Forensics - 150

> Theres something in the building. Can you retrieve the flag?

# Writeup

This challenge provides us with another PNG image file. Nothing interesting comes out of running strings and viewing the metadata. We can try to check if there are any other files inside the PNG using `binwalk`.

```bash
$ binwalk -e buildings.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 657 x 438, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, compressed

```

This shows that this a PNG file, but doesn't show there is another file inside. The elimination of these possibilities hints that this challenge is a [steganography](https://en.wikipedia.org/wiki/Steganography) challenge. We can run this against some automatic steganography detection and extraction tools. One of which is [zsteg](https://github.com/zed-0xff/zsteg) which works on PNGs. There is an [online solution](https://aperisolve.fr/) too if you do not wish to install zsteg.

After running the automatic tool we get the output below.

```
b1,r,lsb,xy .. text: "^5>R5YZrG"
b1,rgb,lsb,xy .. text: "picoCTF{h1d1ng_1n_th3_b1t5}"
b1,abgr,msb,xy .. file: PGP Secret Sub-key -
b2,b,lsb,xy .. text: "XuH}p#8Iy="
b3,abgr,msb,xy .. text: "t@Wp-_tH_v\r"
b4,r,lsb,xy .. text: "fdD\"\"\"\" "
b4,r,msb,xy .. text: "%Q#gpSv0c05"
b4,g,lsb,xy .. text: "fDfffDD\"\""
b4,g,msb,xy .. text: "f\"fff\"\"DD"
b4,b,lsb,xy .. text: "\"$BDDDDf"
b4,b,msb,xy .. text: "wwBDDDfUU53w"
b4,rgb,msb,xy .. text: "dUcv%F#A`"
b4,bgr,msb,xy .. text: " V\"c7Ga4"
b4,abgr,msb,xy .. text: "gOC_$_@o"
```

We can see the flag in the second row, `picoCTF{h1d1ng_1n_th3_b1t5}`.

We can see the way the flag was encoded in the information left of the flag.