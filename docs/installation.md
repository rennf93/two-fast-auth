---
title: Installation - Two-Fast-Auth
description: Learn how to install and set up Two-Fast-Auth, a FastAPI middleware for simplified 2FA implementation
keywords: two-fast-auth installation, fastapi 2fa middleware, fastapi 2fa setup
---

# Installation

## Requirements
- Python 3.10+
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

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=lambda uid: "user_secret",
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
| Component | Required | Version |
|-----------|----------|---------|
| Python | Yes | 3.10+ |
| FastAPI | Yes | 0.115.8+ |
| FastAPI Users | Optional | 14.0.1+ |
| Pillow | Yes | 11.1.0+ |
| PyOTP | Yes | 2.9.0+ |
| QRCode | Yes | 8.0+ |
| SQLAlchemy | Optional | 2.0.37+ |

# What's Next?
- [First Steps](tutorial/first-steps.md)
- [Learn how to implement 2FA in your FastAPI application](tutorial/example_implementation.md)
- [See an example application](tutorial/example_app.md)
