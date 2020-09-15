# PicoCTF 2019 - vault-door-4
Author: PinkNoize

Reverse Engineering - 250

> This vault uses ASCII encoding for the password. The source code for this vault is here: VaultDoor4.java

## TL;DR

This challenge provides a Java source file with a hardcoded password. The password is encoded in different bases and can be converted to ascii to get the flag.

# Writeup

This challenge provides us with a Java source file with a similar setup to the previous challenges. The user input is compared to a byte array.

```java
import java.util.*;

class VaultDoor4 {
    public static void main(String args[]) {
        VaultDoor4 vaultDoor = new VaultDoor4();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String userInput = scanner.next();
	String input = userInput.substring("picoCTF{".length(),userInput.length()-1);
	if (vaultDoor.checkPassword(input)) {
	    System.out.println("Access granted.");
	} else {
	    System.out.println("Access denied!");
        }
    }

    // I made myself dizzy converting all of these numbers into different bases,
    // so I just *know* that this vault will be impenetrable. This will make Dr.
    // Evil like me better than all of the other minions--especially Minion
    // #5620--I just know it!
    //
    //  .:::.   .:::.
    // :::::::.:::::::
    // :::::::::::::::
    // ':::::::::::::'
    //   ':::::::::'
    //     ':::::'
    //       ':'
    // -Minion #7781
    public boolean checkPassword(String password) {
        byte[] passBytes = password.getBytes();
        byte[] myBytes = {
            106 , 85  , 53  , 116 , 95  , 52  , 95  , 98  ,
            0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f,
            0142, 0131, 0164, 063 , 0163, 0137, 063 , 0141,
            '7' , '2' , '4' , 'c' , '8' , 'f' , '9' , '2' ,
        };
        for (int i=0; i<32; i++) {
            if (passBytes[i] != myBytes[i]) {
                return false;
            }
        }
        return true;
    }
}
```

To extract the flag we have to convert each byte in `myBytes` to ascii. We must also notice that the bytes are stored in many different forms, such as decimal, hex, octal and ascii. Alternatively, we could convert `myBytes` to a string and print it for the flag.

```java
...
import java.nio.charset.StandardCharsets;
...
    public boolean checkPassword(String password) {
        byte[] passBytes = password.getBytes();
        byte[] myBytes = {
            106 , 85  , 53  , 116 , 95  , 52  , 95  , 98  ,
            0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f,
            0142, 0131, 0164, 063 , 0163, 0137, 063 , 0141,
            '7' , '2' , '4' , 'c' , '8' , 'f' , '9' , '2' ,
        };
        System.out.println(new String(myBytes, StandardCharsets.UTF_8));
        for (int i=0; i<32; i++) {
            if (passBytes[i] != myBytes[i]) {
                return false;
            }
        }
        return true;
    }
```

We can then compile and run this to get the flag.

```bash
┌─[user@host]─[~/vault-door-4]
└──╼ $javac VaultDoor4.java 
┌─[user@host]─[~/vault-door-4]
└──╼ $java VaultDoor4
Enter vault password: picoCTF{asdfasdfasdf}
jU5t_4_bUnCh_0f_bYt3s_3a724c8f92
Access denied!
```

So the flag is `picoCTF{jU5t_4_bUnCh_0f_bYt3s_3a724c8f92}`.