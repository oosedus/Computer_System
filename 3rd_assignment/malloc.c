#include <stdio.h>
#include <stdlib.h>


struct rec{
    int i;
    float PI;
    char A;
};

int main(void){
    struct rec * ptr_one;
    
    ptr_one = malloc(sizeof(struct rec));   
    printf("-------------------------\n");
    printf("Memory is allocated at %p\n", ptr_one);
    printf("-------------------------\n");
   
   
    ptr_one->i = 10;
    ptr_one->PI = 3.14;
    ptr_one->A = 'a';
    
    
    printf("First value: %d\n", ptr_one->i);
    printf("Second value: %f\n", ptr_one->PI);
    printf("Third value: %c\n", ptr_one->A);
    
    
    free(ptr_one);
    printf("-------------------------\n");
    printf("Memory is deallocated at %p\n", ptr_one);
    printf("-------------------------\n");
    
    return 0;
}
