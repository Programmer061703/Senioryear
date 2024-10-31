# generate_rsa_keys.py
from Cryptodome.PublicKey import RSA

def generate_rsa_keys():
    # Generate RSA private key (2048-bit)
    key = RSA.generate(2048)

    # Extract private and public keys
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save private key to 'private_key.pem'
    with open('private_key.txt', 'wb') as f:
        f.write(private_key)

    # Save public key to 'public_key.pem'
    with open('public_key.txt', 'wb') as f:
        f.write(public_key)
