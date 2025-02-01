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
from two_fast_auth import TwoFactorMiddleware

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    excluded_paths=["/setup-2fa"]
)
```

3. **Create Setup Endpoint**
```python
from two_fast_auth import TwoFactorAuth

@app.post("/setup-2fa")
async def setup_2fa(user: User = Depends(current_user)):
    tfa = TwoFactorAuth()
    return {
        "qr_code": tfa.generate_qr_code(user.email),
        "secret": tfa.secret
    }
```

4. **Implement Verification**
```python
@app.post("/verify-2fa")
async def verify_2fa(code: str, user: User = Depends(current_user)):
    if not TwoFactorAuth(user.two_fa_secret).verify_code(code):
        raise HTTPException(400, "Invalid code")
    return {"status": "verified"}
```
