import itertools
import hashlib
import time

def main():
    # Prompt the user to enter the password length N
    N = int(input("Enter the password length N: "))

    # Read in the file containing [username, SHA256(password)]
    # Assuming the file is named 'hashes.txt'
    # Each line in the file is in the format: [username,hash]
    hashes = {}
    with open('part1.txt', 'r') as f:
        for line in f:
            # Remove any leading/trailing whitespace
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            # Remove the brackets
            line = line.strip('[]')
            # Split the line by comma
            parts = line.split(',')
            if len(parts) != 2:
                print(f"Invalid line format: {line}")
                continue
            username = parts[0].strip()
            hash_value = parts[1].strip()
            hashes[hash_value] = username

    # Define the character set
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%^&*'

    # Start the timer
    start_time = time.time()

    # Initialize a dictionary to store found passwords
    found_passwords = {}

    # Generate all possible combinations
    total_combinations = len(characters) ** N
    print(f"Total combinations to try: {total_combinations}")

    count = 0
    for pwd_tuple in itertools.product(characters, repeat=N):
        pwd = ''.join(pwd_tuple)
        # Hash the password
        hash_pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        # Check if the hash matches any stored hash
        if hash_pwd in hashes:
            username = hashes[hash_pwd]
            found_passwords[username] = pwd
            print(f"Found password for {username}: {pwd}")
            # Remove the hash from hashes to avoid duplicate checking
            del hashes[hash_pwd]
            # Check if all passwords have been found
            if not hashes:
                print("All passwords have been cracked.")
                break
        count += 1
        # Print progress every 100,000 combinations
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

