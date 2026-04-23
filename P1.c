#include<stdio.h>
int main(){
	FILE *f=fopen("input.txt","r");
	char ch;
	int c=0,w=0,l=0;
	while((ch=fgetc(f))!=EOF){
		c++;
		if(ch==' '||ch=='\n')
			w++;
		if(ch=='\n')
			l++;
	}
	printf("%d %d %d",c,w+1,l+1);
}