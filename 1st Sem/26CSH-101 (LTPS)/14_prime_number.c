/*
Question / Aim:
Write a program to find whether a number is prime or not.
*/
#include <stdio.h>

int main(void) {
    int num, i, isPrime = 1;

    printf("Enter a number: ");
    scanf("%d", &num);

    if (num < 2)
        isPrime = 0;
    else {
        for (i = 2; i * i <= num; i++) {
            if (num % i == 0) {
                isPrime = 0;
                break;
            }
        }
    }

    if (isPrime)
        printf("%d is prime.\\n", num);
    else
        printf("%d is not prime.\\n", num);

    return 0;
}
