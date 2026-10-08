/*
Question / Aim:
Write a program to find the grade of a Class 12th student using
if-else-if statements, based on marks in five subjects.
*/
#include <stdio.h>

int main(void) {
    char name[50];
    float a, b, c, d, e, avg;

    printf("Enter name: ");
    scanf("%49s", name);
    printf("Enter marks in five subjects: ");
    scanf("%f %f %f %f %f", &a, &b, &c, &d, &e);

    avg = (a + b + c + d + e) / 5.0f;

    printf("Name: %s\\n", name);
    printf("Average: %.2f\\n", avg);

    if (avg >= 90)
        printf("Grade A\\n");
    else if (avg >= 80)
        printf("Grade B\\n");
    else if (avg >= 70)
        printf("Grade C\\n");
    else
        printf("Grade D\\n");

    return 0;
}
