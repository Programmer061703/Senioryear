#include <iostream>
using namespace std; 



string ceaser_encrypt(string text, int shift){
    string final_text = "";

    for (int i = 0; i < text.length(); i++){
        char temp = text[i];
        if (isupper(temp)){
            final_text += char(int(text[i] + shift - 65) % 26 + 65);

        }
        else if(islower(temp)){
            final_text += char(int(text[i] + shift - 97) % 26 + 97);
            
        }
        else{
            final_text += temp;
        }
    }

    return final_text;

}

string ceaser_decrypt(string text, int shift){
    string final_text = "";

    for (int i = 0; i < text.length(); i++){
        char temp = text[i];
        if (isupper(temp)){
            final_text += char(int(text[i] - shift - 65 + 26) % 26 + 65);

        }
        else if (islower(temp)){
            final_text += char(int(text[i] - shift - 97 + 26) % 26 + 97);
            
        }
        else {
            final_text += temp;
        }
    }

    return final_text;

}


int main() {
    string input = "";
    int shift;
    char mode_select;


    cout << "Select Mode (1: Encrypt, 2: Decrypt): ";
    cin >> mode_select;


    cin.ignore();

    switch (mode_select) {
        case '1': // Encrypt mode
            cout << "Input String: ";
            getline(cin, input);

            cout << "Input Shift value: ";
            cin >> shift;

            cout << "\nEncrypted String: " << ceaser_encrypt(input, shift) << endl;
            break;

        case '2': // Decrypt mode
            cout << "Input String: ";
            getline(cin, input);

            cout << "Input Shift value: ";
            cin >> shift;

            cout << "\nDecrypted String: " << ceaser_decrypt(input, shift) << endl;
            break;

        default:
            cout << "Bad Input, Try again" << endl;
            break;
    }

    return 0;
}

