#include<stdio.h>
#include<ctype.h>
#include<string.h>
char productions[10][10];
int n;
int main()
{
	int i;
	char ch;
	printf("Enter number of productions:\n");
	scanf("%d",&n);
	for(i=0;i<n;i++)
	{
		scanf("%s",productions[i]);
	}
	printf("Enter non-terminal:\n");
	scanf(" %c",&ch);
	printf("\nFIRST(%c) = { ",ch);
	for(i=0;i<n;i++)
	{
		if(productions[i][0]==ch)
		{
			char firstChar=productions[i][3];
			printf("%c ",firstChar);
		}
	}
	printf("}\n");
	return 0;
}