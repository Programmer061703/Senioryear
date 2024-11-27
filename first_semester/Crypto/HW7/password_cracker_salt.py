import itertools
import hashlib
import time

def sha256_with_salt(password, salt):
    """Hash a password with SHA-256 using a 32-bit salt."""
    salted_password = password.encode() + salt.encode()  # Append salt to the password
    return hashlib.sha256(salted_password).hexdigest()

def main():
    # Prompt the user to enter the password length N
    N = int(input("Enter the password length N: "))

    # Read in the file containing [username, salt, SHA256(password||salt)]
    # Assuming the file is named 'hashes_salted.txt'
    # Each line in the file is in the format: [username,salt,hash]
    user_data = {}
    with open('part2.txt', 'r') as f:
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
            if len(parts) != 3:
                print(f"Invalid line format: {line}")
                continue
            username = parts[0].strip()
            salt = parts[1].strip()
            hash_value = parts[2].strip()
            user_data[username] = {'salt': salt, 'hash': hash_value}

    # Define the character set
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%^&*'

    # Start the timer
    start_time = time.time()

    # Initialize a dictionary to store found passwords
    found_passwords = {}

    total_users = len(user_data)
    user_count = 0

    for username, data in user_data.items():
        user_count += 1
        print(f"\nCracking password for user {user_count}/{total_users}: {username}")
        salt = data['salt']
        stored_hash = data['hash']
        password_found = False
        combinations_tried = 0

        # Generate all possible combinations
        total_combinations = len(characters) ** N
        print(f"Total combinations to try: {total_combinations}")

        for pwd_tuple in itertools.product(characters, repeat=N):
            pwd = ''.join(pwd_tuple)
            # Hash the password with the user's salt
            hash_pwd = sha256_with_salt(pwd, salt)
            combinations_tried += 1
            # Check if the hash matches the stored hash
            if hash_pwd == stored_hash:
                found_passwords[username] = pwd
                print(f"Found password for {username}: {pwd}")
                password_found = True
                break
            # Optional: print progress every 100,000 combinations
            if combinations_tried % 100000 == 0:
                print(f"{combinations_tried} combinations tried for {username}...")

        if not password_found:
            print(f"Password not found for {username} within given parameters.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTime taken: {elapsed_time} seconds")

    # Output the found passwords
    print("\nCracked Passwords:")
    for username, password in found_passwords.items():
        print(f"Username: {username}, Password: {password}")

if __name__ == '__main__':
    main()
