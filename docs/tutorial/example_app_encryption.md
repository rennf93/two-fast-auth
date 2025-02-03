---
title: Encrypted Example Application - Two-Fast-Auth
description: Learn how to implement encrypted 2FA in a FastAPI application
keywords: two-fast-auth encrypted example, fastapi 2fa encryption, secure 2fa setup
---

# Encrypted Example Application

```python
# You'll have to create and import
# your own user models, functions, db
# and other dependencies.
# Personal recommendation is to use
# FastAPI Users and SQLAlchemy if you
# don't need a fully customized user
# management system.
from cryptography.fernet import Fernet
from database import async_session_maker
from users import (
    User,
    UserRead,
    UserCreate,
    fastapi_users,
    auth_backend,
    current_active_user
)

# Import FastAPI and Two-Fast-Auth
from fastapi import (
    FastAPI,
    Body,
    Depends,
    Header,
    HTTPException,
    status
)
from fastapi.responses import StreamingResponse
from two_fast_auth import (
    TwoFactorMiddleware,
    TwoFactorAuth
)


# Generate or use a persistent encryption key
ENCRYPTION_KEY = Fernet.generate_key()


# Create FastAPI instance
app = FastAPI()


# Get encrypted secret from database
async def get_encrypted_secret(user_id: str) -> str:
    async with async_session_maker() as session:
        user = await session.get(User, user_id)
        return user.encrypted_secret if user else None


# Middleware with encryption
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=lambda uid: get_encrypted_secret(uid),
    encryption_key=ENCRYPTION_KEY,
    excluded_paths=[
        "/docs", # Swagger UI
        "/openapi.json", # OpenAPI JSON
        "/redoc", # Redoc UI
        "/auth/jwt/login", # FastAPI Users login
        "/auth/register", # FastAPI Users register
        "/setup-2fa", # Example endpoint
        "/verify-2fa", # Example endpoint
        "/recovery-codes" # Example endpoint
    ]
)


# FastAPI Users Routers
## Auth Router
app.include_router(
    fastapi_users.get_auth_router(
        auth_backend
    ),
    prefix="/auth/jwt",
    tags=["Auth"],
)


## Register Router
app.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate
    ),
    prefix="/auth",
    tags=["Auth"],
)


# Endpoints examples
## Setup 2FA with Headers
@app.post(
    "/setup-2fa",
    tags=["Auth"]
)
async def setup_2fa(
    user: User = Depends(current_active_user)
):
    tfa = TwoFactorAuth()
    encrypted_secret = TwoFactorAuth.encrypt_secret(
        tfa.secret,
        ENCRYPTION_KEY
    )
    recovery_codes = TwoFactorAuth.generate_recovery_codes()

    async with async_session_maker() as session:
        db_user = await session.get(User, user.id)
        db_user.encrypted_secret = encrypted_secret
        db_user.recovery_codes = recovery_codes
        await session.commit()

    return StreamingResponse(
        tfa.generate_qr_code(user.email),
        media_type="image/png",
        headers={
            "X-Encrypted-Secret": encrypted_secret,
            "X-Recovery-Codes": ",".join(recovery_codes)
        }
    )


## Verification with Manual Decryption
@app.post(
    "/verify-2fa",
    tags=["Auth"]
)
async def verify_2fa(
    code: str = Body(...),
    user: User = Depends(current_active_user)
):
    async with async_session_maker() as session:
        db_user = await session.get(User, user.id)
        if not db_user.encrypted_secret:
            raise HTTPException(
                status_code=400,
                detail="2FA not set up"
            )

        secret = TwoFactorAuth.decrypt_secret(
            db_user.encrypted_secret,
            ENCRYPTION_KEY
        )

    if not TwoFactorAuth(secret).verify_code(code):
        raise HTTPException(
            status_code=401,
            detail="Invalid code"
        )

    return {"status": "verified"}


## 2FA protected
@app.get(
    "/protected-route",
    tags=["Protected"]
)
async def protected_route(
    user: User = Depends(current_active_user),
    x_2fa_code: str = Header(
        ...,
        alias="X-2FA-Code"
    )
):
    # Explicit 2FA verification for demonstration
    if not user.two_fa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA not configured"
        )

    if not TwoFactorAuth(user.two_fa_secret).verify_code(x_2fa_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid 2FA code"
        )

    return {
        "message": "You've accessed a protected route with valid 2FA!",
        "user_id": str(user.id)
    }


# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
```