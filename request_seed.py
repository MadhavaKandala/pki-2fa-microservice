import requests
import json

with open('student_public.pem', 'r') as f:
    public_key = f.read()

# ‚ö†Ô∏è CHANGE THIS TO YOUR STUDENT ID FROM PARTNR
student_id = "kandala_madhava"  # Replace with YOUR student ID
github_repo_url = "https://github.com/MadhavaKandala/pki-2fa-microservice"

payload = {
    "student_id": student_id,
    "github_repo_url": github_repo_url,
    "public_key": public_key
}

print("Ì¥Ñ Requesting encrypted seed from instructor API...")
response = requests.post(
    "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/",
    json=payload,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    result = response.json()
    with open('encrypted_seed.txt', 'w') as f:
        f.write(result['encrypted_seed'])
    print("‚úÖ Encrypted seed received and saved to encrypted_seed.txt!")
else:
    print(f"‚ùå Error: {response.status_code}")
    print(response.text)
