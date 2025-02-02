![Two-Fast-Auth Logo](docs/assets/big_logo.svg)

---

[![PyPI version](https://badge.fury.io/py/two-fast-auth.svg?cache=none)](https://badge.fury.io/py/two-fast-auth)
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
    header_name="X-2FA-Code"
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
| `excluded_paths`    | ["/login", "/setup-2fa"] | Paths that bypass 2FA verification                                  |
| `header_name`       | "X-2FA-Code"         | Request header containing 2FA verification code                             |

## Advanced Configuration

```python
# Custom QR code generation
auth = TwoFactorAuth(
    qr_fill_color="#1a73e8",
    qr_back_color="#f8f9fa",
    issuer_name="Secure Corp"
)

# Middleware with custom settings
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    excluded_paths=["/public", "/healthcheck"],
    header_name="X-MFA-Token"
)

# Generate recovery codes (10 chars length, 8 codes)
recovery_codes = TwoFactorAuth.generate_recovery_codes(
    count=8,
    code_length=10
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

- [FastAPI](https://fastapi.tiangolo.com/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [PyOTP](https://pyauth.github.io/pyotp/)
- [qrcode](https://github.com/lincolnloop/python-qrcode)