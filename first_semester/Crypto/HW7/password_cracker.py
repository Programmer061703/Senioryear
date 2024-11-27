import itertools
import hashlib
import time

def main():
    # Prompt the user to enter the password length N
    N = int(input("Enter the password length N: "))


    hashes = {}
    with open('part1.txt', 'r') as f:
        for line in f:

            line = line.strip()

            if not line:
                continue
            line = line.strip('[]')
            parts = line.split(',')
            if len(parts) != 2:
                print(f"Invalid line format: {line}")
                continue
            username = parts[0].strip()
            hash_value = parts[1].strip()
            hashes[hash_value] = username

    # Define the character set
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%^&*'

    start_time = time.time()

    found_passwords = {}

    # Generate all possible combinations
    total_combinations = len(characters) ** N
    print(f"Total combinations to try: {total_combinations}")

    count = 0
    for pwd_tuple in itertools.product(characters, repeat=N):
        pwd = ''.join(pwd_tuple)
        # Hash the password
        hash_pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        if hash_pwd in hashes:
            username = hashes[hash_pwd]
            found_passwords[username] = pwd
            print(f"Found password for {username}: {pwd}")
            del hashes[hash_pwd]

            if not hashes:
                print("All passwords have been cracked.")
                break
        count += 1

        if count % 100000 == 0:
            print(f"{count} combinations tried...")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTime taken: {elapsed_time} seconds")

    # Output the found passwords
    print("\nCracked Passwords:")
    for username, password in found_passwords.items():
        print(f"Username: {username}, Password: {password}")

if __name__ == '__main__':
    main()

