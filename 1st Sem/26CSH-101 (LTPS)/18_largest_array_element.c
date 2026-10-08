/*
Question / Aim:
Write a program to find the largest element in an array.
*/
#include <stdio.h>

int main(void) {
    int i, a[5], largest;

    printf("Enter 5 elements: ");
    for (i = 0; i < 5; i++)
        scanf("%d", &a[i]);

    largest = a[0];
    for (i = 1; i < 5; i++) {
        if (a[i] > largest)
            largest = a[i];
    }

    printf("Largest element = %d\\n", largest);
    return 0;
}
