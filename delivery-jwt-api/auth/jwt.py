from jwt import (
    decode,
    encode,
    ExpiredSignatureError,
    InvalidTokenError
)
from fastapi import HTTPException, status
from datetime import datetime, timezone

from typing import Dict, Any

from config import ACCESS_EXPIRE, ALGORITHM, SECRET_KEY_JWT 


def createTokens(username: str) -> Dict[str, str]:
    """Создает JWT токен доступа для аутентификации пользователя

    :param username: Имя пользователя для включения в токен
    :type username: str
    :return: Словарь с токеном JWT
    :rtype: Dict[str, str]
    """
    access_payload = {
        "type": "access",
        "sub": username,
        "exp": datetime.now(timezone.utc) + ACCESS_EXPIRE
    }
    
    return {
        "access_token": encode(access_payload, SECRET_KEY_JWT, ALGORITHM)
    }

def verifyToken(token: str) -> Dict[str, Any]:
    """Проверяет и декодирует JWT токен

    :param token: JWT токен для верификации
    :type token: str
    :raises HTTPException: Если токен просрочен или невалиден
    :return: Декодированный payload
    :rtype: Dict[str, Any]
    """
    try:
        payload = decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(detail="Token expired", status_code=status.HTTP_400_BAD_REQUEST)
    except InvalidTokenError:
        raise HTTPException(detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)