# alice.py

from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import sys

def generate_rsa_keys(key_size=2048):
    # Generate an RSA key pair with a specified key size
    key = RSA.generate(key_size)
    
    # Export Bob's private key and save it to 'bob_private.txt'
    private_key = key.export_key()
    with open('bob_private.txt', 'wb') as f:
        f.write(private_key)
    
    # Export Bob's public key and save it to 'bob_public.txt'
    public_key = key.publickey().export_key()
    with open('bob_public.txt', 'wb') as f:
        f.write(public_key)
    
    print(f"Bob's {key_size}-bit RSA key pair generated.")

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
    
    # Return IV and ciphertext concatenated
    return iv + ciphertext

def main():
    encryption_method = input("Enter encryption method (RSA or AES): ").upper()
    message = input("Enter the message to be encrypted, must be 18 bytes: ").encode('utf-8')
    
    if len(message) != 18:
        print(f"Error: Message must be exactly 18 bytes (you entered {len(message)} bytes).")
        sys.exit(1)
    
    if encryption_method == 'AES':
        key_size = int(input("Enter AES key size (128, 192, or 256): "))
        
        if key_size not in [128, 192, 256]:
            print("Error: Invalid AES key size.")
            sys.exit(1)
        
        key = get_random_bytes(key_size // 8)
        
        # Save the AES key to a file
        with open('key.txt', 'wb') as f:
            f.write(key)
        
        ciphertext = aes_encrypt(message, key)
        
        # Write the method identifier and ciphertext to 'ctext'
        with open('ctext', 'wb') as f:
            f.write(b'AES' + ciphertext)
        
        print(f"Message encrypted using AES-{key_size} and saved to 'ctext'.")
    
    elif encryption_method == 'RSA':
        key_size = int(input("Enter RSA key size (1024, 2048, or 4096): "))
        
        if key_size not in [1024, 2048, 4096]:
            print("Error: Invalid RSA key size.")
            sys.exit(1)
        
        generate_rsa_keys(key_size)
        
        ciphertext = rsa_encrypt(message, 'bob_public.txt')
        
        # Write the method identifier and ciphertext to 'ctext'
        with open('ctext', 'wb') as f:
            f.write(b'RSA' + ciphertext)
        
        print(f"Message encrypted using RSA-{key_size} and saved to 'ctext'.")
    
    else:
        print("Error: Invalid encryption method selected.")
        sys.exit(1)
    
if __name__ == '__main__':
    main()
