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

## Code Verification
```python
@app.post("/verify-2fa")
async def verify_2fa(
    code: str = Form(...),
    user: User = Depends(current_active_user)
):
    if not user.two_fa_secret:
        raise HTTPException(
            status_code=400,
            detail="2FA not configured"
        )

    tfa = TwoFactorAuth(user.two_fa_secret)
    if tfa.verify_code(code):
        return {
            "status": "2FA verified"
        }
    raise HTTPException(
        status_code=401,
        detail="Invalid code"
    )
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
