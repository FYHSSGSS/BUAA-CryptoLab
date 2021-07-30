#include<bits/stdc++.h>
using namespace std;
#define mem(a,b) memset(a,b,sizeof(a))
typedef long long LL;
typedef pair<int,int> PII;
#define X first
#define Y second
inline LL read()
{
	LL x=0,f=1;char c=getchar();
	while(!isdigit(c)){if(c=='-')f=-1;c=getchar();}
	while(isdigit(c)){x=x*10+c-'0';c=getchar();}
	return x*f;
}
inline void write(unsigned int x)//rapidly write
{ 
	if(x>9)write(x/10);
	putchar(x%10+'0');
}
const int maxN=140000000;
unsigned int prime[210000000];
LL n,len;
bitset<65400> vis[65400];//using a bitset to save space
string change(int x)//change an integer to a string
{
	if(x==0)return "";
	return change(x/10)+(char)(x%10+'0');
}	
int main()
{
	n=read();
	for(unsigned int i=2;i<=n;i++)
	{
		if(!vis[i/65400][i%65400])prime[++len]=i;//record the prime number to this array 
        for(LL j=1;j<=len && (LL)i*(LL)prime[j]<=n;j++)//use the prime who is less than i to sieve other numbers
		{
			vis[(LL)i*(LL)prime[j]/65400][(LL)i*(LL)prime[j]%65400]=1;
			if(i%prime[j]==0)break;//i*prime[j] have sieved before,no need to sieve again
		} 
	}
	printf("%lld\n",len);
	string pre_name="prime",suf_name=".txt";
	int file_num=10;//print 10 txt
	for(int i=0;i<file_num;i++)
	{
		string name=pre_name+change(i+1)+suf_name;
		char p[20];	
		strcpy(p,name.c_str());
		freopen(p,"w",stdout);
		for(LL j=(len/(file_num-1))*(LL)i+1;j<=min(len,(len/(file_num-1))*(LL)(i+1));j++)write(prime[j]),putchar(' ');
	}
	return 0;
}
/*
4275117753
4220000000
*/


