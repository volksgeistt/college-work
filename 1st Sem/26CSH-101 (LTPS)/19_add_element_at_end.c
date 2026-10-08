/*
Question / Aim:
Write a program to add an element at the end of an array.
*/
#include <stdio.h>

int main(void) {
    int i, n, value, a[101];

    printf("Enter number of elements (maximum 100): ");
    scanf("%d", &n);
    if (n < 0 || n >= 100) {
        printf("Invalid number of elements.\\n");
        return 1;
    }

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);

    printf("Enter value to add at end: ");
    scanf("%d", &value);

    a[n] = value;
    n++;

    printf("Updated array:\\n");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    printf("\\n");
    return 0;
}
