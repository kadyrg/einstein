from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

from .schemas import EmailSchema, RegisterSchema, TokenSchema, VerifySchema, LoginSchema
from models import User, OTP
from auth import password_manager, auth_manager
from utils.security import generate_otp_code
from utils import mail_manager
from core import settings


async def register(register_in: RegisterSchema, session: AsyncSession) -> EmailSchema:
    user_result = await session.execute(
        select(User).where(
            User.email==register_in.email
        )
    )

    user = user_result.scalar_one_or_none()

    if user and user.is_active:
        raise HTTPException(status_code=400, detail=f"User with {register_in.email} email already exists")

    password = password_manager.hash_password(register_in.password)

    if not user:
        user = User(
            email=register_in.email,
            first_name=register_in.first_name,
            last_name=register_in.last_name,
            password=password
        )
        session.add(user)

    if user:
        user.first_name=register_in.first_name
        user.last_name=register_in.last_name
        user.password=password
    
    code = generate_otp_code()
    
    otp_result = await session.execute(
        select(OTP).where(
            OTP.email==register_in.email,
            OTP.use_count<5,
            OTP.is_used==False
        )
    )

    valid_otp = otp_result.scalar_one_or_none()

    if valid_otp:
        session.delete(valid_otp)

    otp = OTP(
        email=register_in.email,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_VALIDITY)
    )

    session.add(otp)

    mail_manager.send_mail(register_in.email, code)
    
    await session.commit()

    return EmailSchema(
        email=register_in.email
    )


async def verify(verify_in: VerifySchema, session: AsyncSession) -> TokenSchema:
    otp_result = await session.execute(
        select(OTP).where(
            OTP.email==verify_in.email,
            OTP.expires_at>datetime.now(timezone.utc),
            OTP.use_count<5,
            OTP.is_used==False
        )
    )

    valid_otp = otp_result.scalar_one_or_none()

    if not valid_otp:
        raise HTTPException(status_code=400, detail="No email matches")
    
    if valid_otp.code!=verify_in.code:
        valid_otp.use_count+=1
        await session.commit()
        raise HTTPException(status_code=400, detail="Invalid code")
    
    user_result = await session.execute(
        select(User).where(
            User.email==verify_in.email,
            User.is_active==False
        )
    )

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    valid_otp.is_used=True
    valid_otp.use_count+=1

    user.is_active=True

    token = auth_manager.generate_token(user.id)

    await session.commit()

    return TokenSchema(
        token=token
    )


async def login(login_in: LoginSchema, session: AsyncSession) -> TokenSchema:
    result = await session.execute(
        select(User).where(
            User.email==login_in.email,
            User.is_active==True
        )
    )
    
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email")

    password = password_manager.verify_password(login_in.password, user.password)

    if not password:
        raise HTTPException(status_code=401, detail="Invalid password")

    token = auth_manager.generate_token(user.id)

    return TokenSchema(token=token)
