//File name: /Users/argos/github/135/calc.cpp
/*
Author: Pedro Vizzarro Vallejos

Description: this program takes a string from a text file with basic addition/subtraction operations and gives the rresult. Takes only positive integers as input.

Usage: ./calc < <filename>
Example string: "5-3+15-11"
Note: It can accept spaces between operations and handles up to 100 entries.
*/
#include <iostream>
#include <string>
using namespace std;

int parse_num(string s, bool add)
{
    int num = stoi(s);
    if (!add){
        num *= -1;
    }
    return num;
}

int main()
{
    int total = 0;
    const int SIZE = 100;
    int values[SIZE];
    int counter = 0;
    string s = "";
    char c;
    bool add = true;

    while(cin >> c){
        if(c != '+' && c != '-'){
            s += c;
        } 
        values[counter] = parse_num(s, add);
        if(c == '+'){
            add = true;
            counter++;
            s = "";
        }else if(c == '-'){
            add = false;
            counter++;
            s = "";   
        } 
    }
    values[counter] = parse_num(s, add);
    for (int i=0; i<counter+1; i++){
        total += values[i];
    }

    cout << total;

    return 0;
}
