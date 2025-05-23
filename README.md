# 🚀 Simple Order and Delivery Management System with JWT Authorization 🚚

REST API для управления заказами с JWT-аутентификацией

## 🌟 Особенности системы

- 🔑 Аутентификация через JWT (алгоритм HS256)
- 🛡️ Защита паролей: PBKDF2 HMAC-SHA256 (10k итераций)
- 📦 Полный CRUD для заказов и доставок
- 📅 Валидация временных меток
- 🚦 HTTP-статусы для всех операций
- 📊 Детализированные ошибки в JSON-формате

## 🛠 Технологический стек

| Технология         | Назначение                          |
|---------------------|-------------------------------------|
| FastAPI             | backend-фреймворк                    |
| Pydantic v2         | Валидация данных и схемы           |
| JWT (HS256)         |  Аутентификация          |
| PBKDF2-HMAC-SHA256  | Хеширование паролей                |

## 📡 REST API Endpoints 

### 🔐 Authentication Endpoints

#### Login - получение токенов
`POST /auth/login`

| **Параметр**  | **Тип** | **Обязательный** | **Описание**         |
|---------------|---------|------------------|----------------------|
| username      | string  | ✅               | Логин пользователя  |
| password      | string  | ✅               | Пароль пользователя |

**Ответы:**

| Код | Статус        | Описание                          |
|-----|---------------|-----------------------------------|
| 202  | Created       | Успешный вход 🎉          |
| 400 | Bad Request   | Неправильный ввод пароля/логина ❌ |

---

### Register (Регистрация)
`POST /auth/register`

| **Параметр**  | **Тип** | **Обязательный** | **Описание**         |
|---------------|---------|------------------|----------------------|
| username      | string  | ✅               | Логин пользователя  |
| password      | string  | ✅               | Пароль пользователя |

**Ответы:**

| Код | Статус        | Описание                          |
|-----|---------------|-----------------------------------|
| 201 | Created       | Успешная регистрация 🎉          |
| 400 | Bad Request   | Нарушение правил пароля/логина ❌ |
| 400 | Bad Request      | Пользователь уже существует ⚠️   |

## 🚛 Delivery Management Endpoints
### Обновление данных доставки  
`PATCH /deliveries/{order_id}`  

| Параметр  | Тип  | Описание          |
|-----------|------|-------------------|
| Status  | String  | Статус для заказа        |
| TargetTimeDelivery | DateTime | Ожидаемое время доставки  |

**Ответы:**

| Код  | Статус           | Описание                      |
|------|------------------|-------------------------------|
| 200  | OK               | Успешное обновление ✅        |
| 404  | Not Found        | Заказ не найден 🔍           |
| 422  | Validation Error | Ошибка валидации ❗           |
| 401 | Unauthorized  | Требуется авторизация 🔒         |

---

### Создание заказа  
`POST /orders`  

| Параметр  | Тип  | Обязательно | Описание          |
|-----------|------|-------------|-------------------|
| order_id  | int  | ✅   | ID заказа        |
| name | String |  ✅  | Имя заказа |
| pickUpAddress |  String | ✅  | Начальный адрес |
| deliveryAddress | String | ✅  | Адрес доставки |
| weight | int | ✅  | Вес |
| dimensions | String | ✅  | Размеры | 
| description | String | ❌ | Описание |

**Ответы:**  

| Код | Статус        | Описание                          |
|-----|---------------|-----------------------------------|
| 201 | Created       | Успешно создан 🎉                |
| 400 | Bad Request   | Нарушение правил валидации ❌    |
| 401 | Unauthorized  | Требуется авторизация 🔒         |

---

### Получение информации о заказе  
`GET /orders/{order_id}`  

**Ответы:**  

| Код | Статус        | Описание                          |
|-----|---------------|-----------------------------------|
| 200 | Created       | Успешно 🎉                |
| 404 | Not found   | Заказ не найден ❌    |
| 401 | Unauthorized  | Требуется авторизация 🔒         |

---

### Удаление заказа
`DELETE /orders/{order_id}`  

**Ответы:**  

| Код | Статус        | Описание                          |
|-----|---------------|-----------------------------------|
| 200 | Created       | Успешно 🎉                |
| 404 | Not found   | Заказ не найден ❌    |
| 401 | Unauthorized  | Требуется авторизация 🔒         |

## 🚀 Быстрый запуск

### Требования
- Python 3.10+
- pip

### Установка
```bash
# Клонировать репозиторий
git clone https://github.com/loffiecode/delivery-jwt-api.git
cd delivery-jwt-api
# Установить зависимости
pip install -r requirements.txt
```
### Конфигурация 
```bash
cd delivery-jwt-api
nano config.py
```

#### 🔧 Конфигурационные параметры

| Параметр                          | Значение по умолчанию              | Описание                          |
|-----------------------------------|-------------------------------------|-----------------------------------|
| `DATABASE_URL`                    | `postgresql+asyncpg://user:pass@host/db`   | Путь к базе данных 🗄️           |
| `SECRET_KEY_JWT`                  | `"secret"`                         | Ключ для подписи JWT 🔐         |
| `ALGORITHM`                       | `HS256`                            | Алгоритм шифрования токенов 🛡️  |
| `ACCESS_EXPIRE`                   | `1800`                             | Время жизни access-токена ⏳    |
| `PROHIBITED_DATA_UPDATE_DELIVERY` | `("ID", "DeliveryID")`            | Read-only поля обновления доставки 🚫      |
| `ALLOWED_ENDPOINTS_WITHOUT_AUTH`  | `("/auth/login", ...)`            | Публичные эндпоинты без авторизации 🌐         |

### Запуск
```bash
uvicorn main:app --port 8000
```
