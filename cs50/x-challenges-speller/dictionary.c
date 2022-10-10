// Implements a dictionary's functionality
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 260003;

// Hash table
node *hashDict[N];


//Number of loaded words
int wordsLoaded = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char wordLower[LENGTH + 1];
    strcpy(wordLower, word);
    //converts word to lower for comparisson
    for (int i = 0; wordLower[i]; i++)
    {
        wordLower[i] = tolower(wordLower[i]);
    }

    int checkPos = hash(wordLower);
    node *cursor = hashDict[checkPos]  ;

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;

    }

    //case insensitive
    //strcasecmp compare str buit is case insens


    return false;
}

// Djb2 hash function
unsigned int hash(const char *word)
{

        unsigned int hashNum = 5381;
        int c;
        while ((c = *word++))
            hashNum = ((hashNum << 5) + hashNum) + c; /* hash * 33 + c */
        return hashNum % N;

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *dictionaryFile = fopen(dictionary, "r");
    char word[LENGTH + 1];

    if (dictionaryFile != NULL)
    {
        while (fscanf(dictionaryFile, "%s", word) != EOF)
        {
            wordsLoaded++ ;
            node *currentWord = malloc(sizeof(node));

            if (currentWord != NULL)
            {
                strcpy(currentWord->word, word);
                //memset(currentWord, 0, sizeof(node));
                currentWord->next = NULL;

                //call hash and instert into hash table
                int pos = hash(word);




                if (hashDict[pos] == NULL)
                {
                    hashDict[pos] = currentWord;

                }
                else
                {
                    currentWord -> next = hashDict[pos] -> next;
                    hashDict[pos] -> next = currentWord;
                }

            }



        }
        fclose(dictionaryFile);
        return true;
    }
    fclose(dictionaryFile);
    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (wordsLoaded)
    {
        return wordsLoaded;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *target ;
    node *current;

    // TODO
    for (int i = 0; i < N ; i++)
    {

        if (hashDict[i] != NULL)
        {
            current = hashDict[i];
            target = current;
            //printf("word:%s , pointer:%p ,adress itselft: ", hashDict[i]->word,hashDict[i]->next);
            //printf("%p",hashDict[i]);
            //printf("\n\n\n");
            while (current -> next != NULL)
            {
                current = current -> next;
                free(target);
                target = current;
            }
            if (current -> next == NULL)
            {
                free(current);
            }
        }

    }

    return true;
}
