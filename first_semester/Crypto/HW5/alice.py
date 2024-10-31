# alice.py
import hmac
import hashlib
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import os

def generate_key():
    # Generate a 16-byte shared secret key
    k = os.urandom(16)
    # Write the key to 'keyfile'
    with open('keyfile', 'wb') as f:
        f.write(k)
def hash_message(m_bytes):
    """Computes the SHA-256 hash of the message."""
    h = SHA256.new(m_bytes)
    return h.digest()

def generate_rsa_keys():
    # Generate RSA private key (2048-bit)
    key = RSA.generate(2048)
    # Extract private and public keys
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    # Save private key to 'private_key.txt'
    with open('private_key.txt', 'wb') as f:
        f.write(private_key)
    # Save public key to 'public_key.txt'
    with open('public_key.txt', 'wb') as f:
        f.write(public_key)

def hmac_sign_message(key, message_bytes):
    # Generate HMAC
    h = hmac.new(key, message_bytes, hashlib.sha256)
    return h.digest()

def rsa_sign_message(private_key, message_bytes):
    # Create a SHA-256 hash of the message
    h = SHA256.new(message_bytes)
    # Sign the hash with the private key
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def hmac_sign():
    generate_key()
    # HMAC implementation
    with open('keyfile', 'rb') as f:
        k = f.read()

    m = input("Enter an 18-byte message: ")
    m_bytes = m.encode('utf-8')

    if len(m_bytes) != 18:
        print("Error: Message must be exactly 18 bytes.")
        sys.exit(1)

    hmac_value = hmac_sign_message(k, m_bytes).hex()

    with open('mactext', 'w') as f:
        f.write(m + '\n' + hmac_value)

    print("HMAC generated and written to 'mactext'.")

def rsa_sign():
    generate_rsa_keys()
    # Load private key
    try:
        with open('private_key.txt', 'rb') as f:
            private_key = RSA.import_key(f.read())
    except FileNotFoundError:
        print("Private key file not found. Please generate RSA keys first.")
        sys.exit(1)

    m = input("Enter an 18-byte message: ")
    m_bytes = m.encode('utf-8')

    if len(m_bytes) != 18:
        print("Error: Message must be exactly 18 bytes.")
        sys.exit(1)

    signature = rsa_sign_message(private_key, m_bytes)

    # Write message and signature to 'sigtext'
    with open('sigtext', 'wb') as f:
        f.write(m_bytes + b'\n' + signature)

    print("Signature generated and written to 'sigtext'.")

# Main execution starts here
if __name__ == "__main__":
    # Read the user's selection
    method = input("Select method (HMAC/RSA): ").strip().upper()

    if method == 'HMAC':
        hmac_sign()
    elif method == 'RSA':
        rsa_sign()
    else:
        print("Invalid method selected.")
        sys.exit(1)
