from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys():
    print("Generating RSA 4096-bit key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # Save private key
    with open("student_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save public key
    public_key = private_key.public_key()
    with open("student_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("Keys generated successfully: student_private.pem, student_public.pem")

if __name__ == "__main__":
    generate_keys()
