---
title: Implementing TwoFactorAuth - Two-Fast-Auth
description: Learn how to implement TwoFactorAuth in your FastAPI application using Two-Fast-Auth
keywords: two-fast-auth two-factor-auth, fastapi 2fa middleware, fastapi 2fa setup
---

# Implementing TwoFactorAuth

## QR Code Generation
```python
from two_fast_auth import TwoFactorAuth
from fastapi.responses import StreamingResponse

@app.post("/setup-2fa")
async def setup_2fa(
    user: User = Depends(current_active_user)
):
    tfa = TwoFactorAuth(
        issuer_name="MyApp",
        qr_fill_color="#4a86e8"
    )
    qr_code = tfa.generate_qr_code(user.email)

    # Store secret in database
    user.two_fa_secret = tfa.secret
    await user.save()

    return StreamingResponse(qr_code, media_type="image/png")
```

## Encrypted Secret Setup
```python
@app.post("/setup-2fa")
async def setup_2fa(user: User = Depends(current_active_user)):
    tfa = TwoFactorAuth()
    encrypted_secret = TwoFactorAuth.encrypt_secret(
        tfa.secret,
        encryption_key="your-encryption-key"  # Match middleware key
    )

    user.two_fa_secret = encrypted_secret
    await user.save()

    return {
        "qr_code": tfa.generate_qr_code(user.email),
        "secret": "Store this encrypted value: " + encrypted_secret
    }
```

## Encryption Verification
```python
@app.post("/verify-2fa")
async def verify_2fa(
    code: str = Form(...),
    user: User = Depends(current_active_user)
):
    try:
        secret = TwoFactorAuth.decrypt_secret(
            user.two_fa_secret,
            encryption_key="your-encryption-key"
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

    if not TwoFactorAuth(secret).verify_code(code):
        raise HTTPException(401, "Invalid code")

    return {"status": "verified"}
```

## Recovery Code Management
```python
@app.post("/generate-recovery-codes")
async def generate_recovery_codes(
    user: User = Depends(current_active_user)
):
    codes = TwoFactorAuth.generate_recovery_codes(
        count=10,
        code_length=8
    )
    user.recovery_codes = codes
    await user.save()
    return {"recovery_codes": codes}
```

## Notes
- For complete encrypted examples, see [Encryption Implementation](../tutorial/example_implementation_encryption.md)
