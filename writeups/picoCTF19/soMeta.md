# PicoCTF 2019 - So Meta
Author: PinkNoize

Forensics - 150

> Find the flag in this picture. You can also find the file in /problems/so-meta_1_ab9d99603935344b81d7f07973e70155.

# Writeup

This challenge provides us with an PNG image file.

![](assets/soMetaImage.png)

Upon visual inspection there is nothing interesting in the image file. The title of this challenge hints about metadata of the image. We can view the metadata of the image with the `identify` tool from the `imagemagick` tool suite.

```bash
$ identify -verbose ~/ctf-writeups/writeups/picoCTF19/assets/soMetaImage.png 
Image: /home/static/ctf-writeups/writeups/picoCTF19/assets/soMetaImage.png
  Format: PNG (Portable Network Graphics)
  Geometry: 600x600
  Class: DirectClass
  Type: true color
  Depth: 8 bits-per-pixel component
  Channel Depths:
    Red:      8 bits
    Green:    8 bits
    Blue:     8 bits
  Channel Statistics:
    Red:
      Minimum:                     0.00 (0.0000)
      Maximum:                 65535.00 (1.0000)
      Mean:                    46024.58 (0.7023)
      Standard Deviation:      25298.92 (0.3860)
    Green:
      Minimum:                     0.00 (0.0000)
      Maximum:                 65535.00 (1.0000)
      Mean:                    46024.47 (0.7023)
      Standard Deviation:      25299.02 (0.3860)
    Blue:
      Minimum:                     0.00 (0.0000)
      Maximum:                 65535.00 (1.0000)
      Mean:                    46024.66 (0.7023)
      Standard Deviation:      25298.91 (0.3860)
  Filesize: 106.2Ki
  Interlace: No
  Orientation: Unknown
  Background Color: white
  Border Color: #DFDFDF
  Matte Color: #BDBDBD
  Page geometry: 600x600+0+0
  Compose: Over
  Dispose: Undefined
  Iterations: 0
  Compression: Zip
  Png:IHDR.color-type-orig: 2
  Png:IHDR.bit-depth-orig: 8
  Software: Adobe ImageReady
  Artist: picoCTF{s0_m3ta_368a0341}
  Signature: af96cc3fb94bdba64dea0ea1c3141d96bddfbabb4251910681cd52d3eabad77c
  Tainted: False
  User Time: 0.010u
  Elapsed Time: 0m:0.003818s
  Pixels Per Second: 89.9Mi
```

We find the flag in the artist field, `picoCTF{s0_m3ta_368a0341}`.
