/*
Question / Aim:
Write a program to find the first and last digit of a number.
*/
#include <stdio.h>

int main() {
    int num, first, last, count;

    printf("Enter any number: ");
    scanf("%d", &num);

    if (num < 0)
        num = -num;

    last = num % 10;
    first = num;

    while (first >= 10)
        first /= 10;

    printf("First digit = %d\\n", first);
    printf("Last digit = %d\\n", last);

    return 0;
}
