/*
Question / Aim:
(b) Write a program to initialize an array and display its values.
*/
#include <stdio.h>

int main(void) {
    int i, a[5] = {2, 12, 22, 32, 42};

    printf("The values are:\\n");
    for (i = 0; i < 5; i++)
        printf("%d ", a[i]);

    printf("\\n");
    return 0;
}
