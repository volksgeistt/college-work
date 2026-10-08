/*
Question / Aim:
Write a program to delete an element from an array at a specific position.
Positions are entered using 1-based numbering.
*/
#include <stdio.h>

int main() {
    int i, n, position, a[100];

    printf("Enter number of elements (1 to 100): ");
    scanf("%d", &n);
    if (n < 1 || n > 100) {
        printf("Invalid number of elements.\\n");
        return 1;
    }

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);

    printf("Your array is:\\n");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    printf("\\nEnter position to delete (1 to %d): ", n);
    scanf("%d", &position);
    if (position < 1 || position > n) {
        printf("Invalid position.\\n");
        return 1;
    }

    for (i = position - 1; i < n - 1; i++)
        a[i] = a[i + 1];

    n--;

    printf("Updated array:\\n");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    printf("\\n");
    return 0;
}
