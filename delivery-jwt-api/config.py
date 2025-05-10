from datetime import timedelta

PROHIBITED_DATA_UPDATE_DELIVERY = ('ID', 'DeliveryID')
DATABASE_URL = 'sqlite+aiosqlite:///example.db'
SECRET_KEY_JWT = 'jwt_key'
ALGORITHM = "HS256"
ACCESS_EXPIRE = timedelta(minutes=30)
ALLOWED_ENDPOINTS_WITHOUT_AUTH = ("/auth/login", "/auth/register", "/docs", "/openapi.json")