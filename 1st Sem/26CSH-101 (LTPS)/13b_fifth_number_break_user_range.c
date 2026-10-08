/*
Question / Aim:
Write a program to find the 5th number and exit using the break statement.
The user provides the starting and ending values.
*/
#include <stdio.h>

int main() {
    int a, b, i, count = 0;

    printf("Enter first and last values: ");
    scanf("%d %d", &a, &b);

    for (i = a; i <= b; i++) {
        count++;
        if (count == 5) {
            printf("Fifth number: %d\\n", i);
            break;
        }
    }

    if (count < 5)
        printf("The range contains fewer than five numbers.\\n");

    return 0;
}
