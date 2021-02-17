#include <stdio.h>
#include <stdlib.h>

union u{
    struct {
        int type;
    } n;
    struct {
        int type;
        int intnode;
    } ni;
    struct {
        int type;
        double doublenode;
    } nf;
};

int main(void) {
    
    union u my_union;
    union u *up;

    up = &my_union;
    my_union.nf.type = 1;
    my_union.nf.doublenode = 3.14;
    printf("%d\n", my_union.nf.type);
    printf("%f\n", my_union.nf.doublenode);
    printf("%d\n", up->nf.type);
    printf("%f\n", up->nf.doublenode);
    
    return 0;
}
