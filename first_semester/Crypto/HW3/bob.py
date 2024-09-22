from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import sys

# Read the shared key from 'key.txt'
try:
    with open('key.txt', 'rb') as f:
        key = f.read()
except FileNotFoundError:
    print("Error: 'key.txt' not found.")
    sys.exit(1)

if len(key) != 16:
    print("Error: Key must be 128 bits (16 bytes).")
    sys.exit(1)

# Read the IV and ciphertext from 'ctext'
try:
    with open('ctext', 'rb') as f:
        data = f.read()
except FileNotFoundError:
    print("Error: 'ctext' not found. Ensure Alice has encrypted the message.")
    sys.exit(1)

if len(data) <= 16:
    print("Error: The data is too short to contain both IV and ciphertext.")
    sys.exit(1)

# Extract IV and ciphertext
iv = data[:16]
ciphertext = data[16:]

# Create AES cipher in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt and unpad the message
try:
    padded_message = cipher.decrypt(ciphertext)
    message = unpad(padded_message, AES.block_size)
except (ValueError, KeyError):
    print("Error: Decryption failed. Incorrect key or corrupted ciphertext.")
    sys.exit(1)

# Print the original message
print("Decrypted message:", message.decode('utf-8'))
