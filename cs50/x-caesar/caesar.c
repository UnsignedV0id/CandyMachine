#include<stdio.h>
#include<stdlib.h>
#include<cs50.h>
#include<ctype.h>

int main(int argc, string argv[])
{
    
    
    if (argc > 2  || argc <= 1)
    {
       printf("Usage: ./caesar key\n");
       return 1;
    }
    
    for (int i = 0 ; argv[1][i] != '\0' ; i++)
    
    {
        
        int c = isdigit(argv[1][i]);
        
        if(c == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        
    }
    int cText = 0;
    int key = atoi(argv[1]);
    string text = get_string("plain text: ");
    
    for (int i = 0 ; text[i] != '\0' ; i++)
    { 
        
        if ( isalpha(text[i]) )
        {
            
            if ( isupper(text[i]) )
            {
                cText = ( (text[i] - 65) + key ) % 26; 
                text[i] = (char)cText + 65;
                
            }
            else if ( islower(text[i]) )
            {
                cText = ( (text[i] - 97) + key ) % 26;
                text[i] = (char)cText + 97;
            }
            
        }
        
    }
    
    printf("ciphertext: %s\n", text);

}