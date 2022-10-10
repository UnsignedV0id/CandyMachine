#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int H ;

    do
    {
        H = get_int("Enter Height: ");
    }
    while(H < 1 || H > 8);

    int i;
    int l;
    int space;
    for(i = 1 ; i <= H; i++)
    {
       

       

        for( space = H - i; space > 0 ; space--)
        {
            
            printf(" ");
        }
        for(l = i; l > 0 ; l--)
        {
            printf("#");
        }
        printf("  ");
         for(l = i; l > 0 ; l--)
        {
            printf("#");
        }
        printf("\n");

    }

}
