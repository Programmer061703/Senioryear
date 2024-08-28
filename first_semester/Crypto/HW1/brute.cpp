#include <iostream>
#include <string> 
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

// Function to load words from a dictionary file into a vector
vector<string> load_words_from_file(const string& filename) {
    vector<string> words;
    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "Error: Could not open the file " << filename << endl;
        return words;
    }

    string word;
    while (file >> word) {
        words.push_back(word);
    }

    file.close();
    return words;
}

// Function to decrypt a text using Caesar cipher
string ceaser_decrypt(const string& text, int shift) {
    string final_text = "";

    for (int i = 0; i < text.length(); i++) {
        char temp = text[i];
        if (isupper(temp)) {
            final_text += char(int(temp - shift - 65 + 26) % 26 + 65);
        }
        else if (islower(temp)) {
            final_text += char(int(temp - shift - 97 + 26) % 26 + 97);
        }
        else {
            final_text += temp;
        }
    }

    return final_text;
}

// Function to split a string into individual words
vector<string> split_string(const string& str) {
    vector<string> words;
    stringstream ss(str);
    string word;

    while (ss >> word) {
        words.push_back(word);
    }

    return words;
}

// Function to compare decrypted message words with dictionary words
bool compare_input_to_words(const vector<string>& words_vector, const string& input_string) {
    vector<string> input_words = split_string(input_string);

    // Check if any word from the decrypted message is present in the dictionary
    for (const auto& word : input_words) {
        if (find(words_vector.begin(), words_vector.end(), word) != words_vector.end()) {
            return true;
        }
    }

    return false;
}

int main(int argc, char* argv[]) {
    // Ensure the correct number of arguments
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <encrypted_text> <dictionary_file>\n" << "encrypted_text must be encapsulated in quotes for program to work"<<endl;
        return 1;
    }


    string encrypted_text = argv[1];
    string dictionary_filename = argv[2];

  
    vector<string> dictionary = load_words_from_file(dictionary_filename);

    // Try all possible Caesar cipher shifts (1 to 25)
    for (int i = 1; i <= 25; i++) {
        string decrypted_msg = ceaser_decrypt(encrypted_text, i);
        cout << "Trying shift " << i << ": " << decrypted_msg << endl;

        if (compare_input_to_words(dictionary, decrypted_msg)) {
            cout << "Possible match found with shift " << i << ": " << decrypted_msg << endl;
            break; 
        }
    }

    return 0;
}
