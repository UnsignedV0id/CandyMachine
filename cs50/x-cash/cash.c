#include <stdio.h>
#include<cs50.h>
#include <math.h>

int main(void)
{
    
   float owedfloat;
   int change = 0;
    
    do
   {
       owedfloat = get_float("Change owed:");
   }
   while(owedfloat < 0 );

   
   owedfloat *= 100 ;
   owedfloat= round(owedfloat);
    

   int owed = owedfloat;
    

   if(owed > 24)
   {
       
       change = owed / 25;
       owed = owed % 25; 
       
       
   }
   if(owed > 9 )
   {
       
       change += owed /10 ;
       
       owed = owed %10; 
   }
   if(owed > 4 )
   {
       change += owed / 5 ;
       owed = owed % 5; 
   }
   if(owed < 5 )
   {
       change += owed;
   }
       
   

   printf("%i",change);

}

