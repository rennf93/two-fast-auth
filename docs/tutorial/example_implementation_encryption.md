---
title: Encrypted Implementation - Two-Fast-Auth
description: Secure 2FA implementation with secret encryption
keywords: encrypted 2fa implementation, secure fastapi 2fa
---

# Encryption Implementation Guide

## Full Configuration
```python
from cryptography.fernet import Fernet
from two_fast_auth import TwoFactorMiddleware, TwoFactorAuth

ENCRYPTION_KEY = Fernet.generate_key()  # Store securely in production

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_encrypted_secret,
    encryption_key=ENCRYPTION_KEY,
    excluded_paths=["/setup-2fa", "/verify-2fa"]
)

async def get_encrypted_secret(user_id: str) -> str:
    # Return encrypted secret from your database
    return await fetch_encrypted_secret(user_id)
```

## Auth Endpoints
```python
@app.post("/setup-2fa")
async def setup_2fa_endpoint(user: User = Depends(current_user)):
    tfa = TwoFactorAuth()
    encrypted_secret = TwoFactorAuth.encrypt_secret(
        tfa.secret,
        ENCRYPTION_KEY
    )
    await store_encrypted_secret(user.id, encrypted_secret)
    return {
        "qr_code": tfa.generate_qr_code(user.email),
        "encrypted_secret": encrypted_secret
    }

@app.post("/verify-2fa")
async def verify_2fa_endpoint(code: str, user: User = Depends(current_user)):
    encrypted_secret = await get_encrypted_secret(user.id)
    secret = TwoFactorAuth.decrypt_secret(encrypted_secret, ENCRYPTION_KEY)

    if not TwoFactorAuth(secret).verify_code(code):
        raise HTTPException(401, "Invalid 2FA code")

    return {"status": "verified"}
```

## Protected Endpoint
```python
@app.get("/protected-data")
async def protected_data(user: User = Depends(current_active_user)):
    return {"data": "Sensitive encrypted data"}
```

## Testing Workflow
1. Generate encryption key: `Fernet.generate_key()`
2. Start server with encryption middleware
3. Setup 2FA to get encrypted secret
4. Verify requests automatically decrypt secrets
5. Test with invalid encryption key to validate security

## Notes
- See [Encryption Example Application](../tutorial/example_app_encryption.md)
- For non-encrypted flow, refer to [Standard Implementation](../tutorial/example_implementation.md)