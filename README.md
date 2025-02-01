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
- **Customizable Templates**: Flexible UI templates for 2FA setup and verification
- **Session Management**: Built-in session tracking for 2FA validation

## Installation

To install `two-fast-auth`, use pip:
```bash
pip install two-fast-auth
```

## Basic Usage

```python
from fastapi import FastAPI
from two_fast_auth import TwoFactorMiddleware, TwoFactorConfig

app = FastAPI()

config = TwoFactorConfig(
    issuer_name="Your App Name",
    excluded_paths=["/docs", "/redoc"],
    qr_code_size=200,
    recovery_codes_count=8
)

app.add_middleware(TwoFactorMiddleware, config=config)

@app.get("/protected-route")
async def protected_route():
    return {"message": "2FA protected content"}
```

## Configuration Options

### TwoFactorConfig

| Parameter           | Default      | Description                                                                 |
|---------------------|--------------|-----------------------------------------------------------------------------|
| `issuer_name`       | Required     | Name displayed in authenticator apps                                        |
| `excluded_paths`    | []           | Paths that bypass 2FA verification                                          |
| `qr_code_size`      | 200          | Size in pixels for generated QR codes                                       |
| `recovery_codes_count` | 10      | Number of recovery codes to generate per user                               |
| `totp_interval`     | 30           | Time interval (seconds) for TOTP codes                                      |
| `session_expiry`    | 3600         | Session duration after successful 2FA verification (seconds)               |

## Advanced Configuration

```python
from two_fast_auth import TwoFactorMiddleware, TwoFactorConfig

config = TwoFactorConfig(
    issuer_name="Secure App",
    excluded_paths=["/public", "/healthcheck"],
    qr_code_size=300,
    recovery_codes_count=12,
    totp_interval=60,
    session_expiry=7200,
    custom_template="custom_2fa.html",
    failed_attempts_limit=5
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