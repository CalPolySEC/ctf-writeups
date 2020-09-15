# PicoCTF 2019 - c0rrupt
Author: PinkNoize

Forensics - 250

> We found this file. Recover the flag. You can also find the file in /problems/c0rrupt_0_1fcad1344c25a122a00721e4af86de13.

# TL;DR
This challenge provides us with a corrupted PNG file. Fix the header and a few chunks to recover the image with the flag.

# Writeup

This challenge provides us with a file called `mystery`. We can try deternining the file type by running `file` on it.

```bash
$ file mystery 
mystery: data
```

We can run strings on the file to see if if gives us anything interesting.

```bash
$ strings mystery
C"DR
sRGB
gAMA
        pHYs
DETx^

...

N}`6?
.Tn.9u
hxX@
%3m6
e;>6
        1<o
IEND
```

This leaves us with a few readable strings, one of which is IEND. When googling "IEND", the first result is a link to the PNG file structure. As suggested by the above results along with the challenge name, the file is probably a corrupted PNG.

To see what is corrupted we can read the [PNG specification](https://www.w3.org/TR/PNG-Structure.html) and compare it to our file.

```bash
# Get hex in editable format
$ xxd mystery > mystery.hex
$ head mystery.hex
00000000: 8965 4e34 0d0a b0aa 0000 000d 4322 4452  .eN4........C"DR
00000010: 0000 066a 0000 0447 0802 0000 007c 8bab  ...j...G.....|..
00000020: 7800 0000 0173 5247 4200 aece 1ce9 0000  x....sRGB.......
00000030: 0004 6741 4d41 0000 b18f 0bfc 6105 0000  ..gAMA......a...
00000040: 0009 7048 5973 aa00 1625 0000 1625 0149  ..pHYs...%...%.I
00000050: 5224 f0aa aaff a5ab 4445 5478 5eec bd3f  R$......DETx^..?
00000060: 8e64 cd71 bd2d 8b20 2080 9041 8302 08d0  .d.q.-.  ..A....
00000070: f9ed 40a0 f36e 407b 9023 8f1e d720 8b3e  ..@..n@{.#... .>
00000080: b7c1 0d70 0374 b503 ae41 6bf8 bea8 fbdc  ...p.t...Ak.....
00000090: 3e7d 2a22 336f de5b 55dd 3d3d f920 9188  >}*"3o.[U.==. ..
```

The first 8 bytes of the PNG file should be, `137 80 78 71 13 10 26 10` in decimal or `89 50 4e 47 0d 0a 1a 0a` in hex. After the PNG file signature comes a series of chunks. The first chunk should be a IHDR chunk. After fixing the first line we can try to convert this back into a PNG.

```bash
$ xxd -r mystery.hex > mystery_v2 
$ xxd mystery_v2 > mystery.hex 
$ head mystery.hex
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 066a 0000 0447 0802 0000 007c 8bab  ...j...G.....|..
00000020: 7800 0000 0173 5247 4200 aece 1ce9 0000  x....sRGB.......
00000030: 0004 6741 4d41 0000 b18f 0bfc 6105 0000  ..gAMA......a...
00000040: 0009 7048 5973 aa00 1625 0000 1625 0149  ..pHYs...%...%.I
00000050: 5224 f0aa aaff a5ab 4445 5478 5eec bd3f  R$......DETx^..?
00000060: 8e64 cd71 bd2d 8b20 2080 9041 8302 08d0  .d.q.-.  ..A....
00000070: f9ed 40a0 f36e 407b 9023 8f1e d720 8b3e  ..@..n@{.#... .>
00000080: b7c1 0d70 0374 b503 ae41 6bf8 bea8 fbdc  ...p.t...Ak.....
00000090: 3e7d 2a22 336f de5b 55dd 3d3d f920 9188  >}*"3o.[U.==. ..
```

If we try to open this as a PNG, it will fail. By looking at the hexdump above, we can see that the chunks we see are IHDR sRGB, gAMA and pHYs. Based on the [specification for the pHYs chunk](https://www.w3.org/TR/PNG-Chunks.html), an IDAT chunk should follow. This chunk must also be corrupted. To find easily find this chunk we can assume the pHYs chunk is correct and use its structure to locate where the IDAT chunk starts. The pHYs chunk starts at 0x3e and its length of its contents is 0x9 bytes. This means that the IDAT starts at 0x3e + 0x4 (pHYs length) + 0x4 (chunk type) + 0x9 (chunk data) + 0x4 (CRC) = 0x53.

We can update the file to the contents below to fix the chunk type.

```
00000050: 5224 f0aa aaff a549 4441 5478 5eec bd3f
```

If we try to recreate and open the file now, it will still fail. 

```bash
$ xxd -r mystery.hex > mystery_v2 
$ xxd mystery_v2 > mystery.hex
```

We can take a closer look at the IDAT chunk and see that the size is 0xaaaaffa5 which is huge. This size is also corrupted to we will have to calculate and fix that. The next chunk is probably also an IDAT chunk as the spec say this, `There can be multiple IDAT chunks; if so, they must appear consecutively with no other intervening chunks`.

We can find the address of this with `grep`.

```bash
$ grep IDAT mystery.hex 
00000050: 5224 f0aa aaff a549 4441 5478 5eec bd3f  R$.....IDATx^..?
00010000: 6927 db59 0000 fff4 4944 4154 3697 4678  i'.Y....IDAT6.Fx
00020000: ba6b c1fa 0000 fff4 4944 4154 d5df c0b7  .k......IDAT....
00030000: 5997 d200 0000 18a0 4944 4154 bb9d f54c  Y.......IDAT...L
```

The next IDAT chunk starts at 0x10004. The size of our corrupted chunk should be 0x10004 - (0x53 + 0x4 (length) + 0x4 (chunk type) + 0x4 (CRC)) = 0xffa5. We can then update mystery.hex to the contents below.

```
00000050: 5224 f000 00ff a549 4441 5478 5eec bd3f  R$.....IDATx^..?
```

We can recreate the PNG file.

```
$xxd -r mystery.hex > mystery_v2
```

We can now open the file and get the flag, `picoCTF{c0rrupt10n_1847995}`.
