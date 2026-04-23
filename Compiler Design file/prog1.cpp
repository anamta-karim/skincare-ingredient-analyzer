#include<iostream>
#include<fstream>
using namespace std;
int main()
{
	ifstream file("input.txt");
	char ch;
	int characters=0,words=0,lines=0;
	bool inWord=false;
	if(!file)
	{
		cout<<"Error opening file";
		return 0;
	}
	while(file.get(ch))
	{
		characters++;
		if(ch==' '||ch=='\n'||ch=='\t')
		{
			if(inWord)
			{
				words++;
				inWord=false;
			}
		}
		else
		{
			inWord=true;
		}
		if(ch=='\n')
		{
			lines++;
		}
	}
	if(inWord)
	{
		words++;
	}
	cout<<"Characters: "<<characters<<endl;
	cout<<"Words: "<<words<<endl;
	cout<<"Lines: "<<lines<<endl;
	file.close();
	return 0;
}