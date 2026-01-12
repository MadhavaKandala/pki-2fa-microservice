
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

def check_keys():
    try:
        with open('instructor_public.pem', 'rb') as f:
            key_data = f.read()
            key = serialization.load_pem_public_key(key_data)
            print(f"Instructor Key Size: {key.key_size} bits")
            
            # Message size check
            # OAEP overhead: 2 * hash_len + 2
            # SHA-256 digest size: 32 bytes
            # Overhead = 2 * 32 + 2 = 66 bytes.
            # Max message size = KeySizeBytes - 66
            max_size = (key.key_size // 8) - 66
            print(f"Max OAEP-SHA256 plaintext size: {max_size} bytes")
            
            # Signature size (for 4096 bit key) = 512 bytes.
            sig_size = 512
            print(f"Student Signature Size (4096-bit): {sig_size} bytes")
            
            if sig_size > max_size:
                print("CRITICAL: Signature is TOO LARGE to encrypt with Instructor Key using OAEP!")
            else:
                print("Encryption should work.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_keys()
