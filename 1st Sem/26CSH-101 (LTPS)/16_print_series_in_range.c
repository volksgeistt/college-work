/*
Question / Aim:
Write a program to input a series/range of numbers (starting and ending
values provided by the user) and display those numbers.
*/
#include <stdio.h>

int main() {
    int a, b, i;

    printf("Enter first number: ");
    scanf("%d", &a);
    printf("Enter last number: ");
    scanf("%d", &b);

    for (i = a; i <= b; i++)
        printf("%d ", i);

    printf("\\n");
    return 0;
}
