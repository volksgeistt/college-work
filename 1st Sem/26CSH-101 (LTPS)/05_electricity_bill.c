/*
Question / Aim:
Demonstrate an electricity bill calculation in which the unit charge
changes by slab, and calculate the total bill.
*/
#include <stdio.h>

int main(void) {
    int units;
    float bill;

    printf("Enter electricity units: ");
    scanf("%d", &units);

    if (units < 0) {
        printf("Units cannot be negative.\\n");
        return 1;
    }

    if (units <= 100)
        bill = units * 5.0f;
    else if (units <= 200)
        bill = (100 * 5.0f) + (units - 100) * 7.0f;
    else
        bill = (100 * 5.0f) + (100 * 7.0f) + (units - 200) * 10.0f;

    printf("Total bill = Rs. %.2f\\n", bill);
    return 0;
}
