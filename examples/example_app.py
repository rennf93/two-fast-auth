"""
Example FastAPI app with 2FA middleware
"""

# You'll have to create and import
# your own user models, functions, db
# and other dependencies.
# Personal recommendation is to use
# FastAPI Users and SQLAlchemy if you
# don't need a fully customized user
# management system.
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


# Create FastAPI instance
app = FastAPI()


# Get user secret callback for middleware
async def get_user_secret_callback(
    user_id: str
) -> str:
    async with async_session_maker() as session:
        user = await session.get(
            User,
            user_id
        )
        return user.two_fa_secret if user else None


# Add 2FA middleware
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret_callback,
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
## Setup 2FA
@app.post(
    "/setup-2fa",
    tags=["Auth"]
)
async def setup_2fa(
    user: User = Depends(current_active_user)
):
    # Generate new 2FA secret
    two_fa = TwoFactorAuth()

    # Generate QR code
    qr_code = two_fa.generate_qr_code(
        user.email or user.username
    )

    # Generate recovery codes
    recovery_codes = TwoFactorAuth.generate_recovery_codes()

    # Store secret and recovery codes in DB
    async with async_session_maker() as session:
        db_user = await session.get(
            User,
            user.id
        )
        db_user.two_fa_secret = two_fa.secret
        db_user.recovery_codes = recovery_codes
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

    # Return QR code as image stream and other data in headers
    return StreamingResponse(
        qr_code,
        media_type="image/png",
        headers={
            "X-2FA-Secret": two_fa.secret,
            "X-Recovery-Codes": ",".join(recovery_codes)
        }
    )


## Verify 2FA code
@app.post(
    "/verify-2fa",
    tags=["Auth"]
)
async def verify_2fa(
    code: str = Body(
        ...,
        embed=True
    ),
    user: User = Depends(current_active_user)
):
    if not user.two_fa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA not set up"
        )

    two_fa = TwoFactorAuth(user.two_fa_secret)
    if two_fa.verify_code(code):
        return {"success": True}
    return {"success": False}


## Use recovery code
@app.post(
    "/recovery-codes",
    tags=["Auth"]
)
async def use_recovery_code(
    code: str = Body(
        ...,
        embed=True
    ),
    user: User = Depends(current_active_user)
):
    async with async_session_maker() as session:
        # Get fresh user instance from database
        db_user = await session.get(
            User,
            user.id
        )

        if not db_user.recovery_codes or code not in db_user.recovery_codes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid recovery code"
            )

        # Remove used recovery code
        updated_codes = [
            c
            for c in db_user.recovery_codes
            if c != code
        ]
        db_user.recovery_codes = updated_codes
        session.add(db_user)
        await session.commit()

    return {"success": True}


## 2FA protected route example
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
