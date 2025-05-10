from fastapi.responses import JSONResponse

from binascii import hexlify
from hashlib import pbkdf2_hmac

from os import urandom
from typing import Any


def problemResponse(
    status_code: int,
    detail: Any,
    title: str = "Invalid request",
    **kwargs: Any
) -> JSONResponse:
    """Формирует JSON-ответ для ошибок

    :param status_code: HTTP Status code
    :type status_code: int
    :param detail: Детали ошибки
    :type detail: str
    :param title: Ошибка, defaults to "Invalid request"
    :type title: str, optional
    :return: JSON ответ
    :rtype: JSONResponse
    """
    problem_data = {
        "success": False,
        "data": {
            "error": title,
            "detail": detail
        }
    }
    problem_data.update(kwargs)
    return JSONResponse(
        content=problem_data,
        status_code=status_code,
        media_type="application/problem+json"
    )

def successResponse(
    status_code: int,
    **kwargs
) -> JSONResponse:
    """Формирует стандартизированный JSON-ответ для успешных операций

    :param status_code: HTTP Status code
    :type status_code: int
    :return: JSON ответ
    :rtype: JSONResponse
    """
    return JSONResponse(
        content={"success": True, "data": kwargs},
        status_code=status_code,
        media_type="application/json"
    )

def generateSalt() -> str:
    """Генерирует salt для хеширования паролей

    :return: Salt в формате hex
    :rtype: str
    """
    return hexlify(urandom(32)).decode()

def hashPassword(password: str, salt: str) -> str:
    """Вычисляет хеш пароля с использованием PBKDF2-HMAC-SHA256

    :param password: Пароль пользователя
    :type password: str
    :param salt: Salt для создания пароля в hex формате
    :type salt: str
    :return: Пароль в hex формате
    :rtype: str
    """
    iterations = 10000
    return pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations,
        dklen=128
    ).hex()