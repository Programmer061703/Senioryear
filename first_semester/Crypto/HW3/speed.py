# time.py

import sys
import time
from alice import aes_encrypt, rsa_encrypt, generate_rsa_keys
from bob import aes_decrypt, rsa_decrypt
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA

def measure_aes_performance(key_size, message):
    message = b"hi khoi"  # 7-byte message
    key = get_random_bytes(key_size // 8)
    
    # Measure AES encryption time
    start_time = time.time()
    for _ in range(100):
        aes_encrypt(message, key)
    encryption_time = (time.time() - start_time) / 100
    
    # Encrypt once to get ciphertext for decryption measurement
    ciphertext = aes_encrypt(message, key)
    
    # Measure AES decryption time
    start_time = time.time()
    for _ in range(100):
        aes_decrypt(ciphertext, key)
    decryption_time = (time.time() - start_time) / 100
    
    return encryption_time, decryption_time

def measure_rsa_performance(key_size, message):
    message = b"hi khoi"  # 7-byte message
    generate_rsa_keys(key_size)
    
    with open('bob_public.txt', 'rb') as f:
        public_key = RSA.import_key(f.read())
    
    # Measure RSA encryption time
    start_time = time.time()
    for _ in range(100):
        rsa_encrypt(message, 'bob_public.txt')
    encryption_time = (time.time() - start_time) / 100
    
    # Encrypt once to get ciphertext for decryption measurement
    ciphertext = rsa_encrypt(message, 'bob_public.txt')
    
    # Measure RSA decryption time
    start_time = time.time()
    for _ in range(100):
        rsa_decrypt(ciphertext, 'bob_private.txt')
    decryption_time = (time.time() - start_time) / 100
    
    return encryption_time, decryption_time

def main():
    message = input("Enter the message to be encrypted, must be 7 bytes: ").encode('utf-8')
    
    if len(message) != 18:
        print(f"Error: Message must be exactly 7 bytes (you entered {len(message)} bytes).")
        sys.exit(1)    
    print("AES Performance:")
    
    for key_size in [128, 192, 256]:
        enc_time, dec_time = measure_aes_performance(key_size, message)
        print(f"AES-{key_size} Encryption Time: {enc_time:.6f}s, Decryption Time: {dec_time:.6f}s")
    
    print("\nRSA Performance:")
    for key_size in [1024, 2048, 4096]:
        enc_time, dec_time = measure_rsa_performance(key_size, message)
        print(f"RSA-{key_size} Encryption Time: {enc_time:.6f}s, Decryption Time: {dec_time:.6f}s")

if __name__ == '__main__':
    main()
