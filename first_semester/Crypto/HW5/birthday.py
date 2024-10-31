# birthday.py

import random
import string
from alice import hash_message

def H(m):
    """Custom hash function H(m) that uses the first 8 bits of SHA-256(m)."""
    sha256_hash = hash_message(m)
    # Take the first 8 bits (1 byte)
    first_byte = sha256_hash[0]
    return first_byte

def generate_random_message(length=8):
    """Generates a random message of given length."""
    letters = string.ascii_letters + string.digits + string.punctuation + ' '
    message = ''.join(random.choice(letters) for _ in range(length))
    return message.encode('utf-8')

def find_collision():
    """Generates random messages and computes their hash values using H() until a collision is found."""
    hash_table = {}
    trials = 0
    while True:
        message = generate_random_message()
        hash_value = H(message)
        trials += 1
        if hash_value in hash_table:
            # Collision found
            previous_message = hash_table[hash_value]
            if message != previous_message:
                # Ensure the messages are different
                return trials, message.decode('utf-8', errors='replace'), previous_message.decode('utf-8', errors='replace'), hash_value
        else:
            hash_table[hash_value] = message

def main():
    # Part 4(a)
    print("Part 4(a): Finding a collision for H(m)")
    trials, message1, message2, hash_value = find_collision()
    print(f"Number of messages tried before collision: {trials}")
    print(f"Message 1: {message1}")
    print(f"Message 2: {message2}")
    print(f"Hash value (first 8 bits of SHA-256): {hash_value}\n")

    # Part 4(b)
    print("Part 4(b): Calculating average number of trials over 20 iterations")
    total_trials = 0
    iterations = 20
    for _ in range(iterations):
        trials, _, _, _ = find_collision()
        total_trials += trials
    average_trials = total_trials / iterations
    print(f"Average number of trials needed to find a collision over {iterations} iterations: {average_trials:.2f}")

if __name__ == "__main__":
    main()
