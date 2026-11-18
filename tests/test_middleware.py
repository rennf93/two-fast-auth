import pyotp
import pytest
from conftest import MockUser, UserSecretLookup
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.testclient import TestClient

from two_fast_auth import TwoFactorMiddleware


@pytest.mark.asyncio
async def test_middleware_excluded_paths(
    test_app: FastAPI, test_client: TestClient, mock_get_user_secret: UserSecretLookup
) -> None:
    @test_app.get("/excluded")
    async def excluded_route() -> dict[str, str]:
        return {"message": "OK"}

    @test_app.get("/protected")
    async def protected_route(request: Request) -> dict[str, str]:
        return {"message": "Protected"}

    test_app.add_middleware(
        TwoFactorMiddleware,
        get_user_secret_callback=mock_get_user_secret,
        excluded_paths=["/excluded"],
    )

    response = test_client.get("/excluded", headers={"X-2FA-Code": "123456"})
    assert response.status_code == status.HTTP_200_OK

    response = test_client.get("/protected")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_middleware_authentication_flow(
    two_factor_middleware: TwoFactorMiddleware, mock_user: MockUser
) -> None:
    async def async_call_next(request: Request) -> Response:
        return Response("OK", status_code=status.HTTP_200_OK)

    valid_code = pyotp.TOTP("JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP").now()
    mock_user.id = "user_with_2fa"
    response = await two_factor_middleware.dispatch(
        Request(
            scope={
                "type": "http",
                "method": "GET",
                "path": "/",
                "headers": [(b"x-2fa-code", valid_code.encode())],
                "user": mock_user,
            }
        ),
        async_call_next,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_middleware_protected_paths(
    test_app: FastAPI, mock_get_user_secret: UserSecretLookup
) -> None:
    user = type(
        "User",
        (),
        {
            "id": "user_with_2fa",
            "is_authenticated": True,
            "two_fa_secret": "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP",
        },
    )()

    @test_app.get("/protected")
    async def protected_route(request: Request) -> dict[str, str]:
        return {"message": "Protected"}

    middleware = TwoFactorMiddleware(
        app=test_app, get_user_secret_callback=mock_get_user_secret, excluded_paths=[]
    )

    request = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/protected",
            "headers": [],
            "user": user,
        }
    )

    async def sync_call_next(request: Request) -> Response:
        return Response("OK")

    with pytest.raises(HTTPException) as exc:
        await middleware.dispatch(request, sync_call_next)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

    valid_code = pyotp.TOTP("JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP").now()
    valid_request = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/protected",
            "headers": [(b"x-2fa-code", valid_code.encode())],
            "user": user,
        }
    )

    async def async_call_next(request: Request) -> Response:
        return Response("OK", status_code=status.HTTP_200_OK)

    response = await middleware.dispatch(valid_request, async_call_next)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_middleware_scope_get_scenarios(
    test_app: FastAPI, mock_get_user_secret: UserSecretLookup
) -> None:
    """Test all possible request.scope.get scenarios"""
    middleware = TwoFactorMiddleware(
        app=test_app, get_user_secret_callback=mock_get_user_secret, excluded_paths=[]
    )

    async def call_next(request: Request) -> Response:
        return Response("OK", status_code=status.HTTP_200_OK)

    # Scenario 1: scope with no user key
    request1 = Request(
        scope={"type": "http", "method": "GET", "path": "/test", "headers": []}
    )
    response = await middleware.dispatch(request1, call_next)
    assert response.status_code == status.HTTP_200_OK

    # Scenario 2: scope with explicit None user
    request2 = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
            "user": None,
        }
    )
    response = await middleware.dispatch(request2, call_next)
    assert response.status_code == status.HTTP_200_OK

    # Scenario 3: scope with unauthenticated user
    request3 = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
            "user": type("User", (), {"is_authenticated": False})(),
        }
    )
    response = await middleware.dispatch(request3, call_next)
    assert response.status_code == status.HTTP_200_OK

    # Scenario 4: scope with authenticated user but no 2FA
    request4 = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
            "user": type("User", (), {"id": "user_no_2fa", "is_authenticated": True})(),
        }
    )
    response = await middleware.dispatch(request4, call_next)
    assert response.status_code == status.HTTP_200_OK

    # Scenario 5: scope with fully authenticated user with 2FA
    request5 = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [(b"x-2fa-code", b"123456")],
            "user": type(
                "User", (), {"id": "user_with_2fa", "is_authenticated": True}
            )(),
        }
    )
    with pytest.raises(HTTPException) as exc:
        await middleware.dispatch(request5, call_next)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
