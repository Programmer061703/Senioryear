#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>
#include <time.h>

#define MAX_USERNAME 50
#define HASH_LENGTH 65
#define PASSWORD_LENGTH 50
#define CHARSET "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%^&*"

// Function to compute the SHA-256 hash
void compute_sha256(const char *str, char *output) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char *)str, strlen(str), hash);

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(output + (i * 2), "%02x", hash[i]);
    }
    output[64] = '\0'; // Null-terminate the string
}

// Recursive function to generate password combinations
int generate_combinations(int pos, char *current, int max_length, const char *charset, int charset_len, char *target_hash, char *found_password) {
    if (pos == max_length) {
        current[pos] = '\0'; // Null-terminate the password
        char hash_output[HASH_LENGTH];
        compute_sha256(current, hash_output);

        if (strcmp(hash_output, target_hash) == 0) {
            strcpy(found_password, current);
            return 1; // Password found
        }
        return 0;
    }

    for (int i = 0; i < charset_len; i++) {
        current[pos] = charset[i];
        if (generate_combinations(pos + 1, current, max_length, charset, charset_len, target_hash, found_password)) {
            return 1;
        }
    }

    return 0;
}

int main() {
    char filename[] = "hashes.txt";
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        return 1;
    }

    char username[MAX_USERNAME];
    char target_hash[HASH_LENGTH];
    char found_password[PASSWORD_LENGTH];
    int password_length;
    printf("Enter the password length N: ");
    scanf("%d", &password_length);

    const char *charset = CHARSET;
    int charset_len = strlen(charset);
    char current[PASSWORD_LENGTH];

    clock_t start_time = clock();

    printf("Starting unsalted dictionary attack...\n");
    while (fscanf(file, "[%[^,],%[^]]]\n", username, target_hash) != EOF) {
        printf("\nCracking password for user: %s\n", username);

        if (generate_combinations(0, current, password_length, charset, charset_len, target_hash, found_password)) {
            printf("Password for %s: %s\n", username, found_password);
        } else {
            printf("Password for %s not found.\n", username);
        }
    }

    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("\nTime taken: %.2f seconds\n", elapsed_time);

    fclose(file);
    return 0;
}
