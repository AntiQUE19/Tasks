#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <queue>

using namespace std;

struct Bounds{
	size_t start;
	size_t end;
};

struct Token{
	int index;
	char command;
	string info;
};

Bounds find_cell(const int &index, const string &s){
	Bounds bnds;
	size_t pos = 0;
	int i = 0;
	string delimiter = "\t";
	while(i < index){
		pos = s.find(delimiter, pos);
	}
	bnds.start = pos;
	pos = s.find(delimiter, pos);
	bnds.end = pos;
	
	return bnds;
};

void to_lower(const int index, string &s){
	Bounds b = find_cell(index, s); 
	for(size_t i = b.start; i < b.end + 1; i++){
		s[i] = ::tolower(s[i]);
	}
	
	return;
};

void to_upper(const int index, string &s){
	Bounds b = find_cell(index, s); 
		for(size_t i = b.start; i < b.end + 1; i++){
		s[i] = ::toupper(s[i]);
	}
	return;
};

void replace_ab(const int index, string &s, const char a, const char b){
	Bounds bnds = find_cell(index, s); 
	size_t pos = 0;
	while(pos != string::npos){
		pos = s.find(a, pos);
		if(pos > bnds.end){
			break;
		}
		s[pos] = b;
	}
	return;
};

bool parse_command(const string &s,queue<Token> &q){
	Token comm;
	string token;
	string delimiter = ":";
	size_t pos = s.find(delimiter);
	comm.index = stoi(s.substr(0, pos));
	string temp = s.substr(pos + 1, s.length());
	comm.command 	= temp[0];
	comm.info		= temp.substr(1, temp.length());
	q.push(comm);
	return true;
};

void do_action(const Token t, ifstream &fin){
	string row;	
	if(t.command == 'u'){
		while(getline(fin, row)){
			to_lower(t.index, row);
		}
	}else if(t.command == 'U'){
		while(getline(fin, row)){
			to_upper(t.index, row);
		}
	} else if(t.command == 'R'){
		while(getline(fin, row)){
			replace_ab(t.index, row, t.info[0], t.info[1]);
		}
	}else{
		cerr << "Wrong command: " << t.command << "\n";
		return;
	}
	
	cout << row << "\n";
	return;
};

int main(){
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	string name, row, command;
	queue<Token> q;
	ifstream fin;
	
	cin >> name >> ws;
	
	fin.open(name); 
	
	if(!fin.is_open()){
		cerr << "Couldn't open the file '" << name << "'" << "\n";
	}
	
	while(getline(cin, command)){
		if(!parse_command(command, q)){
			cerr << "Wrong command: " << command << "\n";
		}
	}
	
	
	while(q.size() != 0){
		do_action(q.front(), fin);
		q.pop();
	}
	fin.close();
	return 0;
}
