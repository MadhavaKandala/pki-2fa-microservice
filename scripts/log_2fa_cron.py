#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import pyotp
import base64
import time

# Ensure UTC is used
# The environment variable TZ=UTC should be set in Dockerfile

try:
    with open('/data/seed.txt', 'r') as f:
        seed = f.read().strip()
    
    seed_bytes = bytes.fromhex(seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    
    # Get current UTC timestamp
    # Using simple strftime on utcnow for compatibility
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # OUTPUT using stdout as per instructions
    print(f"{timestamp} - 2FA Code: {code}")
    
except Exception as e:
    # Print error to stderr so it shows up in logs but separate from valid output if needed
    print(f"Error: {e}", file=sys.stderr)
