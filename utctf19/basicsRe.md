# [basics] re
Category: Reverse Engineering

For this challenge all you had to do was run strings on the picture (to reduce clutter, you can also grep for the flag format)

$ strings [calculator](assets/calculator) | grep "utflag"

Obtained the flag: utflag{str1ng5_15_4_h4ndy_t00l}
