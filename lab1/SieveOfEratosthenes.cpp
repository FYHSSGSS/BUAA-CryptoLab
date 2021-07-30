#include<bits/stdc++.h>
using namespace std;
#define mem(a,b) memset(a,b,sizeof(a))
typedef long long LL;
typedef pair<int,int> PII;
#define X first
#define Y second
inline int read()
{
	int x=0,f=1;char c=getchar();
	while(!isdigit(c)){if(c=='-')f=-1;c=getchar();}
	while(isdigit(c)){x=x*10+c-'0';c=getchar();}
	return x*f;
}
const int maxn=1000010;
bool have[maxn];
int n;
int main()
{
	n=read();// rapidly read
	have[2]=0;// 2 is a prime
    for(int i=2;i*i<=n;i++)
	{
        if(have[i])continue;//if i is a composite number,we don't need to use i to sieve other numbers
        for(int j=i*i;j<=n;j+=i)have[j]=1;
    }
    int cnt=0;
    for(int i=2;i<=n;i++)if(!have[i])cnt++;// calcultaing the num of primes in range of n
	printf("%d\n",cnt);
    for(int i=2;i<=n;i++)if(!have[i])printf("%d ",i);
	return 0;
}
/*

*/


