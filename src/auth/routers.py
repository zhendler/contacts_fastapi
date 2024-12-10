from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.auth.path_utils import verify_password
from src.auth.mail_auth import send_verification
from src.auth.repos import UserRepository
from src.auth.schema import UserResponse, UserCreate, Token
from src.auth.utils import create_access_token, create_refresh_token, decode_access_token, decode_verification_token, \
    create_verification_token

router = APIRouter()
env = Environment(loader=FileSystemLoader("src/templates"))

@router.post("/register", response_model=UserResponse)
async def register(
    user_create: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user = await user_repo.create_user(user_create)
    verification_token = create_verification_token(user.email)
    verification_link = (
        f"http://localhost:8000/auth/verify-email?token={verification_token}"
    )
    template = env.get_template("verification_email.html")
    email_body = template.render(verification_link=verification_link)
    background_tasks.add_task(send_verification, user.email, email_body)
    return user


@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    email: str = decode_verification_token(token)
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await user_repo.activate_user(user)
    return {"msg": "Email verified successfully"}


@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", status_code=status.HTTP_201_CREATED, response_model=Token)
async def refresh_tokens(refresh_token: str, db: AsyncSession = Depends(get_db)):
    token_data = decode_access_token(refresh_token)
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_username(token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )