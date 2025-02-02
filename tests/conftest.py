import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from two_fast_auth import (
    TwoFactorAuth,
    TwoFactorMiddleware
)



@pytest.fixture
def two_factor_auth():
    return TwoFactorAuth()


@pytest.fixture
def mock_get_user_secret():
    """Fixture that returns the mock secret lookup function"""
    secrets = {
        "user_with_2fa": "SECRETEXAMPLE",
        "user_no_2fa": None
    }

    async def _mock_get_user_secret(
        user_id: str
    ):
        return secrets.get(user_id)

    return _mock_get_user_secret


@pytest.fixture
def two_factor_middleware(
    test_app,
    mock_get_user_secret
):
    return TwoFactorMiddleware(
        app=test_app,
        get_user_secret_callback=mock_get_user_secret,
        excluded_paths=[]
    )


@pytest.fixture
def test_app():
    app = FastAPI()
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


@pytest.fixture
def mock_user():
    class MockUser:
        def __init__(self):
            self.id = "user_with_2fa"
            self.email = "user@example.com"
            self.two_fa_secret = "SECRETEXAMPLE"
            self.is_authenticated = True

    return MockUser()
