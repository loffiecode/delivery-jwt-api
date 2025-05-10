from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from loader import AdapterDB, app

from misc import hashPassword, problemResponse, successResponse
from models import UserCreate, UserBase
from auth.jwt import createTokens


@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    """Авторизация и получение токенов для пользователей

    :param form_data: username и password, defaults to Depends()
    :type form_data: OAuth2PasswordRequestForm, optional
    :return: Ответ в JSON формате
    :rtype: JSONResponse
    """
    user = await AdapterDB.getUser(form_data.username)
    if not user or hashPassword(form_data.password, user.Salt) != user.Password:
        return problemResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            title="Authentication failed",
            detail="Invalid credentials"
        )
    
    tokens = createTokens(user.Username)
    return successResponse(
        result=tokens,
        status_code=status.HTTP_202_ACCEPTED,
    )
    
@app.post("/auth/register", response_model=UserBase)
async def register(user_data: UserCreate) -> JSONResponse:
    """Регистрация новых пользователей

    :param user_data: username, password пользователя
    :type user_data: UserCreate
    :return: Ответ в формате JSON
    :rtype: JSONResponse
    """
    errors = []
    if not 3 < len(user_data.username) < 32:
        errors.append({
            "title": "Invalid username",
            "detail": "Username must be between 4 and 32 characters long."
        })
    if not 8 < len(user_data.password) < 128:
        errors.append({
            "title": "Invalid password",
            "detail": "Password must be between 8 and 128 characters long."
        })
    if not errors:
        existing_user = await AdapterDB.getUser(user_data.username)
        if existing_user:
            errors.append({
                "title": "User exists",
                "detail": "User already exists."
            })
    if errors:
        return problemResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errors
        )
    await AdapterDB.createUser(user_data.username, user_data.password)
    return successResponse(status_code=status.HTTP_201_CREATED, username=user_data.username)