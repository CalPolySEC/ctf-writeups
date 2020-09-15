# picoCTF 2019 - waves over lambda
Author: PinkNoize

Cryptography - 300

> We made alot of substitutions to encrypt this. Can you decrypt it? Connect with `nc 2019shell1.picoctf.com 37925`.

# Writeup

Upon running the netcat command, we are given a ciphertext.

```
-------------------------------------------------------------------------------
pwxamlez gqmq nz cwbm sfla - smqibqxpc_nz_p_wvqm_flktul_klmztyjwjm
-------------------------------------------------------------------------------
glvnxa glu zwkq enkq le kc unzjwzlf ygqx nx fwxuwx, n glu vnznequ egq tmnenzg kbzqbk, lxu kluq zqlmpg lkwxa egq twwoz lxu kljz nx egq fntmlmc mqalmunxa emlxzcfvlxnl; ne glu zembpo kq egle zwkq swmqoxwyfquaq ws egq pwbxemc pwbfu glmufc slnf ew glvq zwkq nkjwmelxpq nx uqlfnxa yneg l xwtfqklx ws egle pwbxemc. n snxu egle egq unzemnpe gq xlkqu nz nx egq qdemqkq qlze ws egq pwbxemc, hbze wx egq twmuqmz ws egmqq zeleqz, emlxzcfvlxnl, kwfulvnl lxu tbowvnxl, nx egq knuze ws egq plmjlegnlx kwbxelnxz; wxq ws egq ynfuqze lxu fqlze oxwyx jwmenwxz ws qbmwjq. n ylz xwe ltfq ew fnage wx lxc klj wm ywmo anvnxa egq qdlpe fwplfnec ws egq plzefq umlpbfl, lz egqmq lmq xw kljz ws egnz pwbxemc lz cqe ew pwkjlmq yneg wbm wyx wmuxlxpq zbmvqc kljz; tbe n swbxu egle tnzemner, egq jwze ewyx xlkqu tc pwbxe umlpbfl, nz l slnmfc yqff-oxwyx jflpq. n zglff qxeqm gqmq zwkq ws kc xweqz, lz egqc klc mqsmqzg kc kqkwmc ygqx n elfo wvqm kc emlvqfz yneg knxl.
```

As hinted by the desciption, this is a substitution cipher. We can use an [online substitution solver](https://www.guballa.de/substitution-solver) to solve this.

```
-------------------------------------------------------------------------------
congrats here is your flag - frequency_is_c_over_lambda_marsbwpopr
-------------------------------------------------------------------------------
having had some time at my disposal when in london, i had visited the british museum, and made search among the books and maps in the library regarding transylvania; it had struck me that some foreknowledge of the country could hardly fail to have some importance in dealing with a nobleman of that country. i find that the district he named is in the extreme east of the country, just on the borders of three states, transylvania, moldavia and bukovina, in the midst of the carpathian mountains; one of the wildest and least known portions of europe. i was not able to light on any map or work giving the exact locality of the castle dracula, as there are no maps of this country as yet to compare with our own ordnance survey maps; but i found that bistritz, the post town named by count dracula, is a fairly well-known place. i shall enter here some of my notes, as they may refresh my memory when i talk over my travels with mina.
```

The flag is `frequency_is_c_over_lambda_marsbwpopr`.