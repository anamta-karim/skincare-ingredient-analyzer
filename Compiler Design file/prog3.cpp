#include<iostream>
#include<cctype>
#include<string>
using namespace std;
string keywords[]={"int","float","if","else","while","return","for","char","double","void"};
bool isKeyword(string str){
	for(int i=0;i<10;i++){
		if(str==keywords[i]){
			return true;
		}
	}
	return false;
}
bool isOperator(char ch){
	if(ch=='+'||ch=='-'||ch=='*'||ch=='/'||ch=='='||ch=='%'||ch=='<'||ch=='>'){
		return true;
	}
	return false;
}
int main(){
	string input;
	cout<<"Enter code: ";
	getline(cin,input);
	int i=0;
	while(i<input.length()){
		if(input[i]==' '||input[i]=='\t'||input[i]=='\n'){
			i++;
			continue;
		}
		if(input[i]=='/'&&input[i+1]=='/'){
			break;
		}
		if(isalpha(input[i])||input[i]=='_'){
			string word="";
			while(i<input.length()&&(isalnum(input[i])||input[i]=='_')){
				word+=input[i];
				i++;
			}
			if(isKeyword(word)){
				cout<<word<<" : Keyword"<<endl;
			}
			else{
				cout<<word<<" : Identifier"<<endl;
			}
		}
		else if(isdigit(input[i])){
			string num="";
			while(i<input.length()&&isdigit(input[i])){
				num+=input[i];
				i++;
			}
			cout<<num<<" : Constant"<<endl;
		}
		else if(isOperator(input[i])){
			cout<<input[i]<<" : Operator"<<endl;
			i++;
		}
		else{
			i++;
		}
	}
	return 0;
}