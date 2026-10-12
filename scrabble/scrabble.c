#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Array of points for each letter
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string s);

int main(void)
{
    string p1 = get_string("Player 1: ");
    string p2 = get_string("Player 2: ");

    int score1 = compute_score(p1);
    int score2 = compute_score(p2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string s)
{
    int score = 0;
    for (int i = 0; i < strlen(s); i++)
    {
        if (isalpha(s[i]))
        {
            score += POINTS[tolower(s[i]) - 'a'];
        }
    }
    return score;
}
