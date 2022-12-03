#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(void){
    int A[4][4], T[4][4], S[4][4];
    int i, j;
    
    for(i=0; i<4; i++){
        for(j=0; j<4; j++){
            printf("input [%d][%d]: ",i,j);
            scanf("%d", &A[i][j]);   
        }
    }
    printf("Original matrix: \n");
    for(i=0; i<4; i++){
        for(j=0; j<4; j++){
            printf("%2d ",A[i][j]);
        }
        printf("\n");
    }
    for(i=0; i<4; i++){
        for(j=0; j<4; j++){
            T[i][j] = A[j][i];
        }
    }
    printf("Transposed matrix: \n");
    for(i=0; i<4; i++){
        for(j=0; j<4; j++){
            printf("%2d ",T[i][j]);
        }
        printf("\n");
    }
    for(i=0; i<4; i++){
        for(j=0; j<4; j++){
            S[i][j] = A[i][j]+T[i][j];
        }
    }
    printf("Sum of two matrices: \n");
    for(i=0; i<4; i++){
        for(j=0; j<4; j++){
            printf("%2d ",S[i][j]);
        }
        printf("\n");
    }
    return 0;
}
