/*
Question / Aim:
Write a program to input a starting value and an ending value,
then find the sum of all even numbers in that range.
*/
#include <stdio.h>

int main(void) {
    int a, b, i, sum = 0;

    printf("Enter starting number: ");
    scanf("%d", &a);
    printf("Enter ending number: ");
    scanf("%d", &b);

    for (i = a; i <= b; i++) {
        if (i % 2 == 0)
            sum += i;
    }

    printf("Sum = %d\\n", sum);
    return 0;
}
