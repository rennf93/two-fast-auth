from io import BytesIO
from typing import cast

import pyotp
import pytest
from conftest import MockUser

from two_fast_auth import TwoFactorAuth


def test_default_initialization() -> None:
    tfa = TwoFactorAuth()
    assert len(tfa.secret) == 32
    assert tfa.issuer_name == "2FastAuth"


def test_custom_initialization() -> None:
    custom_secret = "CUSTOMSECRET123456"
    tfa = TwoFactorAuth(
        secret=custom_secret,
        qr_fill_color="blue",
        qr_back_color="yellow",
        issuer_name="TestIssuer",
    )
    assert tfa.secret == custom_secret
    assert tfa.qr_fill_color == "blue"
    assert tfa.issuer_name == "TestIssuer"


def test_generate_qr_code(two_factor_auth: TwoFactorAuth, mock_user: MockUser) -> None:
    qr_code = two_factor_auth.generate_qr_code(mock_user.email)
    assert isinstance(qr_code, BytesIO)
    assert qr_code.getbuffer().nbytes > 0


def test_verify_valid_code(two_factor_auth: TwoFactorAuth) -> None:
    code = pyotp.TOTP(two_factor_auth.secret).now()
    assert two_factor_auth.verify_code(code)


def test_verify_invalid_code(two_factor_auth: TwoFactorAuth) -> None:
    assert two_factor_auth.verify_code("000000") is False


def test_generate_recovery_codes() -> None:
    codes = TwoFactorAuth.generate_recovery_codes()
    assert len(codes) == 5
    assert all(len(code) == 14 for code in codes)

    custom_codes = TwoFactorAuth.generate_recovery_codes(count=3, code_length=8)
    assert len(custom_codes) == 3
    assert all(len(code) == 11 for code in custom_codes)


def test_generate_qr_code_without_email(two_factor_auth: TwoFactorAuth) -> None:
    """Test QR code generation validation"""
    with pytest.raises(ValueError) as exc:
        two_factor_auth.generate_qr_code(cast("str", None))
    assert "User email is required" in str(exc.value)

    with pytest.raises(ValueError):
        two_factor_auth.generate_qr_code("")


def test_verify_code_edge_cases(two_factor_auth: TwoFactorAuth) -> None:
    """Test non-6-digit code verification"""
    assert two_factor_auth.verify_code(cast("str", None)) is False
    assert two_factor_auth.verify_code("") is False
    assert two_factor_auth.verify_code("12345") is False  # 5 digits
    assert two_factor_auth.verify_code("1234567") is False  # 7 digits
