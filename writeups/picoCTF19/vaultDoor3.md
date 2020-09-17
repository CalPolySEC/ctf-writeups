# PicoCTF 2019 - vault-door-3
Author: PinkNoize

Reverse Engineering - 200

> This vault uses for-loops and byte arrays. The source code for this vault is here: VaultDoor3.java

## TL;DR

This challenge consists of a Java source file with a obfuscated hardcoded password. The input is reordered then compared to the flag.

# Writeup

This challenge provides source code like the similar problems.

```java
import java.util.*;

class VaultDoor3 {
    public static void main(String args[]) {
        VaultDoor3 vaultDoor = new VaultDoor3();
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

    // Our security monitoring team has noticed some intrusions on some of the
    // less secure doors. Dr. Evil has asked me specifically to build a stronger
    // vault door to protect his Doomsday plans. I just *know* this door will
    // keep all of those nosy agents out of our business. Mwa ha!
    //
    // -Minion #2671
    public boolean checkPassword(String password) {
        if (password.length() != 32) {
            return false;
        }
        char[] buffer = new char[32];
        int i;
        for (i=0; i<8; i++) {
            buffer[i] = password.charAt(i);
        }
        for (; i<16; i++) {
            buffer[i] = password.charAt(23-i);
        }
        for (; i<32; i+=2) {
            buffer[i] = password.charAt(46-i);
        }
        for (i=31; i>=17; i-=2) {
            buffer[i] = password.charAt(i);
        }
        String s = new String(buffer);
        return s.equals("jU5t_a_sna_3lpm13g34c_u_4_m3rf48");
    }
}
```

At a quick glance, `checkPassword()` reorders the input then compares it with a hardcoded string. If we can recover the input that reorders to the hardcoded string, we can recover the flag. We can recover the mapping of indices from before reordering to after by modifying the code.

```java
    public boolean checkPassword(String password) {
        if (password.length() != 32) {
          return false;
        }
        char[] buffer = new char[32];
        int i;

        int[] map = new int[32]; // new

        for (i=0; i<8; i++) {
            buffer[i] = password.charAt(i);
            map[i] = i; // new
        }
        for (; i<16; i++) {
            buffer[i] = password.charAt(23-i);
            map[i] = 23-i; // new
        }
        for (; i<32; i+=2) {
            buffer[i] = password.charAt(46-i);
            map[i] = 46-i; // new
        }
        for (i=31; i>=17; i-=2) {
            buffer[i] = password.charAt(i);
            map[i] = i; // new
        }
        String s = new String(buffer);

        System.out.println(Arrays.toString(map)); // new
        
        return s.equals("jU5t_a_sna_3lpm13g34c_u_4_m3rf48");
    }
```

We can run this code with an input of 32 characters (plus the prefix) to recover the mapping.

```bash
┌─[user@host]─[~/vault-door-3]
└──╼ $javac VaultDoor3.java 
┌─[user@host]─[~/vault-door-3]
└──╼ $java VaultDoor3 
Enter vault password: picoCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}
[0, 1, 2, 3, 4, 5, 6, 7, 15, 14, 13, 12, 11, 10, 9, 8, 30, 17, 28, 19, 26, 21, 24, 23, 22, 25, 20, 27, 18, 29, 16, 31]
Access denied!
```

We can then apply the reverse of this mapping to the hardcoded string to recover the flag.

```java
        char[] recovered_flag = new char[32];
        for(i=0;i<32;i++) {
          recovered_flag[i] = "jU5t_a_sna_3lpm13g34c_u_4_m3rf48".charAt(map[i]);
        }
        System.out.println(new String(recovered_flag));
```

We can then run this by compiling the file and running the result.

```bash
┌─[user@host]─[~/vault-door-3]
└──╼ $javac VaultDoor3.java 
┌─[user@host]─[~/vault-door-3]
└──╼ $java VaultDoor3 
Enter vault password: picoCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}
[0, 1, 2, 3, 4, 5, 6, 7, 15, 14, 13, 12, 11, 10, 9, 8, 30, 17, 28, 19, 26, 21, 24, 23, 22, 25, 20, 27, 18, 29, 16, 31]
jU5t_a_s1mpl3_an4gr4m_4_u_c33f38
Access denied!
┌─[static@parrot]─[~/Downloads]
└──╼ $
```

We now just have to wrap the result with the flag prefix to get the flag, `picoCTF{jU5t_a_s1mpl3_an4gr4m_4_u_c33f38}`.