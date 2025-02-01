---
title: Two-Fast-Auth - FastAPI 2FA Middleware
description: FastAPI middleware for simplified 2FA implementation
keywords: fastapi, security, middleware, python, 2fa, 2fa middleware, fastapi 2fa, fastapi 2fa middleware
---

# Two-Fast-Auth

![Two-Fast-Auth Logo](assets/big_logo.svg)

[![PyPI version](https://badge.fury.io/py/two-fast-auth.svg?cache=none)](https://badge.fury.io/py/two-fast-auth)
[![Release](https://github.com/rennf93/two-fast-auth/actions/workflows/release.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/rennf93/two-fast-auth/actions/workflows/ci.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/ci.yml)
[![CodeQL](https://github.com/rennf93/two-fast-auth/actions/workflows/code-ql.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/code-ql.yml)

[![pages-build-deployment](https://github.com/rennf93/two-fast-auth/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/rennf93/two-fast-auth/actions/workflows/pages/pages-build-deployment)
[![Docs Update](https://github.com/rennf93/two-fast-auth/actions/workflows/docs.yml/badge.svg)](https://github.com/rennf93/two-fast-auth/actions/workflows/docs.yml)
[![Downloads](https://pepy.tech/badge/two-fast-auth)](https://pepy.tech/project/two-fast-auth)

`two-fast-auth` is a FastAPI middleware for simplified 2FA implementation. It integrates seamlessly with FastAPI to offer robust protection against various security threats, ensuring your application remains secure and reliable.

## Features
- QR Code Generation
- TOTP Verification
- Recovery Codes Generation

## Quick Start
```python
from fastapi import FastAPI
from two_fast_auth import TwoFactorMiddleware

app = FastAPI()
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=lambda uid: "secret",
    excluded_paths=["/docs"]
)
```

## Documentation

- [Installation](installation.md)
- [First Steps](tutorial/first-steps.md)
- [Example Application](tutorial/example_app.md)
- [Example Implementation](tutorial/example_implementation.md)
- [TwoFactorAuth Class](core/core.md)
- [TwoFactorMiddleware Class](middleware/middleware.md)
