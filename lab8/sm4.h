#ifndef SM4_H_
#define SM4_H_

typedef unsigned int u32;

u32 transT(u32 tin);
u32 transT_k(u32 tin);

u32* expandKey(u32 key[4]);

u32* sm4_enc(u32* p,u32* key);
u32* sm4_dec(u32* c,u32* key);

void padding(char* p);
void rev_padding(char* p);
#endif
