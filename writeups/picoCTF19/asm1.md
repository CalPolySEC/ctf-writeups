# PicoCTF 2019 - asm1
Author: PinkNoize

Reverse Engineering - 200

> What does asm1(0x610) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source located in the directory at /problems/asm1_1_95494d904d73b330976420bc1cd763ec.

## TL;DR

This challenge provides and assembly function and an input. The return value in hex is the flag.

# Writeup

The challenge description asks us to determine the return value of the given assembly function when the argument is 0x610.

```gas
asm1:
        <+0>:   push   ebp
        <+1>:   mov    ebp,esp
        <+3>:   cmp    DWORD PTR [ebp+0x8],0x3b9
        <+10>:  jg     0x50f <asm1+34>
        <+12>:  cmp    DWORD PTR [ebp+0x8],0x1
        <+16>:  jne    0x507 <asm1+26>
        <+18>:  mov    eax,DWORD PTR [ebp+0x8]
        <+21>:  add    eax,0x11
        <+24>:  jmp    0x526 <asm1+57>
        <+26>:  mov    eax,DWORD PTR [ebp+0x8]
        <+29>:  sub    eax,0x11
        <+32>:  jmp    0x526 <asm1+57>
        <+34>:  cmp    DWORD PTR [ebp+0x8],0x477
        <+41>:  jne    0x520 <asm1+51>
        <+43>:  mov    eax,DWORD PTR [ebp+0x8]
        <+46>:  sub    eax,0x11
        <+49>:  jmp    0x526 <asm1+57>
        <+51>:  mov    eax,DWORD PTR [ebp+0x8]
        <+54>:  add    eax,0x11
        <+57>:  pop    ebp
        <+58>:  ret    
```

Before we can understand how this function will behave, we first have to understand a little about how it is called. As this is x86 (32-bit) assembly, function arguments are placed on the stack. For a better description of the stack, read [this](overflow0.md).

To call the function with 0x610 we would write...

```gas
...
push 0x610
call asm1
...
```

This means that when the function is called, the return address is esp+0 and the argument is esp+4.
The first instruction, `<+0>:   push   ebp`, backs up the previous stack frame's base pointer. This moves the stack down by 4 so the argument is now at esp+8.

The second instruction, `<+1>:   mov    ebp,esp`, sets ebp=esp. This sets up the current base pointer so its easy to find arguments and local variables. The first argument will now be referenced by ebp+8. From here on its a matter of keeping track of the jumps and eax. The green lines are instructions that are executed.

```diff
asm1:
+       <+0>:   push   ebp
+       <+1>:   mov    ebp,esp
+       <+3>:   cmp    DWORD PTR [ebp+0x8],0x3b9
+       <+10>:  jg     0x50f <asm1+34> --------------
-       <+12>:  cmp    DWORD PTR [ebp+0x8],0x1      |
-       <+16>:  jne    0x507 <asm1+26>              |
-       <+18>:  mov    eax,DWORD PTR [ebp+0x8]      |
-       <+21>:  add    eax,0x11                     |
-       <+24>:  jmp    0x526 <asm1+57>              |
-       <+26>:  mov    eax,DWORD PTR [ebp+0x8]      |
-       <+29>:  sub    eax,0x11                     |
-       <+32>:  jmp    0x526 <asm1+57>              |
+       <+34>:  cmp    DWORD PTR [ebp+0x8],0x477 <---
+    --- <+41>:  jne    0x520 <asm1+51>
-    |  <+43>:  mov    eax,DWORD PTR [ebp+0x8]
-    |  <+46>:  sub    eax,0x11
-    |  <+49>:  jmp    0x526 <asm1+57>
+    -> <+51>:  mov    eax,DWORD PTR [ebp+0x8] ; eax=0x610
+       <+54>:  add    eax,0x11 ; eax + 0x11 = 0x621
+       <+57>:  pop    ebp
+       <+58>:  ret    
```

To get the return value after the function returns, we read eax. This means the return value is 0x621, which is the flag.