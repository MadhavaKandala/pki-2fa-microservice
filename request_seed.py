import requests
import json

def request_seed():
    url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
    student_id = "23P31A1205"
    repo_url = "https://github.com/MadhavaKandala/pki-2fa-microservice"
    
    print("Reading public key...")
    with open("student_public.pem", "r") as f:
        public_key_content = f.read()

    # Format check: Ensure it has newlines 
    # The API likely wants the PEM string as-is but JSON escaped.
    # Python's json.dumps handles the escaping.
    
    payload = {
        "student_id": student_id,
        "github_repo_url": repo_url,
        "public_key": public_key_content
    }

    print(f"Requesting seed for {student_id}...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "encrypted_seed" in data:
                enc_seed = data["encrypted_seed"]
                with open("encrypted_seed.txt", "w") as f:
                    f.write(enc_seed)
                print("SUCCESS: Encrypted seed saved to encrypted_seed.txt")
            else:
                print("ERROR: 'encrypted_seed' not in response.")
                print(data)
        else:
            print("ERROR: Request failed.")
            print(response.text)
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    request_seed()
