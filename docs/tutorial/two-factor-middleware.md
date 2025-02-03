---
title: Implementing TwoFactorMiddleware - Two-Fast-Auth
description: Learn how to implement TwoFactorMiddleware in your FastAPI application using Two-Fast-Auth
keywords: two-fast-auth two-factor-middleware, fastapi 2fa middleware, fastapi 2fa setup
---

# Implementing TwoFactorMiddleware

## Basic Configuration
```python
from two_fast_auth import TwoFactorMiddleware

async def get_user_secret(
    user_id: str
) -> Optional[str]:
    async with AsyncSession() as session:
        user = await session.get(
            User,
            user_id
        )
        return user.two_fa_secret if user else None

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    excluded_paths=[
        "/docs",
        "/openapi.json",
        "/auth/jwt/login",
        "/setup-2fa"
    ],
    header_name="X-2FA-Code"
)
```

## Encryption Configuration
```python
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    encryption_key="your-32-url-safe-base64-key",  # Required for encrypted secrets
    excluded_paths=[
        "/docs",
        "/setup-2fa"
    ],
    header_name="X-2FA-Code"
)
```

## Handling Exceptions
```python
@app.exception_handler(HTTPException)
async def two_fa_exception_handler(
    request: Request,
    exc: HTTPException
):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "2FA verification required"
            }
        )
    return await http_exception_handler(request, exc)
```

## Testing Middleware
```python
def test_2fa_protected_route():
    # Valid request
    response = client.get(
        "/protected",
        headers={"X-2FA-Code": "123456"}
    )
    assert response.status_code == 200

    # Missing 2FA header
    response = client.get("/protected")
    assert response.status_code == 401
```

## Encryption Validation
```python
# Test valid encrypted flow
def test_encrypted_flow():
    valid_code = get_current_totp_code(secret)
    response = client.get(
        "/protected",
        headers={"X-2FA-Code": valid_code}
    )
    assert response.status_code == 200

# Test invalid encryption key
def test_bad_encryption():
    with pytest.raises(ValueError) as exc:
        TwoFactorAuth.decrypt_secret(
            encrypted_secret,
            encryption_key="wrong-key"
        )
    assert "Decryption failed" in str(exc.value)
```

## Notes
- For full encrypted middleware examples, refer to [Encryption Implementation](../tutorial/example_implementation_encryption.md)
