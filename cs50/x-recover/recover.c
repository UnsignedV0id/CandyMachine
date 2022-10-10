#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>


typedef uint8_t BYTE;



int main(int argc, char *argv[])
{
    //checks if everything is ok to run
    if (argc < 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    
    FILE *corrupted = fopen(argv[1], "r");
    
    if (corrupted == NULL)
    {
        printf("fopen returned null");
        return 2;
    }
    
    //variables for recover process
    FILE *recoveredImg = NULL;
    BYTE cFile[511];
    bool isWriting ;
    int imgcount = 0;
    char imgName[8] = "000.jpg";
    
    
    while (fread(cFile, 512, 1, corrupted))
    {
        for (int i = 0; i < 512; i++)
        {
            if (cFile[i] == 0xff && cFile[i + 1] == 0xd8 && cFile[i + 2] == 0xff)
            {
                if (cFile[i + 3] > 223 && cFile[i + 3] < 240)
                {
                    
                    
                    if (isWriting)
                    {
                        imgcount++;
                        sprintf(imgName, "%03i.jpg", imgcount);
                    }
                    isWriting = true;
                    recoveredImg = fopen(imgName, "w");
                }
            }
            
            if (isWriting == true)
            {
                fwrite(&cFile[i], 1, 1, recoveredImg);
            }
            
        }
    }
    
}
