import requests
import time
import json
import subprocess
import sys

BASE_URL = "http://localhost:8080"

def run_test():
    print("[-] Starting verification...")
    
    # 1. Decrypt Seed
    print("[-] Test 1: Decrypt Seed")
    try:
        with open("encrypted_seed.txt", "r") as f:
            enc_seed = f.read().strip()
        
        resp = requests.post(f"{BASE_URL}/decrypt-seed", json={"encrypted_seed": enc_seed})
        print(f"    Status: {resp.status_code}")
        print(f"    Response: {resp.text}")
        if resp.status_code != 200:
            print("    FAIL: Decrypt seed failed")
            return
    except Exception as e:
        print(f"    FAIL: {e}")
        return

    # 2. Generate 2FA
    print("[-] Test 2: Generate 2FA")
    code = ""
    try:
        resp = requests.get(f"{BASE_URL}/generate-2fa")
        print(f"    Status: {resp.status_code}")
        print(f"    Response: {resp.text}")
        if resp.status_code == 200:
            data = resp.json()
            code = data.get("code")
            print(f"    Code: {code}")
        else:
            print("    FAIL: Generate 2FA failed")
    except Exception as e:
        print(f"    FAIL: {e}")

    # 3. Verify 2FA
    print("[-] Test 3: Verify 2FA")
    if code:
        try:
            resp = requests.post(f"{BASE_URL}/verify-2fa", json={"code": code})
            print(f"    Status: {resp.status_code}")
            print(f"    Response: {resp.text}")
            if resp.status_code == 200 and resp.json().get("valid") == True:
                print("    PASS")
            else:
                print("    FAIL")
        except Exception as e:
            print(f"    FAIL: {e}")
    else:
        print("    SKIP (No code generated)")

    # 4. Cron Check
    print("[-] Test 4: Cron Job (Waiting 70s...)")
    time.sleep(70)
    try:
        # Get container ID
        res = subprocess.run(["docker", "ps", "-q", "-f", "ancestor=week2gpp-app"], capture_output=True, text=True) # Adjust image name if needed
        # Actually it's simpler to use docker-compose exec
        res = subprocess.run(["docker-compose", "exec", "-T", "app", "cat", "/cron/last_code.txt"], capture_output=True, text=True)
        print("    Cron Output:")
        print(res.stdout)
        if "2FA Code:" in res.stdout:
            print("    PASS: Cron logs found")
        else:
            print("    FAIL: No cron logs found")
            print("    Stderr:", res.stderr)
    except Exception as e:
        print(f"    FAIL: {e}")

if __name__ == "__main__":
    run_test()
