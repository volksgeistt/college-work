/*
Question / Aim:
Write a program to count the number of digits in an integer.
*/
#include <stdio.h>

int main(void) {
    int num, count = 0;

    printf("Enter an integer: ");
    scanf("%d", &num);

    if (num == 0) {
        count = 1;
    } else {
        while (num != 0) {
            num /= 10;
            count++;
        }
    }

    printf("Number of digits = %d\\n", count);
    return 0;
}
