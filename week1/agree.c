#include <cs50.h>
#include <cs50.c>

int main(void)
{
    char c = get_char("Do you agree? ");

    if (c == 'Y' || c == 'y')
    {
        printf("Agreed.\n");
    }
    else
    {
        printf("Not agreed.\n");
    }
}
