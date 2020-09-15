# PicoCTF 2019 - vault-door-training
Author: PinkNoize

Reverse Engineering - 50

> Your mission is to enter Dr. Evil's laboratory and retrieve the blueprints for his Doomsday Project. The laboratory is protected by a series of locked vault doors. Each door is controlled by a computer and requires a password to open. Unfortunately, our undercover agents have not been able to obtain the secret passwords for the vault doors, but one of our junior agents obtained the source code for each vault's computer! You will need to read the source code for each level to figure out what the password is for that vault door. As a warmup, we have created a replica vault in our training facility. The source code for the training vault is here: VaultDoorTraining.java

## TL;DR

The challenge consists of a Java source file with a hardcoded password that is the flag.

# Writeup

The challenge description directs us to a Java source file.

```java
import java.util.*;

class VaultDoorTraining {
    public static void main(String args[]) {
        VaultDoorTraining vaultDoor = new VaultDoorTraining();
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

    // The password is below. Is it safe to put the password in the source code?
    // What if somebody stole our source code? Then they would know what our
    // password is. Hmm... I will think of some ways to improve the security
    // on the other doors.
    //
    // -Minion #9567
    public boolean checkPassword(String password) {
        return password.equals("w4rm1ng_Up_w1tH_jAv4_fcb79c48f5b");
    }
}
```

In `main()` we can see that `userInput` is check with the vault door password in `vaultDoor.checkPassword(input)`.
In `checkPassword()` we can see that the password is `w4rm1ng_Up_w1tH_jAv4_fcb79c48f5b`. We can combine this with picoCTF{} to get the full flag, `picoCTF{w4rm1ng_Up_w1tH_jAv4_fcb79c48f5b}`.