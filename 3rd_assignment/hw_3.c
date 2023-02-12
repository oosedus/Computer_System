#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(void){
    char * str1;
    char str2[100];
    
    
    str1 = (char*)malloc(sizeof(str2));

    
    strcpy(str1, "21102044");

    
    printf("str1: %s, address: %p\n", str1, str1);

    
    strcpy(str2, "21102044");

    
    printf("str2: %s, address: %p\n", str2, str2);

    
    free(str1);
    
    return 0;
}
