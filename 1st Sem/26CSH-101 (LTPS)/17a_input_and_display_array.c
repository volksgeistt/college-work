/*
Question / Aim:
(a) Write a program to declare an array, input its values, and display them.
*/
#include <stdio.h>

int main() {
    int i, a[5];

    printf("Enter 5 values: ");
    for (i = 0; i < 5; i++)
        scanf("%d", &a[i]);

    printf("The values are:\\n");
    for (i = 0; i < 5; i++)
        printf("%d ", a[i]);

    printf("\\n");
    return 0;
}
