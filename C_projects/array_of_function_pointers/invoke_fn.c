#include <stdio.h>
#include <stdlib.h>

void msg_1(void){
    printf("Find what you love and let it kill you\n");
}

void msg_2(void){
    printf("An intellectual says a simple thing in a hard way. An artist says a hard thing in a simple way.\n");
}

void msg_3(void){
    printf("What matters most is how well you walk through the fire.\n");
}

int main(void){
    void (*fn_pointer[3])(void) = {msg_1, msg_2, msg_3};
    int choice;
    printf("Please type 1, 2, or 3 to get a message: ");
    scanf("%1d", &choice);
    choice--;
    fn_pointer[choice]();
    return 0;
}
