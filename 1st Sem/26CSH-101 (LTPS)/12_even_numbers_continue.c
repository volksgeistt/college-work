/*
Question / Aim:
Write a program to display even numbers using the continue statement.
*/
#include <stdio.h>

int main(void) {
    int i;

    for (i = 0; i <= 10; i++) {
        if (i % 2 != 0)
            continue;
        printf("%d ", i);
    }

    printf("\\n");
    return 0;
}
