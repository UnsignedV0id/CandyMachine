#include "helpers.h"
#include <math.h>
#include <stdio.h>



/*typedef struct
{
    BYTE  rgbtBlue;
    BYTE  rgbtGreen;
    BYTE  rgbtRed;
} __attribute__((__packed__))
RGBTRIPLE;
*/

// Convert image to grayscale DONE
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width ; w++)
        {
            int average = round((image[h][w].rgbtRed + image[h][w].rgbtBlue + image[h][w].rgbtGreen) / 3.0);

            //gets pointer for each RGB value

            BYTE* rp = &image[h][w].rgbtBlue;
            BYTE* bp = &image[h][w].rgbtRed;
            BYTE* gp = &image[h][w].rgbtGreen;

            //apply new value

            *rp = average;
            *bp = average;
            *gp = average;

        }
    }
    return;
}

// Convert image to sepia DONE
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width ; w++)
        {

            int sepiaRed = round(0.393 * image[h][w].rgbtRed + 0.769 * image[h][w].rgbtGreen + 0.189 * image[h][w].rgbtBlue);
            int sepiaGreen = round(0.349 * image[h][w].rgbtRed + 0.686 * image[h][w].rgbtGreen + 0.168 * image[h][w].rgbtBlue);
            int sepiaBlue = round(0.272 * image[h][w].rgbtRed + 0.534 * image[h][w].rgbtGreen + 0.131 * image[h][w].rgbtBlue);

            //cap values if greater then 255 or less then 0
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            else if (sepiaRed < 0)
            {
                sepiaRed = 0;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            else if (sepiaBlue < 0)
            {
                sepiaBlue = 0;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            else if (sepiaGreen < 0)
            {
                sepiaGreen = 0;
            }



            //gets pointer for each RGB value

            BYTE *rp = &image[h][w].rgbtRed;
            BYTE *bp = &image[h][w].rgbtBlue;
            BYTE *gp = &image[h][w].rgbtGreen;

            //apply new value

            *rp = sepiaRed;
            *bp = sepiaBlue;
            *gp = sepiaGreen;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE reflectedRow[width];

    for (int h = 0; h < height; h++)
    {

        //gets half of array to use in odd width images
        int half = floor(width  / 2.0) ;
        // creates mirrored row
        for (int w = width; w > 0 ; w--)
        {

            if (width % 2 == 0)
            {
                reflectedRow[width - w] = image[h][w - 1] ;
            }
            else
            {
                if (w != half + 1)
                {
                    reflectedRow[width - w] = image[h][w - 1];
                }
                else
                {
                    reflectedRow[half] = image[h][half];
                }
            }

        }



        //apply mirrored row
        for (int rP = 0; rP < width; rP++)
        {
            //creates pointer to row and then apply mirror effect
            RGBTRIPLE *row = &image[h][rP];
            *row = reflectedRow[rP];
        }

    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE* pixelP;
    RGBTRIPLE blurredImage[height][width];
    int avgB, avgR, avgG;

    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < width ; w++)
        {

            if (h == 0 && w == 0)
            {
                avgB = round((image[h][w + 1].rgbtBlue + image[h + 1][w].rgbtBlue + image[h + 1 ][w + 1].rgbtBlue + image[h][w].rgbtBlue)/4.0);
                avgR = round((image[h][w + 1].rgbtRed + image[h + 1][w].rgbtRed + image[h + 1 ][w + 1].rgbtRed + image[h][w].rgbtRed)/4.0);
                avgG = round((image[h][w + 1].rgbtGreen + image[h + 1][w].rgbtGreen + image[h + 1 ][w + 1].rgbtGreen + image[h][w].rgbtGreen)/4.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;
            }
            else if (h == 0 && w == width - 1)
            {
                avgB = round((image[h][w - 1].rgbtBlue + image[h + 1][w - 1].rgbtBlue + image[h + 1][w].rgbtBlue + image[h][w].rgbtBlue)/4.0);
                avgR = round((image[h][w - 1].rgbtRed + image[h + 1][w - 1].rgbtRed + image[h + 1][w].rgbtRed + image[h][w].rgbtRed)/4.0);
                avgG = round((image[h][w - 1].rgbtGreen + image[h + 1][w - 1].rgbtGreen + image[h + 1][w].rgbtGreen + image[h][w].rgbtGreen)/4.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;

            }
            else if (h == height - 1 && w == 0)
            {
                avgB = round((image[h - 1][w].rgbtBlue + image[h - 1][w + 1].rgbtBlue + image[h][w + 1].rgbtBlue + image[h][w].rgbtBlue)/4.0);
                avgR = round((image[h - 1][w].rgbtRed + image[h - 1][w + 1].rgbtRed + image[h][w + 1].rgbtRed + image[h][w].rgbtRed)/4.0);
                avgG = round((image[h - 1][w].rgbtGreen + image[h - 1][w + 1].rgbtGreen + image[h][w + 1].rgbtGreen + image[h][w].rgbtGreen)/4.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;
            }
            else if (h == height - 1 && w == width - 1)
            {

                avgB = round((image[h - 1][w].rgbtBlue + image[h - 1][w - 1].rgbtBlue + image[h][w - 1].rgbtBlue + image[h][w].rgbtBlue)/4.0);
                avgR = round((image[h - 1][w].rgbtRed + image[h - 1][w - 1].rgbtRed + image[h][w - 1].rgbtRed + image[h][w].rgbtRed)/4.0);
                avgG = round((image[h - 1][w].rgbtGreen + image[h - 1][w - 1].rgbtGreen + image[h][w - 1].rgbtGreen + image[h][w].rgbtGreen)/4.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;
            }
            else if (h == 0)
            {
                avgB = round((image[h][w - 1].rgbtBlue + image[h][w + 1].rgbtBlue + image[h + 1][w - 1].rgbtBlue + image[h + 1][w].rgbtBlue +
                image[h + 1][w + 1].rgbtBlue + image[h][w].rgbtBlue)/6.0);
                avgR = round((image[h][w - 1].rgbtRed + image[h][w + 1].rgbtRed + image[h + 1][w - 1].rgbtRed + image[h + 1][w].rgbtRed +
                image[h + 1][w + 1].rgbtRed + image[h][w].rgbtRed)/6.0);
                avgG = round((image[h][w - 1].rgbtGreen + image[h][w + 1].rgbtGreen + image[h + 1][w - 1].rgbtGreen + image[h + 1][w].rgbtGreen +
                image[h + 1][w + 1].rgbtGreen + image[h][w].rgbtGreen)/6.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;
            }
            else if (h == height - 1)
            {
                
                avgB = round((image[h][w - 1].rgbtBlue + image[h][w + 1].rgbtBlue + image[h - 1][w].rgbtBlue + image[h - 1][w - 1].rgbtBlue +
                image[h - 1][w + 1].rgbtBlue + image[h][w].rgbtBlue)/6.0);
                avgR = round((image[h][w - 1].rgbtRed + image[h][w + 1].rgbtRed + image[h - 1][w - 1].rgbtRed + image[h - 1][w].rgbtRed +
                image[h - 1][w + 1].rgbtRed + image[h][w].rgbtRed)/6.0);
                avgG = round((image[h][w - 1].rgbtGreen + image[h][w + 1].rgbtGreen + image[h - 1][w - 1].rgbtGreen + image[h - 1][w].rgbtGreen +
                image[h - 1][w + 1].rgbtGreen + image[h][w].rgbtGreen)/6.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;
            }
            else if (w == 0)
            {

                avgB = round((image[h - 1][w].rgbtBlue + image[h - 1][w + 1].rgbtBlue + image[h][w + 1].rgbtBlue + image[h + 1][w].rgbtBlue +
                image[h + 1][w + 1].rgbtBlue + image[h][w].rgbtBlue)/6.0);
                avgR = round((image[h - 1][w].rgbtRed + image[h - 1][w + 1].rgbtRed + image[h][w + 1].rgbtRed + image[h + 1][w].rgbtRed +
                image[h + 1][w + 1].rgbtRed + image[h][w].rgbtRed)/6.0);
                avgG = round((image[h - 1][w].rgbtGreen + image[h - 1][w + 1].rgbtGreen + image[h][w + 1].rgbtGreen + image[h + 1][w].rgbtGreen +
                image[h + 1][w + 1].rgbtGreen + image[h][w].rgbtGreen)/6.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;
            }
            else if (w == width -1)
            {

                avgB = round((image[h - 1][w].rgbtBlue + image[h - 1][w - 1].rgbtBlue + image[h][w - 1].rgbtBlue + image[h + 1][w].rgbtBlue +
                image[h + 1][w - 1].rgbtBlue + image[h][w].rgbtBlue)/6.0);
                avgR = round((image[h - 1][w].rgbtRed + image[h - 1][w - 1].rgbtRed + image[h][w - 1].rgbtRed + image[h + 1][w].rgbtRed +
                image[h + 1][w - 1].rgbtRed + image[h][w].rgbtRed)/6.0);
                avgG = round((image[h - 1][w].rgbtGreen + image[h - 1][w - 1].rgbtGreen + image[h][w - 1].rgbtGreen + image[h + 1][w].rgbtGreen +
                image[h + 1][w - 1].rgbtGreen + image[h][w].rgbtGreen)/6.0);
                blurredImage[h][w].rgbtBlue = avgB;
                blurredImage[h][w].rgbtRed = avgR;
                blurredImage[h][w].rgbtGreen = avgG;

            }
            else
            {

            avgB = round((image[h + 1][w - 1].rgbtBlue + image[h + 1][w].rgbtBlue + image[h + 1][w + 1].rgbtBlue + image[h][w - 1].rgbtBlue + image[h][w + 1].rgbtBlue +
            image[h - 1][w - 1].rgbtBlue + image[h - 1][w].rgbtBlue + image[h - 1][w + 1].rgbtBlue + image[h][w].rgbtBlue) / 9.0);

            avgR = round((image[h + 1][w - 1].rgbtRed + image[h + 1][w].rgbtRed + image[h + 1][w + 1].rgbtRed + image[h][w - 1].rgbtRed + image[h][w + 1].rgbtRed +
            image[h - 1][w - 1].rgbtRed + image[h - 1][w].rgbtRed + image[h - 1][w + 1].rgbtRed + image[h][w].rgbtRed) / 9.0);

            avgG = round((image[h + 1][w - 1].rgbtGreen + image[h + 1][w].rgbtGreen + image[h + 1][w + 1].rgbtGreen + image[h][w - 1].rgbtGreen + image[h][w + 1].rgbtGreen +
            image[h - 1][w - 1].rgbtGreen + image[h - 1][w].rgbtGreen + image[h - 1][w + 1].rgbtGreen + image[h][w].rgbtGreen) / 9.0);


            blurredImage[h][w].rgbtBlue = avgB;
            blurredImage[h][w].rgbtRed = avgR;
            blurredImage[h][w].rgbtGreen = avgG;

            }
        }

    }

    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < width ; w++)
        {
            //pointer to pixel
            pixelP = &image[h][w];

            *pixelP = blurredImage[h][w];
        }

    }

    return;
}
