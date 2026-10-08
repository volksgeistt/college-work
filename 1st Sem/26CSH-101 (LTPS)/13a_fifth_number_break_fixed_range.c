/*
Question / Aim:
Write a program to find the 5th number and exit using the break statement.
The range is already given as 1 to 10.
*/
#include <stdio.h>

int main(void) {
    int i;

    for (i = 1; i <= 10; i++) {
        if (i == 5) {
            printf("Fifth number: %d\\n", i);
            break;
        }
        printf("%d ", i);
    }

    return 0;
}
