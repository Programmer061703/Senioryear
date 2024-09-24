
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import sys

def generate_rsa_keys():
    # Generate a 2048-bit RSA key pair
    key = RSA.generate(2048)
    
    # Export Bob's private key and save it to 'bob_private.pem'
    private_key = key.export_key()
    with open('bob_private.txt', 'wb') as f:
        f.write(private_key)
    
    # Export Bob's public key and save it to 'bob_public.pem'
    public_key = key.publickey().export_key()
    with open('bob_public.txt', 'wb') as f:
        f.write(public_key)
    
    print("Bob's RSA key pair generated.")

def rsa_encrypt(message, public_key_file):
    # Read Bob's public key from the given file
    try:
        with open(public_key_file, 'rb') as f:
            public_key = RSA.import_key(f.read())
    except FileNotFoundError:
        print(f"Error: '{public_key_file}' not found.")
        sys.exit(1)
    
    # Encrypt the message using Bob's public key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    ciphertext = cipher_rsa.encrypt(message)
    return ciphertext

def aes_encrypt(message, key):
    # Generate a random 16-byte IV
    iv = get_random_bytes(16)
    
    # Pad the message to a multiple of AES block size (16 bytes)
    padded_message = pad(message, AES.block_size)
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Encrypt the message
    ciphertext = cipher.encrypt(padded_message)
    
    # Return IV and ciphertext
    return iv + ciphertext


def main():
    encryption_method = input("Enter encryption method (RSA or AES): ").upper()
    message = input("Enter the message to be encrypted, must be 18 bytes: ").encode()

def main():
    # Ask the user to choose the encryption method
    encryption_method = input("Choose encryption method (AES/RSA): ").strip().upper()
    
    # Prompt for the 18-byte message
    message = input("Enter an 18-byte message: ").encode('utf-8')
    
    if len(message) != 18:
        print(f"Error: Message must be exactly 18 bytes (you entered {len(message)} bytes).")
        sys.exit(1)
    
    if encryption_method == 'AES':
        # Read the shared key from 'key.txt'
        try:
            with open('key.txt', 'rb') as f:
                key = f.read()
        except FileNotFoundError:
            print("Error: 'key.txt' not found. Please generate the key first.")
            sys.exit(1)
    
        if len(key) != 16:
            print("Error: Key must be 128 bits (16 bytes).")
            sys.exit(1)
        
        # Encrypt the message using AES
        ciphertext = aes_encrypt(message, key)
        
        # Write the method identifier and ciphertext to 'ctext'
        with open('ctext', 'wb') as f:
            f.write(b'AES' + ciphertext)
        
        print("Message encrypted using AES and saved to 'ctext'.")
    
    elif encryption_method == 'RSA':
        # Generate Bob's RSA key pair
        generate_rsa_keys()
        
        # Encrypt the message using Bob's public key
        ciphertext = rsa_encrypt(message, 'bob_public.pem')
        
        # Write the method identifier and ciphertext to 'ctext'
        with open('ctext', 'wb') as f:
            f.write(b'RSA' + ciphertext)
        
        print("Message encrypted using RSA and saved to 'ctext'.")
    
    else:
        print("Error: Invalid encryption method selected.")
        sys.exit(1)
    
if __name__ == '__main__':
    main()