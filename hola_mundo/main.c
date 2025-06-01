#include<stdio.h>

int suma(int a, int b, int c)
{
    int test = 0;
    return a + b + c + test;
}

int main()
{
    printf("Hola, mundo!\n");
    printf("La suma de 1, 2 y 3 es: %d\n", suma(1, 2, 3));
}