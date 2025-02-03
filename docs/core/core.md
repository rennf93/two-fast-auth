---
title: TwoFactorAuth Class - Two-Fast-Auth
description: Learn how to use the TwoFactorAuth class in your FastAPI application using Two-Fast-Auth
keywords: two-fast-auth two-factor-auth, fastapi 2fa middleware, fastapi 2fa setup
---

# TwoFactorAuth Class

## Class Definition
```python
class TwoFactorAuth(
    secret: str = None,
    *,
    qr_fill_color: str = "black",
    qr_back_color: str = "white",
    issuer_name: str = "2FastAuth"
)
```

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `secret` | `str` | `None` | Base32 secret (auto-generated if None) |
| `qr_fill_color` | `str` | "black" | QR code foreground color |
| `qr_back_color` | `str` | "white" | QR code background color |
| `issuer_name` | `str` | "2FastAuth" | Service name for authenticator apps |

## Methods
### `generate_qr_code(user_email: str) -> BytesIO`
- Generates QR code for authenticator setup
- **Parameters:**
    - `user_email`: User's email address
- **Returns:** BytesIO object containing QR code image
- **Raises:** `ValueError` if email is empty

### `verify_code(code: str) -> bool`
- Validates 6-digit TOTP code using pyotp
- **Parameters:**
    - `code`: 6-digit TOTP code
- **Returns:** `True` if code is valid

### `generate_recovery_codes(count=5, code_length=10) -> tuple[str, ...]`
- Generates URL-safe recovery codes using secrets module
- **Parameters:**
    - `count`: Number of codes to generate
    - `code_length`: Length of each code
- **Returns:** Tuple of recovery codes

### `encrypt_secret(secret: str, encryption_key: Optional[Union[str, bytes]] = None) -> str` (static)
- Encrypts 2FA secret using Fernet encryption
- **Parameters:**
    - `secret`: Plaintext base32 secret
    - `encryption_key`: Fernet-compatible key (str/bytes)
- **Returns:** Encrypted secret string
- **Raises:** `ValueError` for invalid inputs

### `decrypt_secret(encrypted_secret: str, encryption_key: Optional[Union[str, bytes]] = None) -> str` (static)
- Decrypts encrypted 2FA secret
- **Parameters:**
    - `encrypted_secret`: Encrypted secret string
    - `encryption_key`: Key used for encryption
- **Returns:** Decrypted base32 secret
- **Raises:** `ValueError` for decryption failures

## Error Handling
- `ValueError`: Invalid email address
- `TypeError`: Invalid code format

## Example
```python
from two_fast_auth import TwoFactorAuth

# Initialize with default settings
tfa = TwoFactorAuth()
qr = tfa.generate_qr_code("user@example.com")
valid = tfa.verify_code("123456")
codes = TwoFactorAuth.generate_recovery_codes()
```
