#include <stdio.h>
#include <stdlib.h>

static int marker;

void retrieve(unsigned int *p) {
    marker = *p; 
}

void set_num(void) {
    static unsigned int num = 13;
    unsigned int *p;
    p = &num;
    //printf("%d", *p);
    retrieve(p);
}

int main(void) {
    set_num();
    printf("%d", marker);
    return 0;
}
