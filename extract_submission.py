
import re

def extract():
    content = ""
    try:
        with open('submission_data.txt', 'r', encoding='utf-16') as f:
            content = f.read()
    except:
        with open('submission_data.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Extract fields
    md = "# Submission Data\n\n"
    
    commit_match = re.search(r"Commit Hash:\s+([a-f0-9]+)", content)
    if commit_match:
        md += f"**Commit Hash:** `{commit_match.group(1)}`\n\n"
        
    sig_match = re.search(r"Encrypted Commit Signature:\s+([a-zA-Z0-9+/=]+)", content)
    if sig_match:
        md += f"**Encrypted Commit Signature:**\n```\n{sig_match.group(1)}\n```\n\n"
        
    seed_match = re.search(r"Encrypted Seed:\s+([a-zA-Z0-9+/=]+)", content)
    if seed_match:
        md += f"**Encrypted Seed:**\n```\n{seed_match.group(1)}\n```\n\n"
        
    # Public Key
    if "BEGIN PUBLIC KEY" in content:
        start = content.find("-----BEGIN PUBLIC KEY-----")
        end = content.find("-----END PUBLIC KEY-----") + len("-----END PUBLIC KEY-----")
        key = content[start:end]
        md += f"**Student Public Key:**\n```\n{key}\n```\n\n"
    
    with open('final_submission.md', 'w', encoding='utf-8') as f:
        f.write(md)
    print("final_submission.md created")

if __name__ == "__main__":
    extract()
