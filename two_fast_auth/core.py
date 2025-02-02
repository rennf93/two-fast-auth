from cryptography.fernet import (
    Fernet,
    InvalidToken
)
from io import BytesIO
import secrets
import pyotp
import qrcode
from typing import (
    Optional,
    Union
)


class TwoFactorAuth:
    def __init__(
        self,
        secret: str = None,
        *,
        qr_fill_color: str = "black",
        qr_back_color: str = "white",
        issuer_name: str = "2FastAuth"
    ):
        self.secret = secret or pyotp.random_base32()
        self.qr_fill_color = qr_fill_color
        self.qr_back_color = qr_back_color
        self.issuer_name = issuer_name

    def generate_qr_code(
        self,
        user_email: str
    ) -> BytesIO:
        """Generate QR code for authenticator app setup"""
        if not user_email:
            raise ValueError("User email is required")

        uri = pyotp.totp.TOTP(
            self.secret
        ).provisioning_uri(
            name=user_email,
            issuer_name=self.issuer_name
        )

        qr = qrcode.QRCode()
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(
            fill_color=self.qr_fill_color,
            back_color=self.qr_back_color
        )
        byte_io = BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        return byte_io

    def verify_code(
        self,
        code: str
    ) -> bool:
        """Verify the 2FA code"""
        if not code or len(code) != 6:
            return False

        totp = pyotp.TOTP(self.secret)
        return totp.verify(code)

    @staticmethod
    def generate_recovery_codes(
        count: int = 5,
        code_length: int = 10
    ) -> tuple[str, ...]:
        """Generate recovery codes with customizable parameters"""
        return tuple(
            secrets.token_urlsafe(code_length)
            for _ in range(count)
        )

    @staticmethod
    def encrypt_secret(
        secret: str,
        encryption_key: Optional[Union[str, bytes]] = None
    ) -> str:
        """Encrypt 2FA secret (optional)"""
        if not secret:
            raise ValueError("Secret cannot be empty")

        if not encryption_key:
            return secret

        key_bytes = (
            encryption_key
            if isinstance(encryption_key, bytes)
            else encryption_key.encode()
        )

        try:
            cipher = Fernet(key_bytes)
            return cipher.encrypt(
                secret.encode()
            ).decode()

        except (ValueError, TypeError) as e:
            raise ValueError(f"Encryption failed: {str(e)}") from e

    @staticmethod
    def decrypt_secret(
        encrypted_secret: str,
        encryption_key: Optional[Union[str, bytes]] = None
    ) -> str:
        """Decrypt 2FA secret (optional)"""
        if not encrypted_secret:
            raise ValueError("No secret to decrypt")

        if not encryption_key:
            return encrypted_secret

        key_bytes = (
            encryption_key
            if isinstance(encryption_key, bytes)
            else encryption_key.encode()
        )

        try:
            cipher = Fernet(key_bytes)
            return cipher.decrypt(
                encrypted_secret.encode()
            ).decode()

        except (InvalidToken, ValueError) as e:
            raise ValueError(f"Decryption failed: {str(e)}") from e
