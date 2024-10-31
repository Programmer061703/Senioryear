# generate_key.py
import os

def generate_key():
    # Generate a 16-byte shared secret key
    k = os.urandom(16)

    # Write the key to 'keyfile'
    with open('keyfile', 'wb') as f:
        f.write(k)
