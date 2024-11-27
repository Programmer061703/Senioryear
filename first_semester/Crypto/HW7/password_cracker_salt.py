import itertools
import hashlib
import time

def sha256_with_salt(password, salt):
    """Hash a password with SHA-256 using a 32-bit salt."""
    salted_password = password.encode() + salt.encode()  
    return hashlib.sha256(salted_password).hexdigest()

def main():
    # Prompt the user to enter the password length N
    N = int(input("Enter the password length N: "))


    user_data = {}
    with open('part2.txt', 'r') as f:
        for line in f:
  
            line = line.strip()

            if not line:
                continue

            line = line.strip('[]')

            parts = line.split(',')
            if len(parts) != 3:
                print(f"Invalid line format: {line}")
                continue
            username = parts[0].strip()
            salt = parts[1].strip()
            hash_value = parts[2].strip()
            user_data[username] = {'salt': salt, 'hash': hash_value}


    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%^&*'
    start_time = time.time()
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


        total_combinations = len(characters) ** N
        print(f"Total combinations to try: {total_combinations}")

        for pwd_tuple in itertools.product(characters, repeat=N):
            pwd = ''.join(pwd_tuple)

            hash_pwd = sha256_with_salt(pwd, salt)
            combinations_tried += 1

            if hash_pwd == stored_hash:
                found_passwords[username] = pwd
                print(f"Found password for {username}: {pwd}")
                password_found = True
                break
            # Prints the number of combinations tried every 100,000 combinations
            if combinations_tried % 100000 == 0:
                print(f"{combinations_tried} combinations tried for {username}...")

        if not password_found:
            print(f"Password not found for {username} within given parameters.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTime taken: {elapsed_time} seconds")

    print("\nCracked Passwords:")
    for username, password in found_passwords.items():
        print(f"Username: {username}, Password: {password}")

if __name__ == '__main__':
    main()
