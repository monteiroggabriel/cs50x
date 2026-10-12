#include <cs50.h>
#include <stdio.h>

void draw_pyramid(int height);

int main(void)
{
    int height = 0;
    while (height <= 0)
    {
        height = get_int("Height: ");
    }

    draw_pyramid(height);
}

void draw_pyramid(int height)
{
    for (int i = 1; i <= height; i++)
    {
        // Spaces
        for (int j = 0; j < height - i; j++)
        {
            printf(" ");
        }

        // Bricks
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}
