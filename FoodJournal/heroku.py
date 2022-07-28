import os
import dj_database_url
from DietTracker.settings import *

'''DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL")
)
}'''
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

DEBUG=False
TEMPLATE_DEBUG=False
STATIC_ROOT=os.path.join(BASE_DIR, "static")
SECRET_KEY=os.environ.get("SECRET_KEY")
ALLOWED_HOSTS=["*"]

MIDDLEWARE = (
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *MIDDLEWARE,
)