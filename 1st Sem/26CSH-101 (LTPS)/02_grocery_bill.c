/*
Question / Aim:
Write a program that takes grocery bill details as input and calculates
the total amount to be paid, including 18% GST.
*/
#include <stdio.h>

int main() {
    char item[50];
    float price, quantity, amount, gst, total;

    printf("Enter item name: ");
    scanf("%49s", item);
    printf("Enter price: ");
    scanf("%f", &price);
    printf("Enter quantity: ");
    scanf("%f", &quantity);

    amount = price * quantity;
    gst = amount * 18.0f / 100.0f;
    total = amount + gst;

    printf("\\n----- Grocery Bill -----\\n");
    printf("Item: %s\\n", item);
    printf("Price: %.2f\\n", price);
    printf("Quantity: %.2f\\n", quantity);
    printf("Amount: %.2f\\n", amount);
    printf("GST (18%%): %.2f\\n", gst);
    printf("Total Amount: %.2f\\n", total);

    return 0;
}
