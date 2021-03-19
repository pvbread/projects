//File name: /Users/argos/CS/CPP/135/week7/caesar.cpp
/*
Author: Pedro Vizzarro Vallejos
Course: CSCI-135
Instructor: Prof. Tong Yi
Assignment: 6c

Description: Demonstration of encryption and decryption of caesar and vigenere ciphers. The decryptions use the encryption function calls with a reversed key.
Please note that vigenere key only accept lower case characters for now.
*/
#include <iostream>
#include <cctype>
#include <string>
using namespace std;

char shiftChar(char c, int rshift);
string encryptCaesar(string txt, int rshift);
string encryptVigenere(string txt, string key);
string decryptCaesar(string txt, int rshift);
string decryptVigenere(string txt, string key);

int main()
{
    string s, key;
    int shift;
    
    cout << "Enter plaintext: ";
    getline(cin, s);
    cout << "= Caesar =" << endl; 
    cout << "Enter shift    : " << endl;
    cin >> shift;
    string enc = encryptCaesar(s, shift);
    cout << "Ciphertext     : " << enc << endl;
    cout << "Decrypted      : " << decryptCaesar(enc, shift) << endl;
    
    cout << "= Vigenere =" << endl; 
    cout << "Enter keyword  : " << endl;
    cin >> key;
    enc = encryptVigenere(s, key);
    cout << "Ciphertext     : " << enc << endl;
    cout << "Decrypted      : " << decryptVigenere(enc, key);
    
    //cout << encryptVigenere("aaaaaaaaaa", "cake");
    //cout << decryptVigenere("cakecakeca", "cake");
    return 0;
}
char shiftChar(char c, int rshift){
    //calibrate indices
    if (!isalpha(c)){
        return c;
    }

    int a, b;

    //take care of negative shifts
    while (rshift < 0){
        rshift += 26;
    }
    if (isupper(c)){
        a = c - 65;
        b = a + rshift;
        if (b > 25) {
            b = b % 26;
        }
        b += 65;
    } else {
        a = c - 97;
        b = a + rshift;
        if (b > 25) {
            b = b % 26;
        }
        b += 97;
    }
    char idx = b;
    return idx;
}
string encryptCaesar(string txt, int rshift){
    string temp = "";

    for (int i = 0; i < txt.length(); i++){
        if (isalpha(txt[i])){
            temp += shiftChar(txt[i], rshift);
        } else {
            temp += txt[i];
        }
    }
    return temp;
}
string encryptVigenere(string txt, string key){
    int shift = 0;
    int j = 0;
    string enc = "";
    string c = "";
    for (int i = 0; i < txt.length(); i++){
        if (isalpha(txt[i])){
            //to 0-index the shifts
            shift = key[j] - 97;

            //convert char to string
            c = txt[i];
            enc += encryptCaesar(c, shift);
            //bumps key counter and resets cycle
            j = (j+1) % key.length();
        } else {
            enc += txt[i];
        }
    }

    return enc;
}
string decryptCaesar(string txt, int rshift){
    rshift = -1 * rshift;
    return encryptCaesar(txt, rshift);
}
string decryptVigenere(string txt, string key){
    string reverse = "";
    int shift = 0;
    //reverse the key
    for (int i = 0; i < key.length(); i++){
        shift = key[i] - 97;
        //reverse the shift
        shift = -1 * shift;
        if (shift){
            reverse += 123 + shift;
        } else {
            reverse += key[i];
        }
    }
    string dec = "";
    dec = encryptVigenere(txt, reverse);

    return dec;
}

