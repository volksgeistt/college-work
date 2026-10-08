/*
Question / Aim:
Write a program to delete an element from an array from the end.
*/
#include <stdio.h>

int main() {
    int i, n, a[100];

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

    n--;

    printf("\\nArray after deleting the last element:\\n");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    printf("\\n");
    return 0;
}
