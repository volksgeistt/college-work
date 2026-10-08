/*
Question / Aim:
Write a program to insert an element in an array at a specific position.
Positions are entered using 1-based numbering.
*/
#include <stdio.h>

int main(void) {
    int i, n, position, value, a[101];

    printf("Enter number of elements (maximum 100): ");
    scanf("%d", &n);
    if (n < 0 || n >= 100) {
        printf("Invalid number of elements.\\n");
        return 1;
    }

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);

    printf("Enter position for the new element (1 to %d): ", n + 1);
    scanf("%d", &position);
    if (position < 1 || position > n + 1) {
        printf("Invalid position.\\n");
        return 1;
    }

    printf("Enter value to add: ");
    scanf("%d", &value);

    for (i = n; i >= position; i--)
        a[i] = a[i - 1];

    a[position - 1] = value;
    n++;

    printf("Updated array:\\n");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    printf("\\n");
    return 0;
}
