from typing import (
    Awaitable,
    Callable,
    List,
    Optional
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
        excluded_paths: Optional[List[str]] = None,
        header_name: str = "X-2FA-Code"
    ):
        super().__init__(app)
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

        # Get authenticated user from FastAPI Users context
        user = request.scope.get("user")
        if not user or not user.is_authenticated:
            return await call_next(request)

        # Get the user's 2FA secret
        user_secret = await self.get_user_secret(str(user.id))

        # If no secret, skip 2FA
        if not user_secret:
            return await call_next(request)

        # Verify 2FA code
        two_fa_code = request.headers.get(self.header_name)
        if not two_fa_code or not TwoFactorAuth(user_secret).verify_code(two_fa_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing 2FA code"
            )

        return await call_next(request)
