#include<iostream>
#include<cctype>
using namespace std;
bool isIdentifier(string str)
{
	if(!(isalpha(str[0])||str[0]=='_'))
	{
		return false;
	}
	for(int i=1;i<str.length();i++)
	{
		if(!(isalnum(str[i])||str[i]=='_'))
		{
			return false;
		}
	}
	return true;
}
bool isConstant(string str)
{
	for(int i=0;i<str.length();i++)
	{
		if(!isdigit(str[i]))
		{
			return false;
		}
	}
	return true;
}
bool isOperator(string str)
{
	if(str=="+"||str=="-"||str=="*"||str=="/"||str=="="||str=="%")
	{
		return true;
	}
	return false;
}
int main()
{
	string str;
	cout<<"Enter string: ";
	cin>>str;
	if(isIdentifier(str))
	{
		cout<<"Identifier";
	}
	else if(isConstant(str))
	{
		cout<<"Constant";
	}
	else if(isOperator(str))
	{
		cout<<"Operator";
	}
	else
	{
		cout<<"Invalid";
	}
	return 0;
}