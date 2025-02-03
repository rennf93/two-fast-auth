---
title: Example Implementation - Two-Fast-Auth
description: Learn how to implement 2FA in a FastAPI application using Two-Fast-Auth
keywords: two-fast-auth example implementation, fastapi 2fa middleware, fastapi 2fa setup
---

# Complete Example Implementation

## Full Configuration
```python
from fastapi import FastAPI, Depends, HTTPException
from two_fast_auth import TwoFactorMiddleware, TwoFactorAuth

app = FastAPI()

# Database setup and user model
# ...

# Middleware configuration
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    excluded_paths=["/setup-2fa", "/verify-2fa"]
)
```

## Auth endpoints
```python
@app.post("/setup-2fa")
async def setup_2fa_endpoint(
    user: User = Depends(current_active_user)
):
    tfa = TwoFactorAuth()
    qr_code = tfa.generate_qr_code(user.email)
    user.two_fa_secret = tfa.secret
    await user.save()
    return StreamingResponse(qr_code, media_type="image/png")

@app.post("/verify-2fa")
async def verify_2fa_endpoint(
    code: str = Form(...),
    user: User = Depends(current_active_user)
):
    if not TwoFactorAuth(user.two_fa_secret).verify_code(code):
        raise HTTPException(
            status_code=401,
            detail="Invalid 2FA code"
        )
    return {"status": "verified"}
```

## Protected endpoint
```python
@app.get("/protected-data")
async def protected_data(
    user: User = Depends(current_active_user)
):
    return {"data": "Sensitive information"}
```

## Testing Workflow
1. Start server: `uvicorn example_app:app --reload`
2. Register user at `/auth/register`
3. Login with credentials at `/auth/jwt/login`
4. Access `/setup-2fa` to get QR code
5. Scan code in authenticator app
6. Access protected routes with valid code

## Notes
- See [Example Application](../tutorial/example_app.md) for complete implementation
- For encrypted secrets, use [Encryption Implementation](../tutorial/example_implementation_encryption.md)
