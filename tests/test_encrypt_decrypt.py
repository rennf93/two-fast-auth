from typing import cast

import pytest
from conftest import UserSecretLookup
from cryptography.fernet import Fernet
from fastapi import FastAPI, HTTPException, Request, Response, status

from two_fast_auth import TwoFactorAuth, TwoFactorMiddleware


class TestEncryptionDecryption:
    """Test suite for encryption/decryption functionality"""

    @pytest.mark.parametrize(
        "secret",
        ["JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP123", "ANOTHER_SECRET_KEY", "TEST!@#$%^&*()"],
    )
    def test_encrypt_decrypt_cycle(
        self, secret: str, valid_encryption_key: bytes
    ) -> None:
        """Test full encrypt/decrypt cycle with valid key"""
        encrypted = TwoFactorAuth.encrypt_secret(secret, valid_encryption_key)
        decrypted = TwoFactorAuth.decrypt_secret(encrypted, valid_encryption_key)
        assert decrypted == secret

    def test_encrypt_without_key(self) -> None:
        """Test encryption without key returns plaintext"""
        secret = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"
        result = TwoFactorAuth.encrypt_secret(secret, None)
        assert result == secret

    def test_decrypt_without_key(self) -> None:
        """Test decryption without key returns ciphertext"""
        encrypted = "gAAAAABmD-3C6r1zUQ4E8E6tZJQY7KjH7J7XqY7b7v3V3Z3n3v3r3t3y3u3w=="
        result = TwoFactorAuth.decrypt_secret(encrypted, None)
        assert result == encrypted

    @pytest.mark.parametrize("key_type", [str, bytes])
    def test_key_type_handling(
        self, key_type: type, valid_encryption_key: bytes
    ) -> None:
        """Test both string and bytes key formats"""
        secret = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"
        key = valid_encryption_key.decode() if key_type is str else valid_encryption_key
        encrypted = TwoFactorAuth.encrypt_secret(secret, key)
        decrypted = TwoFactorAuth.decrypt_secret(encrypted, key)
        assert decrypted == secret

    def test_invalid_encryption_key(self) -> None:
        """Test encryption with invalid key format"""
        with pytest.raises(ValueError) as exc:
            TwoFactorAuth.encrypt_secret("secret", b"invalid_key")
        assert "Encryption failed" in str(exc.value)

    def test_decrypt_with_wrong_key(self, valid_encryption_key: bytes) -> None:
        """Test decryption with incorrect key"""
        secret = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"
        encrypted = TwoFactorAuth.encrypt_secret(secret, valid_encryption_key)

        wrong_key = Fernet.generate_key()

        with pytest.raises(ValueError) as exc:
            TwoFactorAuth.decrypt_secret(encrypted, wrong_key)
        assert "Decryption failed" in str(exc.value)

    def test_tampered_ciphertext(self, valid_encryption_key: bytes) -> None:
        """Test decryption of modified ciphertext"""
        encrypted = TwoFactorAuth.encrypt_secret(
            "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP", valid_encryption_key
        )
        tampered = encrypted[:-1] + "X"

        with pytest.raises(ValueError) as exc:
            TwoFactorAuth.decrypt_secret(tampered, valid_encryption_key)
        assert "Decryption failed" in str(exc.value)

    def test_empty_secret_handling(self, valid_encryption_key: bytes) -> None:
        """Test edge case with empty secret"""
        with pytest.raises(ValueError) as exc:
            TwoFactorAuth.encrypt_secret("", valid_encryption_key)
        assert "Secret cannot be empty" in str(exc.value)

    def test_decrypt_empty_secret(self) -> None:
        """Test decrypting empty secret raises proper error"""
        with pytest.raises(ValueError) as exc:
            TwoFactorAuth.decrypt_secret("", "dummy_key")
        assert "No secret to decrypt" in str(exc.value)

    def test_decrypt_none_secret(self) -> None:
        """Test decrypt None secret handling"""
        with pytest.raises(ValueError) as exc:
            TwoFactorAuth.decrypt_secret(cast("str", None), "dummy_key")
        assert "No secret to decrypt" in str(exc.value)


@pytest.mark.asyncio
async def test_invalid_encryption_key_handling(
    mock_get_user_secret: UserSecretLookup,
) -> None:
    """Test middleware initialization with invalid keys"""
    # Test invalid string key
    with pytest.raises(ValueError) as exc:
        TwoFactorMiddleware(
            app=FastAPI(),
            get_user_secret_callback=mock_get_user_secret,
            encryption_key="invalid_key",
        )
    assert "Invalid encryption key" in str(exc.value)

    # Test invalid bytes key
    with pytest.raises(ValueError) as exc:
        TwoFactorMiddleware(
            app=FastAPI(),
            get_user_secret_callback=mock_get_user_secret,
            encryption_key=b"invalid_key",
        )
    assert "Invalid encryption key" in str(exc.value)


@pytest.mark.asyncio
async def test_decryption_failure_handling(
    test_app: FastAPI, mock_get_user_secret: UserSecretLookup
) -> None:
    """Test decryption failure returns proper error"""
    middleware = TwoFactorMiddleware(
        app=test_app,
        get_user_secret_callback=mock_get_user_secret,
        encryption_key=Fernet.generate_key(),
    )

    # Create request with encrypted secret
    request = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/protected",
            "headers": [],
            "user": type(
                "User", (), {"id": "user_with_2fa", "is_authenticated": True}
            )(),
        }
    )

    async def call_next(request: Request) -> Response:
        return Response("OK")

    with pytest.raises(HTTPException) as exc:
        await middleware.dispatch(request, call_next)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Decryption failed" in str(exc.value.detail)
