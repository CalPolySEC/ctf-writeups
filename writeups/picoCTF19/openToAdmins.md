# PicoCTF 2019 - Open-to-admins
Author: PinkNoize

Web Exploitation - 200

> This secure website allows users to access the flag only if they are admin and if the time is exactly 1400. https://2019shell1.picoctf.com/problem/32249/ (link) or http://2019shell1.picoctf.com:32249

## TL;DR

The challenge provides a website with a protected flag page. Set admin cookie and time cookie to get the flag.

# Writeup

This challenge starts by directing us to a page with a big flag button. If you click on the flag button it tries to access `/flag` but redirects us back with an error message `I'm sorry it doesn't look like you are the admin or it's the incorrect time`. We will have to find a way that makes us admin and set or determine the time. This cannot be done by signing in as the sign in page has not been implemented.

The challenge provides a hint saying, `Can cookies help you to get the flag?`. Perhaps if we set an admin cookie and set a time cookie we can get the flag.

```bash
$ curl https://2019shell1.picoctf.com/problem/32249/flag -b 'admin=True;time=1400' | grep picoCTF{
            <p style="text-align:center; font-size:30px;"><b>Flag</b>: <code>picoCTF{0p3n_t0_adm1n5_cc661e91}</code></p>
```

We now have the flag, `picoCTF{0p3n_t0_adm1n5_cc661e91}`.