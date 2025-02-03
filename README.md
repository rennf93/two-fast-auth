![Two-Fast-Auth Logo](docs/assets/big_logo.svg)

---

[![PyPI version](https://badge.fury.io/py/two-fast-auth.svg?cache=none&icon=si%3Apython&icon_color=%23008cb4)](https://badge.fury.io/py/two-fast-auth)
[![Release](https://github.com/rennf93/two-fast-auth/actions/workflows/release.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/rennf93/two-fast-auth/actions/workflows/ci.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/ci.yml)
[![CodeQL](https://github.com/rennf93/two-fast-auth/actions/workflows/code-ql.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/code-ql.yml)
[![Docs Update](https://github.com/rennf93/two-fast-auth/actions/workflows/docs.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/docs.yml)
[![Downloads](https://pepy.tech/badge/two-fast-auth)](https://pepy.tech/project/two-fast-auth)

`two-fast-auth` is a FastAPI middleware that provides seamless two-factor authentication implementation. It integrates with FastAPI to offer robust 2FA protection for your application routes.

---

## Documentation

📚 [Full Documentation](https://rennf93.github.io/two-fast-auth/) - Comprehensive technical documentation and API reference

## Features

- **QR Code Generation**: Automatic QR code creation for authenticator apps
- **TOTP Verification**: Time-based one-time password validation
- **Recovery Codes**: Secure recovery code generation and management
- **Optional Secret Encryption**: Securely store and verify 2FA secrets
- **Middleware Integration**: Easy integration with FastAPI routes

## Installation

To install `two-fast-auth`, use pip:
```bash
pip install two-fast-auth
```

## Basic Usage

```python
from fastapi import FastAPI
from two_fast_auth import TwoFactorMiddleware, TwoFactorAuth

app = FastAPI()

async def get_user_secret(user_id: str) -> str:
    # Implement your logic to retrieve user's secret from database
    return "user_stored_secret"  # Replace with actual DB lookup

app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    excluded_paths=["/docs", "/redoc"],
    header_name="X-2FA-Code",
    encryption_key="your-key-here"  # Optional
)

@app.get("/protected-route")
async def protected_route():
    return {"message": "2FA protected content"}
```

## Configuration Options

### TwoFactorAuth Parameters

| Parameter           | Default      | Description                                                                 |
|---------------------|--------------|-----------------------------------------------------------------------------|
| `secret`            | Auto-generated| Base32 secret for TOTP generation                                          |
| `qr_fill_color`     | "black"      | QR code foreground color                                                    |
| `qr_back_color`     | "white"      | QR code background color                                                    |
| `issuer_name`       | "2FastAuth"  | Name displayed in authenticator apps                                        |

### TwoFactorMiddleware Parameters

| Parameter           | Default              | Description                                                                 |
|---------------------|----------------------|-----------------------------------------------------------------------------|
| `encryption_key`    | None                 | Encryption key for securing 2FA secrets (Fernet-compatible key)            |
| `excluded_paths`    | ["/login", "/setup-2fa"] | Paths that bypass 2FA verification                                  |
| `header_name`       | "X-2FA-Code"         | Request header containing 2FA verification code                             |

## Advanced Configuration

```python
# Generate and encrypt secret
secret = TwoFactorAuth().secret
encrypted_secret = TwoFactorAuth.encrypt_secret(
    secret,
    encryption_key="your-key-here"
)

# Store encrypted secret in database
async def get_user_secret(user_id: str) -> str:
    return await fetch_encrypted_secret_from_db(user_id)

# Middleware with encrypted secrets
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    encryption_key="your-key-here",
    excluded_paths=["/healthcheck"]
)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

MIT License - See [LICENSE](https://github.com/rennf93/two-fast-auth/blob/main/LICENSE) for details

## Author

**Renzo Franceschini**
- [GitHub Profile](https://github.com/rennf93)
- [Email](mailto:rennf93@gmail.com)

## Acknowledgements

- [Cryptography](https://cryptography.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyOTP](https://pyauth.github.io/pyotp/)
- [qrcode](https://github.com/lincolnloop/python-qrcode)