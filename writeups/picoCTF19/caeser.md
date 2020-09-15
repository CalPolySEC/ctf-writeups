# PicoCTF 2019 - caeser
Author: PinkNoize

Cryptography - 100

> Decrypt this message. You can find the ciphertext in /problems/caesar_5_d706b250ed3c6d2d2c72155de301a2f1 on the shell server.

# Writeup

The message provided is `picoCTF{dspttjohuifsvcjdpobqjtwtvk}`. As the name of this challenge is caeser, I am assuming that this flag is encrypted using the [caeser cipher](https://en.wikipedia.org/wiki/Caesar_cipher). The caeser cipher works by shifting each letter in the plaintext by some number forward. If it goes past the end of the alphabet it rotates back to the beginning. As there are only 25 possible keys we can try them all until we get a result that looks like language.

After trying 'b' or 1 as the key we get, `picoCTF{crossingtherubiconapisvsuj}`
