/*
Question / Aim:
Write a program to input a student's name and marks in five subjects,
then calculate and display the total and average marks.
*/
#include <stdio.h>

int main() {
    char name[50];
    float sub1, sub2, sub3, sub4, sub5, total, avg;

    printf("Enter your name: ");
    scanf("%49s", name);

    printf("Enter marks in Subject 1: ");
    scanf("%f", &sub1);
    printf("Enter marks in Subject 2: ");
    scanf("%f", &sub2);
    printf("Enter marks in Subject 3: ");
    scanf("%f", &sub3);
    printf("Enter marks in Subject 4: ");
    scanf("%f", &sub4);
    printf("Enter marks in Subject 5: ");
    scanf("%f", &sub5);

    total = sub1 + sub2 + sub3 + sub4 + sub5;
    avg = total / 5.0f;

    printf("\\nName: %s\\n", name);
    printf("Total Marks: %.2f\\n", total);
    printf("Average Marks: %.2f\\n", avg);

    return 0;
}
