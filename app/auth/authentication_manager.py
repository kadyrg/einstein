import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone

from core import settings
from db import db_helper
from models import User


security = HTTPBearer()


class AuthManager:
    secret_key = settings.SECRET_KEY
    algorithm = settings.ALGORITHM
    token_validity = settings.TOKEN_VALIDITY


    @classmethod
    def generate_token(cls, user_id: int) -> str:
        expiration_date = datetime.now(timezone.utc) + timedelta(days=settings.TOKEN_VALIDITY)
        payload = {
            "sub": str(user_id),
            "exp": expiration_date
        }
        token = jwt.encode(
            payload,
            cls.secret_key,
            algorithm=cls.algorithm
        )
        return token
    

    @classmethod
    async def student_auth(
        cls,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> User:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            user_id = payload.get("sub")
            result = await session.execute(
                select(User).where(
                    User.id==int(user_id),
                    User.type=="student",
                    User.is_active==True
                )
            )
            student = result.scalar_one_or_none()
            if not student:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            return student
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")


    @classmethod
    async def admin_auth(
        cls,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(db_helper.get_scoped_session),
    ):
        try:
            token = credentials.credentials
            payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            user_id = payload.get("sub")
            result = await session.execute(
                select(User).where(
                    User.id==int(user_id),
                    User.type=="admin",
                    User.is_active==True
                )
            )
            admin = result.scalar_one_or_none()

            if not admin:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")


auth_manager = AuthManager()
