---
title: Secret Encryption - Two-Fast-Auth
description: Learn how to securely encrypt 2FA secrets using Two-Fast-Auth
keywords: two-fast-auth encryption, fernet encryption, 2fa secret security
---

# Secret Encryption Guide

## Generating Encryption Keys
```python
from cryptography.fernet import Fernet

# Generate a new key to encrypt/decrypt the 2FA secret
key = Fernet.generate_key()
print("Encryption key:", key.decode())
```

## Using Encryption
```python
from two_fast_auth import TwoFactorAuth

# Encrypt the 2FA secret
encrypted_secret = TwoFactorAuth.encrypt_secret(
    "plaintext_secret",
    encryption_key="your-encryption-key"
)

# Decrypt the 2FA secret
decrypted_secret = TwoFactorAuth.decrypt_secret(
    encrypted_secret,
    encryption_key="your-encryption-key"
)
```

## Middleware Configuration
```python
app.add_middleware(
    TwoFactorMiddleware,
    get_user_secret_callback=get_user_secret,
    encryption_key="your-encryption-key",
    excluded_paths=["/docs"]
)
```

## Best Practices
1. Store encryption keys securely (e.g., environment variables/secret manager)
2. Rotate keys periodically using key rotation strategies
3. Use different keys for different environments
4. Always validate keys during middleware initialization

## Migration Example
```python
# Migrate existing unencrypted secrets
async def migrate_secrets():
    for user in get_all_users():
        if not user.encrypted_secret:
            encrypted = TwoFactorAuth.encrypt_secret(
                user.plain_secret,
                encryption_key=KEY
            )
            user.encrypted_secret = encrypted
            await user.save()
```
