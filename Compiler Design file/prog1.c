#include<stdio.h>
int main(){
    char ch;
    int c=0,w=0,l=0;
    while((ch=getchar())!=EOF){
        c++;
        if(ch==' '||ch=='\n') w++;
        if(ch=='\n') l++;
    }
    printf("Characters: %d\nWords: %d\nLines: %d\n",c,w+1,l+1);
}