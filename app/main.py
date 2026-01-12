from fastapi import FastAPI, HTTPException, Request
import os
import logging
from app.crypto import decrypt_seed
from app.totp import generate_totp, verify_totp, get_remaining_seconds

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(request: Request):
    """Decrypt encrypted seed and store in persistent volume"""
    try:
        data = await request.json()
        logger.info(f"Received decrypt-seed request. Keys loaded from /app/student_private.pem")
        
        # Ensure private key exists
        if not os.path.exists('/app/student_private.pem'):
            logger.error("Private key not found at /app/student_private.pem")
            # Fallback to local dir if running without docker mount mapping (though Dockerfile copys to /app)
            if os.path.exists('student_private.pem'):
                 seed = decrypt_seed(data['encrypted_seed'], 'student_private.pem')
            else:
                 raise FileNotFoundError("student_private.pem not found")
        else:
            seed = decrypt_seed(data['encrypted_seed'], '/app/student_private.pem')
        
        if len(seed) != 64 or not all(c in '0123456789abcdef' for c in seed.lower()):
            logger.error("Invalid seed format")
            raise ValueError("Invalid seed format")
        
        os.makedirs('/data', exist_ok=True)
        with open('/data/seed.txt', 'w') as f:
            f.write(seed)
        
        logger.info("Seed decrypted and saved successfully.")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Decryption failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    """Generate current 2FA code"""
    try:
        if not os.path.exists('/data/seed.txt'):
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        
        with open('/data/seed.txt', 'r') as f:
            seed = f.read().strip()
        
        code = generate_totp(seed)
        remaining = get_remaining_seconds()
        
        return {"code": code, "valid_for": remaining}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generate 2FA error: {str(e)}")
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

@app.post("/verify-2fa")
async def verify_2fa(request: Request):
    """Verify 2FA code"""
    try:
        data = await request.json()
        
        if 'code' not in data:
            raise HTTPException(status_code=400, detail="Missing code")
        
        if not os.path.exists('/data/seed.txt'):
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        
        with open('/data/seed.txt', 'r') as f:
            seed = f.read().strip()
        
        valid = verify_totp(seed, data['code'])
        return {"valid": valid}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Verify 2FA error: {str(e)}")
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
