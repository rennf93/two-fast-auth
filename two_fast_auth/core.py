from io import BytesIO
import secrets
import pyotp
import qrcode


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
