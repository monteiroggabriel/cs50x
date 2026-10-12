#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check if program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    // Check if all characters in argv[1] are digits
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: %s key\n", argv[0]);
            return 1;
        }
    }

    // Convert argv[1] from a `string` to an `int`
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("Plaintext: ");

    // For each character in the plaintext:
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            plaintext[i] = (plaintext[i] - 'A' + key) % 26 + 'A';
        }
        else if (islower(plaintext[i]))
        {
            plaintext[i] = (plaintext[i] - 'a' + key) % 26 + 'a';
        }
    }

    printf("ciphertext: %s\n", plaintext);
    return 0;
}
