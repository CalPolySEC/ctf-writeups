# PicoCTF 2019 - where-are-the-robots
Author: PinkNoize

Web Exploitation - 100

> Can you find the robots? https://2019shell1.picoctf.com/problem/12267/ (link) or http://2019shell1.picoctf.com:12267

## TL;DR

This challenge consists of a website with a hidden page disclosed in robots.txt. View the hidden page to receive the flag.

# Writeup

We are first presented with a page displaying "Welcome" and "Where are the robots?" This suggests that there may be something at [robots.txt](https://www.robotstxt.org/robotstxt.html).

```
User-agent: *
Disallow: /713d3.html
```

The robots.txt page displays one disallowed html file. Let's view it. Navigating to /713d3.html gives us the flag, `picoCTF{ca1cu1at1ng_Mach1n3s_713d3}`.