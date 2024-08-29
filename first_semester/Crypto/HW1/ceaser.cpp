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


int main(int argc, char* argv[]) {
    // Ensure the correct number of arguments
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " <1 or 2> <input_text(must have quotes around text)> <shift_value>\n" 
             << "\t\t1: Encrypt 2: Decrypt" << endl;
        return 1;
    }

    // Get the mode from the first argument
    char mode_select = argv[1][0];  // First character of argv[1]

    // Get the input string and shift value from the command line arguments
    string input = argv[2];
    int shift = stoi(argv[3]);

    switch (mode_select) {
        case '1': // Encrypt mode
            cout << "\nEncrypted String: " << ceaser_encrypt(input, shift) << endl;
            break;

        case '2': // Decrypt mode
            cout << "\nDecrypted String: " << ceaser_decrypt(input, shift) << endl;
            break;

        default:
            cerr << "Invalid mode selected. Use '1' for Encrypt or '2' for Decrypt." << endl;
            return 1;
    }

    return 0;
}

