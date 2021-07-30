#include <stdio.h>
#include <string.h>
#include <time.h>
#include "sm4.h"

int main() {
    unsigned char p[17] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32,
                           0x10, '\0'};
    unsigned char k[17] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32,
                           0x10, '\0'};

    if (strlen(k) != 16 || strlen(p) > 16) {
        printf("length of key is error!");
        return 0;
    }

    u32 *ek = NULL;
    ek = expandKey((u32 *) k);
    u32 *sm4_c = (u32 *)p;
    clock_t t = clock();
    for (int i = 0; i < 1000000; i++) {
        sm4_c = sm4_enc(sm4_c, ek);
    }
    printf("1000000 times:%.20f s\n", (double) (clock() - t) / CLOCKS_PER_SEC);
    printf("%u %u %u %u\n", *(sm4_c), *(sm4_c + 1), *(sm4_c + 2), *(sm4_c+ 3));
    unsigned char *c = (unsigned char *) sm4_c;


//    u32 *sm4_p = sm4_dec((u32 *) c, (u32 *) k);
//    unsigned char *de_p = (unsigned char *) sm4_p;

    return 0;
}
/*
*/