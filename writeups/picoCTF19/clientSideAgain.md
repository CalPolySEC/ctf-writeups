# PicoCTF 2019 - client-side-again
Author: PinkNoize

Web Exploitation - 200

> Can you break into this super secure portal? https://2019shell1.picoctf.com/problem/12278/ (link) or http://2019shell1.picoctf.com:12278

## TL;DR

This challenge presents us with a login webpage. The flag is hardcoded in obfuscated javascript.

# Writeup

This webpage presents us with a login page. We can view the source to see how this login works.

```html
<html>
<head>
<title>Secure Login Portal V2.0</title>
</head>
<body background="barbed_wire.jpeg" >
<!-- standard MD5 implementation -->
<script type="text/javascript" src="md5.js"></script>

<script type="text/javascript">
  var _0x5a46=['0a0d8}','_again_4','this','Password\x20Verified','Incorrect\x20password','getElementById','value','substring','picoCTF{','not_this'];(function(_0x4bd822,_0x2bd6f7){var _0xb4bdb3=function(_0x1d68f6){while(--_0x1d68f6){_0x4bd822['push'](_0x4bd822['shift']());}};_0xb4bdb3(++_0x2bd6f7);}(_0x5a46,0x1b3));var _0x4b5b=function(_0x2d8f05,_0x4b81bb){_0x2d8f05=_0x2d8f05-0x0;var _0x4d74cb=_0x5a46[_0x2d8f05];return _0x4d74cb;};function verify(){checkpass=document[_0x4b5b('0x0')]('pass')[_0x4b5b('0x1')];split=0x4;if(checkpass[_0x4b5b('0x2')](0x0,split*0x2)==_0x4b5b('0x3')){if(checkpass[_0x4b5b('0x2')](0x7,0x9)=='{n'){if(checkpass[_0x4b5b('0x2')](split*0x2,split*0x2*0x2)==_0x4b5b('0x4')){if(checkpass[_0x4b5b('0x2')](0x3,0x6)=='oCT'){if(checkpass[_0x4b5b('0x2')](split*0x3*0x2,split*0x4*0x2)==_0x4b5b('0x5')){if(checkpass['substring'](0x6,0xb)=='F{not'){if(checkpass[_0x4b5b('0x2')](split*0x2*0x2,split*0x3*0x2)==_0x4b5b('0x6')){if(checkpass[_0x4b5b('0x2')](0xc,0x10)==_0x4b5b('0x7')){alert(_0x4b5b('0x8'));}}}}}}}}else{alert(_0x4b5b('0x9'));}}
</script>
<div style="position:relative; padding:5px;top:50px; left:38%; width:350px; height:140px; background-color:gray">
<div style="text-align:center">
<p>New and Improved Login</p>

<p>Enter valid credentials to proceed</p>
<form action="index.html" method="post">
<input type="password" id="pass" size="8" />
<br/>
<input type="submit" value="verify" onclick="verify(); return false;" />
</form>
</div>
</div>
</body>
</html>
```

There is some javascript that appears to contain parts of the flag. Perhaps this is obfuscated javascript. Let's plug this in a deobfuscator to check. I used https://lelinhtinh.github.io/de4js/.

```javascript
function verify() {
    checkpass = document.getElementById('pass').value;
    split = 4;
    if (checkpass.substring(0, split * 2) == 'picoCTF\{') {
        if (checkpass.substring(7, 9) == '{n') {
            if (checkpass.substring(split * 2, split * 2 * 2) == 'not_this') {
                if (checkpass.substring(3, 6) == 'oCT') {
                    if (checkpass.substring(split * 3 * 2, split * 4 * 2) == '0a0d8\}') {
                        if (checkpass.substring(6, 11) == 'F{not') {
                            if (checkpass.substring(split * 2 * 2, split * 3 * 2) == '_again_4') {
                                if (checkpass.substring(12, 16) == 'this') {
                                    alert('Password Verified');
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        alert('Incorrect password');
    }
}
```

Now that we have deobfuscated the javascript we can see that it checks the password with a bunch substrings, we can map the indices and constants to recover the flag as in the previous challenges.

The flag is `picoCTF{not_this_again_40a0d8}`.