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
