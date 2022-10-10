#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(void)
{

    int words = 1, letters = 0, sentences = 0;

    string text = get_string("Text: ");

    for (int c = 0 ; text[c] != '\0' ; c++)
    {
        if (text[c] >= 65 && text[c] <= 122)
        {
            
            if (text[c] < 91 || text[c] > 96)
            {
                letters++;
            }
            
        }
        else if (text [c]== 32)
        {
            words++;
        }
        else if (text[c] == 33 || text[c] == 46 || text[c] == 63)
        {
            sentences++;
        }
        
    }
   
    printf("words:%i, sentences:%i, letters:%i ",words, sentences, letters);
   
    //implementing the formula index = 0.0588 * L - 0.296 * S - 15.8
    float L = (float)letters * 100 / words;
    float S = (float)sentences * 100 / words;
    
    float index = 0.0588 * L - 0.296 * S - 15.8;
   
    printf("Index :%f , L : %f , S: %f", index, L, S);
   
    index = round(index);
    
    if(index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int)index);
    }
}