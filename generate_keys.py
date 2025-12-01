from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

print("Ì¥ê Generating RSA 4096-bit key pair...")
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('student_private.pem', 'wb') as f:
    f.write(private_pem)

public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open('student_public.pem', 'wb') as f:
    f.write(public_pem)

print("‚úÖ Keys generated successfully!")
print("   - student_private.pem")
print("   - student_public.pem")
