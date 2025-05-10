import routes
from loader import app
from middlewaries import jwtMiddleware

app.middleware("http")(jwtMiddleware)