#include <cs50.h>
#include <stdio.h>

int main(void)
{
    float x = get_float("What's x? ");
    float y = get_float("What's y? ");

    printf("%.50f\n", x / y);
}
