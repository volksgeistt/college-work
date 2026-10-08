/*
Question / Aim:
Write a program to print the table of any number using a loop.
*/
#include <stdio.h>

int main(void) {
    int num, i;

    printf("Enter the number: ");
    scanf("%d", &num);

    for (i = 1; i <= 10; i++)
        printf("%d x %d = %d\\n", num, i, num * i);

    return 0;
}
