#include <stdio.h>

void print_row(int width);

int main(void)
{
    const int n = 3;
    print_row(n);
}

void print_row(int width)
{
    for (int i = 0; i < width; i++)
    {
        printf("#");
    }
    printf("\n");
}
