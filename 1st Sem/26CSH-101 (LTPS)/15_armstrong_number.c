/*
Question / Aim:
Write a program to check whether a number is an Armstrong number or not.
This version follows the three-digit Armstrong-number method in the notebook.
*/
#include <stdio.h>

int main(void) {
    int num, original, digit, sum = 0;

    printf("Enter a number: ");
    scanf("%d", &num);

    original = num;
    while (num != 0) {
        digit = num % 10;
        sum += digit * digit * digit;
        num /= 10;
    }

    if (sum == original)
        printf("%d is an Armstrong number.\\n", original);
    else
        printf("%d is not an Armstrong number.\\n", original);

    return 0;
}
