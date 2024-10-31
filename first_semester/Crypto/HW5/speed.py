# time.py

import sys
import time
from alice import generate_key, generate_rsa_keys, hmac_sign_message, rsa_sign_message
from bob import hmac_verify_message, rsa_verify_message
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA

def measure_hmac_performance(message):
    # Generate a 16-byte key
    key = get_random_bytes(16)
    
    # Measure HMAC generation time over 100 iterations
    start_time = time.time()
    for _ in range(100):
        hmac_sign_message(key, message)
    hmac_generation_time = (time.time() - start_time) / 100
    
    # Generate HMAC once to get the HMAC value for verification
    hmac_value = hmac_sign_message(key, message)
    
    # Measure HMAC verification time over 100 iterations
    start_time = time.time()
    for _ in range(100):
        hmac_verify_message(key, message, hmac_value)
    hmac_verification_time = (time.time() - start_time) / 100
    
    return hmac_generation_time, hmac_verification_time

def measure_rsa_performance(message):
    # Generate RSA keys (2048 bits)
    generate_rsa_keys()
    
    with open('private_key.txt', 'rb') as f:
        private_key = RSA.import_key(f.read())
    with open('public_key.txt', 'rb') as f:
        public_key = RSA.import_key(f.read())
    
    # Measure RSA signature generation time over 100 iterations
    start_time = time.time()
    for _ in range(100):
        rsa_sign_message(private_key, message)
    signature_generation_time = (time.time() - start_time) / 100
    
    # Generate signature once to get the signature for verification
    signature = rsa_sign_message(private_key, message)
    
    # Measure RSA signature verification time over 100 iterations
    start_time = time.time()
    for _ in range(100):
        rsa_verify_message(public_key, message, signature)
    signature_verification_time = (time.time() - start_time) / 100
    
    return signature_generation_time, signature_verification_time

def main():
    message = input("Enter the message to be signed (must be 7 bytes): ").encode('utf-8')
    
    if len(message) != 7:
        print(f"Error: Message must be exactly 7 bytes (you entered {len(message)} bytes).")
        sys.exit(1)
    
    print("\n100 Average Itteration HMAC Performance:")
    hmac_gen_time, hmac_ver_time = measure_hmac_performance(message)
    print(f"Generation Time: {hmac_gen_time:.6f}s, Verification Time: {hmac_ver_time:.6f}s")
    
    print("\n100 Average Itteration RSA Signature Performance:")
    rsa_gen_time, rsa_ver_time = measure_rsa_performance(message)
    print(f"Generation Time: {rsa_gen_time:.6f}s, Verification Time: {rsa_ver_time:.6f}s")

if __name__ == '__main__':
    main()
