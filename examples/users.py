"""
FastAPI Users setup for the examples (JWT bearer authentication).

Set the JWT_SECRET environment variable before starting an example.
"""

import os
import uuid
from collections.abc import AsyncGenerator
from typing import Annotated

from database import User, get_user_db
from fastapi import Depends
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    UUIDIDMixin,
    schemas,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    pass


async def get_user_manager(
    user_db: Annotated[SQLAlchemyUserDatabase[User, uuid.UUID], Depends(get_user_db)],
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    # Read at request time so importing this module needs no environment
    return JWTStrategy(secret=os.environ["JWT_SECRET"], lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
