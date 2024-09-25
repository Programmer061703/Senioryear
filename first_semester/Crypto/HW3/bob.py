from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import unpad
from Cryptodome.PublicKey import RSA
import sys

def rsa_decrypt(ciphertext, private_key_file):
    # Read Bob's private key from the given file
    try:
        with open(private_key_file, 'rb') as f:
            private_key = RSA.import_key(f.read())
    except FileNotFoundError:
        print(f"Error: '{private_key_file}' not found.")
        sys.exit(1)
    
    # Decrypt the message using Bob's private key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    try:
        message = cipher_rsa.decrypt(ciphertext)
    except ValueError:
        print("Error: Decryption failed. Incorrect key or corrupted ciphertext.")
        sys.exit(1)
    
    return message

def aes_decrypt(data, key):

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
    
    return message


def main():
    # Read the ciphertext from 'ctext'
    try:
        with open('ctext', 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print("Error: 'ctext' not found. Ensure Alice has encrypted the message.")
        sys.exit(1)
    
    # Determine the encryption method from the first 3 bytes
    encryption_method = data[:3].decode('utf-8')
    ciphertext = data[3:]  # Remove the method identifier from the data
    
    if encryption_method == 'AES':
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
        
        # Decrypt the message using AES
        message = aes_decrypt(ciphertext, key)
        
        # Print the original message
        print("Decrypted message:", message.decode('utf-8'))
    
    elif encryption_method == 'RSA':
        # Decrypt the message using Bob's private key
        message = rsa_decrypt(ciphertext, 'bob_private.txt')
        
        # Print the original message
        print("Decrypted message:", message.decode('utf-8'))
    
    else:
        print("Error: Unknown encryption method.")
        sys.exit(1)

if __name__ == '__main__':
    main()
