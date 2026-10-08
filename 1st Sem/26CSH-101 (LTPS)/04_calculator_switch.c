/*
Question / Aim:
Write a menu-driven program to implement arithmetic operations
using a switch statement.
*/
#include <stdio.h>

int main() {
    int a, b, op;

    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);

    printf("Choose operation:\\n1. ADD\\n2. SUB\\n3. MULTIPLY\\n4. DIVIDE\\n");
    printf("Enter operation number: ");
    scanf("%d", &op);

    switch (op) {
        case 1: printf("ADD is %d\\n", a + b); break;
        case 2: printf("SUB is %d\\n", a - b); break;
        case 3: printf("MULTIPLY is %d\\n", a * b); break;
        case 4:
            if (b != 0)
                printf("DIV is %.2f\\n", (float)a / b);
            else
                printf("Division by zero is not possible.\\n");
            break;
        default: printf("Invalid operation.\\n");
    }

    return 0;
}
