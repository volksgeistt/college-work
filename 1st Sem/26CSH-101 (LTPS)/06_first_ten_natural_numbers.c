/*
Question / Aim:
Write a program using a loop to print the first 10 natural numbers.
*/
#include <stdio.h>

int main(void) {
    int i;

    for (i = 1; i <= 10; i++)
        printf("%d ", i);

    printf("\\n");
    return 0;
}
