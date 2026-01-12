import subprocess
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import json
import sys

def get_commit_hash():
    """Get the current commit hash from git"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not get commit hash. Make sure you're in a git repository.")
        return None

def sign_and_encrypt_commit_hash(commit_hash):
    """Sign the commit hash using RSA-PSS with SHA-256 and encrypt with instructor's public key"""
    try:
        # Read the student's private key
        with open('student_private.pem', 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=None)
        
        # Sign the commit hash using RSA-PSS with SHA-256
        # CRITICAL: Sign the ASCII bytes of the hash string
        signature = private_key.sign(
            commit_hash.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Read the instructor's public key
        with open('instructor_public.pem', 'rb') as f:
            instructor_public_key = serialization.load_pem_public_key(f.read(), backend=None)
        
        # Encrypt the signature with instructor's public key using OAEP
        encrypted_signature = instructor_public_key.encrypt(
            signature,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Encode encrypted signature as base64 and ensure single line
        encoded_signature = base64.b64encode(encrypted_signature).decode('utf-8').replace('\n', '').strip()
        return encoded_signature
    except FileNotFoundError as e:
        print(f"Error: {e} not found")
        return None
    except Exception as e:
        print(f"Error signing and encrypting commit hash: {e}")
        return None

def main():
    print("[*] Generating submission proof...")
    
    # Get commit hash
    commit_hash = get_commit_hash()
    if not commit_hash:
        return False
    
    print(f"[+] Current commit hash: {commit_hash}")
    
    # Sign and encrypt
    encrypted_signature = sign_and_encrypt_commit_hash(commit_hash)
    if not encrypted_signature:
        return False
    
    print(f"[+] Signature generated.")
    
    # Read other files
    try:
        with open('student_public.pem', 'r') as f:
            student_public_key = f.read().replace('\r\n', '\n')
            # Ensure proper PEM formatting
        
        with open('encrypted_seed.txt', 'r') as f:
            encrypted_seed = f.read().strip().replace('\n', '')
    except Exception as e:
        print(f"Error reading files: {e}")
        return False

    print("=" * 70)
    print("SUBMISSION DATA")
    print("=" * 70)
    
    print("1. GitHub Repository URL:")
    print(" https://github.com/MadhavaKandala/pki-2fa-microservice")
    print()
    
    print("2. Commit Hash:")
    print(f" {commit_hash}")
    print()
    
    print("3. Encrypted Commit Signature:")
    print(f" {encrypted_signature}")
    print()
    
    print("4. Student Public Key:")
    print(student_public_key)
    print()
    
    print("5. Encrypted Seed:")
    print(encrypted_seed)
    print()
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
