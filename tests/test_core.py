import pytest
from io import BytesIO
import pyotp
from two_fast_auth import TwoFactorAuth



def test_default_initialization():
    tfa = TwoFactorAuth()
    assert len(tfa.secret) == 32
    assert tfa.issuer_name == "2FastAuth"


def test_custom_initialization():
    custom_secret = "CUSTOMSECRET123456"
    tfa = TwoFactorAuth(
        secret=custom_secret,
        qr_fill_color="blue",
        qr_back_color="yellow",
        issuer_name="TestIssuer"
    )
    assert tfa.secret == custom_secret
    assert tfa.qr_fill_color == "blue"
    assert tfa.issuer_name == "TestIssuer"


def test_generate_qr_code(
    two_factor_auth, mock_user
):
    qr_code = two_factor_auth.generate_qr_code(mock_user.email)
    assert isinstance(qr_code, BytesIO)
    assert qr_code.getbuffer().nbytes > 0


def test_verify_valid_code(two_factor_auth):
    code = pyotp.TOTP(two_factor_auth.secret).now()
    assert two_factor_auth.verify_code(code)


def test_verify_invalid_code(two_factor_auth):
    assert two_factor_auth.verify_code("000000") is False


def test_generate_recovery_codes():
    codes = TwoFactorAuth.generate_recovery_codes()
    assert len(codes) == 5
    assert all(len(code) == 14 for code in codes)

    custom_codes = TwoFactorAuth.generate_recovery_codes(
        count=3,
        code_length=8
    )
    assert len(custom_codes) == 3
    assert all(len(code) == 11 for code in custom_codes)
