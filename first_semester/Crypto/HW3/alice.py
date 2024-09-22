from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
import sys


try:
    with open('key.txt', 'rb') as f:
        key = f.read()
except FileNotFoundError:
    print("Error: 'key.txt' not found. Please generate the key first.")
    sys.exit(1)


if len(key) != 16:
    print("Error: Key must be 128 bits (16 bytes).")
    sys.exit(1)


# Prompt for the 18-byte message
message = input("Enter an 18-byte message: ").encode('utf-8')

if len(message) != 18:
    print(f"Error: Message must be exactly 18 bytes (you entered {len(message)} bytes).")
    sys.exit(1)


# Generate a random 16-byte IV
iv = get_random_bytes(16)

# Pad the message to a multiple of AES block size (16 bytes)
padded_message = pad(message, AES.block_size)

# Create AES cipher in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)

# Encrypt the message
ciphertext = cipher.encrypt(padded_message)


# Write the IV and ciphertext to 'ctext'
with open('ctext', 'wb') as f:
    f.write(iv + ciphertext)

print("Message encrypted and saved to 'ctext'.")
