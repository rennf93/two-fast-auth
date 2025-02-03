---
title: Getting Started with Two-Fast-Auth
description: First steps guide for implementing Two-Fast-Auth in your FastAPI application
keywords: two-fast-auth tutorial, fastapi 2fa middleware, fastapi 2fa setup
---

# Getting Started with 2FA

1. **Install Package**
```bash
pip install two-fast-auth
```

2. **Add Middleware**
```python
# With encryption (Optional, Recommended)
from two_fast_auth import TwoFactorMiddleware

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    encryption_key="your-fernent-key-here",
    excluded_paths=["/setup-2fa"]
)

# Without encryption
from two_fast_auth import TwoFactorMiddleware

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    encryption_key="your-fernent-key-here",
    excluded_paths=["/setup-2fa"]
)
```

3. **Create Setup Endpoint (Encrypted)**
```python
from two_fast_auth import TwoFactorAuth

@app.post("/setup-2fa")
async def setup_2fa(user: User = Depends(current_user)):
    tfa = TwoFactorAuth()
    encrypted_secret = TwoFactorAuth.encrypt_secret(
        tfa.secret,
        encryption_key="your-key-here"  # From middleware config
    )
    return {
        "qr_code": tfa.generate_qr_code(user.email),
        "secret": encrypted_secret  # Store this in DB
    }
```

4. **Implement Verification (Encrypted)**
```python
@app.post("/verify-2fa")
async def verify_2fa(code: str, user: User = Depends(current_user)):
    # Secret is automatically decrypted by middleware
    if not TwoFactorAuth(user.two_fa_secret).verify_code(code):
        raise HTTPException(400, "Invalid code")
    return {"status": "verified"}
```

5. **Manual Secret Handling (Optional)**
```python
# Encrypt existing secret
encrypted = TwoFactorAuth.encrypt_secret(
    "BASE32SECRET",
    encryption_key="your-key"
)

# Decrypt secret
original = TwoFactorAuth.decrypt_secret(
    encrypted,
    encryption_key="your-key"
)
```

## Next Steps
- Explore [encryption example application](example_app_encryption.md)
- See [full encryption implementation](example_implementation_encryption.md)
