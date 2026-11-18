from collections.abc import Awaitable, Callable

from cryptography.fernet import Fernet
from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

from .core import TwoFactorAuth


class TwoFactorMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        get_user_secret_callback: Callable[[str], Awaitable[str | None]],
        *,
        encryption_key: str | bytes | None = None,
        excluded_paths: list[str] | None = None,
        header_name: str = "X-2FA-Code",
    ):
        super().__init__(app)
        self.encryption_key = self._normalize_encryption_key(encryption_key)
        self._validate_encryption_key()
        self.get_user_secret = get_user_secret_callback
        self.excluded_paths = excluded_paths or ["/login", "/setup-2fa"]
        self.header_name = header_name

    @staticmethod
    def _normalize_encryption_key(
        encryption_key: str | bytes | None,
    ) -> bytes | None:
        if not encryption_key:
            return None
        if isinstance(encryption_key, str):
            return encryption_key.encode()
        return encryption_key

    def _validate_encryption_key(self) -> None:
        if not self.encryption_key:
            return
        try:
            Fernet(self.encryption_key)
        except ValueError as e:
            raise ValueError(f"Invalid encryption key: {str(e)}") from e

    def _decrypt_user_secret(self, encrypted_secret: str) -> str:
        if not self.encryption_key:
            return encrypted_secret
        try:
            return TwoFactorAuth.decrypt_secret(
                encrypted_secret,
                self.encryption_key,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
            ) from e

    def _verify_two_fa_code(self, request: Request, user_secret: str) -> None:
        two_fa_code = request.headers.get(self.header_name)
        auth = TwoFactorAuth(user_secret)
        if not two_fa_code or not auth.verify_code(two_fa_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing 2FA code",
            )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        user = request.scope.get("user")
        if not user or not user.is_authenticated:
            return await call_next(request)

        encrypted_secret = await self.get_user_secret(str(user.id))
        if not encrypted_secret:
            return await call_next(request)

        user_secret = self._decrypt_user_secret(encrypted_secret)
        self._verify_two_fa_code(request, user_secret)
        return await call_next(request)
