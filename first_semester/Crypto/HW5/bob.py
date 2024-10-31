# bob.py
import hmac
import hashlib
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

def hmac_verify_message(key, message_bytes, hmac_value):
    h = hmac.new(key, message_bytes, hashlib.sha256)
    computed_hmac = h.digest()
    return hmac.compare_digest(computed_hmac, hmac_value)

def rsa_verify_message(public_key, message_bytes, signature):
    h = SHA256.new(message_bytes)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def hmac_verify():
    with open('keyfile', 'rb') as f:
        k = f.read()

    try:
        with open('mactext', 'r') as f:
            lines = f.read().split('\n')
            if len(lines) < 2:
                print("Error: 'mactext' does not contain both message and HMAC.")
                sys.exit(1)
            m = lines[0]
            hmac_value = bytes.fromhex(lines[1])
    except FileNotFoundError:
        print("File 'mactext' not found.")
        sys.exit(1)

    m_bytes = m.encode('utf-8')
    if hmac_verify_message(k, m_bytes, hmac_value):
        print("Verification succeeds.")
    else:
        print("Verification fails.")

def rsa_verify():
    # Load public key
    try:
        with open('public_key.txt', 'rb') as f:
            public_key = RSA.import_key(f.read())
    except FileNotFoundError:
        print("Public key file not found. Please ensure 'public_key.txt' is available.")
        sys.exit(1)

    try:
        with open('sigtext', 'rb') as f:
            content = f.read().split(b'\n', 1)
            if len(content) < 2:
                print("Error: 'sigtext' does not contain both message and signature.")
                sys.exit(1)
            m_bytes = content[0]
            signature = content[1]
    except FileNotFoundError:
        print("File 'sigtext' not found.")
        sys.exit(1)

    if rsa_verify_message(public_key, m_bytes, signature):
        print("Verification succeeds.")
    else:
        print("Verification fails.")

# Main execution starts here
if __name__ == "__main__":
    # Read the user's selection
    method = input("Select method (HMAC/RSA): ").strip().upper()

    if method == 'HMAC':
        hmac_verify()
    elif method == 'RSA':
        rsa_verify()
    else:
        print("Invalid method selected.")
        sys.exit(1)



