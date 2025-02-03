from cryptography.fernet import Fernet
from typing import (
    Awaitable,
    Callable,
    List,
    Optional,
    Union
)
from .core import TwoFactorAuth
from fastapi import (
    HTTPException,
    Request,
    Response,
    status
)
from starlette.middleware.base import BaseHTTPMiddleware


class TwoFactorMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Callable[
            [Request],
            Awaitable[Response]
        ],
        get_user_secret_callback: Callable[
            [str],
            Awaitable[Optional[str]]
        ],
        *,
        encryption_key: Optional[Union[str, bytes]] = None,
        excluded_paths: Optional[List[str]] = None,
        header_name: str = "X-2FA-Code"
    ):
        super().__init__(app)
        self.encryption_key = (
            encryption_key.encode()
            if isinstance(encryption_key, str)
            else encryption_key
        ) if encryption_key else None

        if self.encryption_key:
            try:
                Fernet(self.encryption_key)
            except ValueError as e:
                raise ValueError(f"Invalid encryption key: {str(e)}") from e

        self.get_user_secret = get_user_secret_callback
        self.excluded_paths = excluded_paths or ["/login", "/setup-2fa"]
        self.header_name = header_name

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[
            [Request],
            Awaitable[Response]
        ]
    ) -> Response:
        if any(request.url.path == path for path in self.excluded_paths):
            return await call_next(request)

        user = request.scope.get("user")
        if not user or not user.is_authenticated:
            return await call_next(request)

        encrypted_secret = await self.get_user_secret(str(user.id))

        if not encrypted_secret:
            return await call_next(request)

        try:
            user_secret = (
                TwoFactorAuth.decrypt_secret(
                    encrypted_secret,
                    self.encryption_key
                )
                if self.encryption_key
                else encrypted_secret
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

        two_fa_code = request.headers.get(self.header_name)
        auth = TwoFactorAuth(user_secret)
        if not two_fa_code or not auth.verify_code(two_fa_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing 2FA code"
            )

        return await call_next(request)
