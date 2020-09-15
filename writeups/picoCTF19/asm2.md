# PicoCTF 2019 - asm2
Author: PinkNoize

Reverse Engineering - 250

> What does asm2(0x10,0x18) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source located in the directory at /problems/asm2_0_a50f0b17a6f50b50a53305ebd71af535.

## TL;DR

This challenge provides and assembly function and an input. The return value in hex is the flag.

# Writeup

This challenge provides with an assembly function just like [asm1](asm1.md). The arguments to this function are 0x10 and 0x18. The solution as detailed in the description is the return value.

```gas
asm2:
	<+0>:	push   ebp
	<+1>:	mov    ebp,esp
	<+3>:	sub    esp,0x10
	<+6>:	mov    eax,DWORD PTR [ebp+0xc]
	<+9>:	mov    DWORD PTR [ebp-0x4],eax
	<+12>:	mov    eax,DWORD PTR [ebp+0x8]
	<+15>:	mov    DWORD PTR [ebp-0x8],eax
	<+18>:	jmp    0x50c <asm2+31>
	<+20>:	add    DWORD PTR [ebp-0x4],0x1
	<+24>:	add    DWORD PTR [ebp-0x8],0xcb
	<+31>:	cmp    DWORD PTR [ebp-0x8],0xb693
	<+38>:	jle    0x501 <asm2+20>
	<+40>:	mov    eax,DWORD PTR [ebp-0x4]
	<+43>:	leave  
	<+44>:	ret    
```

This function starts like any other function by backing up the previous base pointer and setting the current base pointer. It then allocates 0x10 bytes for local variables, `sub    esp,0x10`. As we noticed in asm1, the first argument is located at ebp+0x8. Since this is 32 bit x86, a register is 4 bytes. This can let us assume that integers will also be 4 bytes too. Using this assumption, we can say that the 2nd argument is located at ebp+(0x8+0x4) = ebp+0xc. Using this knowledge we can now step through the instructions keeping track of the registers.

```diff
asm2:
+	<+0>:	push   ebp
+	<+1>:	mov    ebp,esp
+	<+3>:	sub    esp,0x10
+	<+6>:	mov    eax,DWORD PTR [ebp+0xc] ; eax = arg2 = 0x18
+	<+9>:	mov    DWORD PTR [ebp-0x4],eax ; var1 -> [ebp-0x4] = 0x18
+	<+12>:	mov    eax,DWORD PTR [ebp+0x8] ; eax = arg1 = 0x10
+	<+15>:	mov    DWORD PTR [ebp-0x8],eax ; var2 -> [ebp-0x8] = 0x10
+	<+18>:	jmp    0x50c <asm2+31> ; stopped here
	<+20>:	add    DWORD PTR [ebp-0x4],0x1
	<+24>:	add    DWORD PTR [ebp-0x8],0xcb
	<+31>:	cmp    DWORD PTR [ebp-0x8],0xb693
	<+38>:	jle    0x501 <asm2+20>
	<+40>:	mov    eax,DWORD PTR [ebp-0x4]
	<+43>:	leave  
	<+44>:	ret  
```

We now notice that there is a jmp that goes to a comparison. As there is a conditional jump after this, we know this is either an if statement or a loop. Given that the jump goes backward and falls back onto the same comparison we can conclude that this is a loop. This loop may get difficult to keep track of so I am going to convert this assembly to C and analyze it further from there.

NOTE: If you cannot convert between asm and C, don't worry as it is a skill that comes with experience. One way to improve this is to write C code and view the generated assembly at different optimization levels. This will help you identify common patterns that easily translate to C, such as a loop.

```c++
int asm2(int arg1, int arg2) {
    int var1; // [ebp-0x4]
    int var2; // [ebp-0x8]

    var1 = arg2; // mov eax,DWORD PTR [ebp+0xc]; mov DWORD PTR [ebp-0x4],eax
    var2 = arg1; //mov eax,DWORD PTR [ebp+0x8]; mov DWORD PTR [ebp-0x8],eax

    while(var2 <= 0xb693) { //cmp DWORD PTR [ebp-0x8],0xb693; jle    0x501
        var1 += 1; // add DWORD PTR [ebp-0x4],0x1
        var2 += 0xcb; // add DWORD PTR [ebp-0x8],0xcb
    }
    return var1; // mov eax,DWORD PTR [ebp-0x4]; leave; ret
}
```

As we can see from the C code, the return value is `var1` after the loop. Let's emulate this loop using python.

```python
>>> var1 = 0x18
>>> var2 = 0x10
>>> while var2 <= 0xb693:
...     var1 += 1
...     var2 += 0xcb
... 
>>> var1
255
>>> hex(var1)
'0xff'
```

We now know the result is 0xff.
