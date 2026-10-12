// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table (26 letters * 27 possibilities for the second position + 1)
const unsigned int N = 703;

// Hash table
node *table[N];

// Word count tracker
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word
    unsigned int index = hash(word);

    // Traverse the linked list at the corresponding bucket
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        // Case-insensitive comparison
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash based on the first two letters of the word
    // First letter: a-z (0-25), apostrophe (26)
    // Second letter (if exists): a-z (0-25), apostrophe (26)
    unsigned int first = (tolower(word[0]) == '\'') ? 26 : tolower(word[0]) - 'a';

    if (word[1] == '\0')
    {
        return first;
    }

    unsigned int second = (tolower(word[1]) == '\'') ? 26 : tolower(word[1]) - 'a';

    return first * 27 + second;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    // Buffer to read each word
    char buffer[LENGTH + 1];

    // Read each word from the dictionary
    while (fscanf(source, "%s", buffer) != EOF)
    {
        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(source);
            return false;
        }

        // Copy word into the node
        strcpy(new_node->word, buffer);

        // Hash the word
        unsigned int index = hash(buffer);

        // Insert node at the beginning of the linked list
        new_node->next = table[index];
        table[index] = new_node;

        // Increment word count
        word_count++;
    }

    // Close the file
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate over each bucket in the hash table
    for (unsigned int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            // Save the next node before freeing the current one
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
