---
title: Installation - Two-Fast-Auth
description: Learn how to install and set up Two-Fast-Auth, a FastAPI middleware for simplified 2FA implementation
keywords: two-fast-auth installation, fastapi 2fa middleware, fastapi 2fa setup
---

# Installation

## Requirements
- Python 3.10+
- cryptography (required for secret encryption)
- FastAPI
- pyotp
- qrcode
- Pillow

## Install
```bash
pip install two-fast-auth
```

## Verify Installation
```python
import two_fast_auth
print(two_fast_auth.__version__)
```

## Configuration
```python
from two_fast_auth import TwoFactorMiddleware

# Without encryption
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=lambda uid: "user_secret",
    header_name="X-2FA-Token"
)

# With encryption
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=lambda uid: "encrypted_secret",
    encryption_key="your-fernent-key-here",
    header_name="X-2FA-Token"
)
```

## Development
```bash
git clone https://github.com/rennf93/two-fast-auth
cd two-fast-auth
pip install -e .
```

## Dependency Matrix
| Component | Required | Version | Purpose |
|-----------|----------|---------|---------|
| cryptography | Yes * | 44.0.0+ | Secret encryption |
| Python | Yes | 3.10+ | Runtime |
| FastAPI | Yes | 0.115.8+ | Runtime |
| FastAPI Users | Optional | 14.0.1+ | Runtime |
| Pillow | Yes | 11.1.0+ | Runtime |
| PyOTP | Yes | 2.9.0+ | Runtime |
| QRCode | Yes | 8.0+ | Runtime |
| SQLAlchemy | Optional | 2.0.37+ | Runtime |
| * Required for encryption features |

# What's Next?
- [First Steps](tutorial/first-steps.md)
- [Standard Implementation](tutorial/example_implementation.md)
- [Encryption Implementation](tutorial/example_implementation_encryption.md)
- [Example Application](tutorial/example_app.md)
- [Encryption Example Application](tutorial/example_app_encryption.md)
