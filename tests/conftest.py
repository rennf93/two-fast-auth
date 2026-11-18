from collections.abc import Awaitable, Callable

import pytest
from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi.testclient import TestClient

from two_fast_auth import TwoFactorAuth, TwoFactorMiddleware

UserSecretLookup = Callable[[str], Awaitable[str | None]]


class MockUser:
    def __init__(self) -> None:
        self.id = "user_with_2fa"
        self.email = "user@example.com"
        self.two_fa_secret = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"
        self.is_authenticated = True


@pytest.fixture
def two_factor_auth() -> TwoFactorAuth:
    return TwoFactorAuth()


@pytest.fixture
def mock_get_user_secret() -> UserSecretLookup:
    """Fixture that returns the mock secret lookup function"""
    secrets: dict[str, str | None] = {
        "user_with_2fa": "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP",
        "user_no_2fa": None,
    }

    async def _mock_get_user_secret(user_id: str) -> str | None:
        return secrets.get(user_id)

    return _mock_get_user_secret


@pytest.fixture
def two_factor_middleware(
    test_app: FastAPI, mock_get_user_secret: UserSecretLookup
) -> TwoFactorMiddleware:
    return TwoFactorMiddleware(
        app=test_app, get_user_secret_callback=mock_get_user_secret, excluded_paths=[]
    )


@pytest.fixture
def test_app() -> FastAPI:
    app = FastAPI()
    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


@pytest.fixture
def mock_user() -> MockUser:
    return MockUser()


@pytest.fixture
def valid_encryption_key() -> bytes:
    return Fernet.generate_key()


@pytest.fixture
def invalid_encryption_key() -> bytes:
    return b"invalid_key_1234567890_"


@pytest.fixture
def encrypted_secret(valid_encryption_key: bytes) -> str:
    return TwoFactorAuth.encrypt_secret(
        "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP", valid_encryption_key
    )
