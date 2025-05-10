from fastapi import Request, status, Response
from loader import AdapterDB

from jwt import PyJWTError

from misc import problemResponse
from auth import verifyToken
from loader import AdapterDB
from typing import Any, Callable
from config import ALLOWED_ENDPOINTS_WITHOUT_AUTH


async def jwtMiddleware(request: Request, call_next: Callable[[Request], Any]) -> Response:
    """Middleware для JWT аутентификации

    :param request: HTTP-запрос
    :type request: Request
    :param call_next: Следующий обработчик
    :type call_next: Callable[[Request], Any]
    :return: Ответ приложения или ошибка аутентификации
    :rtype: Response
    """
    if request.url.path in ALLOWED_ENDPOINTS_WITHOUT_AUTH:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return problemResponse(detail="Missing authorization header", status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(" ")[1]
    try:
        payload = verifyToken(token)
        username = payload.get("sub")
        if not username:
            return problemResponse(detail="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
        
        request.state.user = await AdapterDB.getUser(username)
        if not request.state.user:
            return problemResponse(detail="User not found", status_code=status.HTTP_401_UNAUTHORIZED)
    
    except PyJWTError as e:
        return problemResponse(detail=str(e), status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return problemResponse(detail=str(e), status_code=status.HTTP_401_UNAUTHORIZED)
    
    return await call_next(request)