import os
import dj_database_url
from DietTracker.settings import *

DATABASES = {
    "default": dj_database_url.config(
        default='postgres://bmkvaujwsilfcd:d50e5f1ba7c391c0708e21ac5b2747c903eab5fce1d49ba2ac9aa4d8edd20116@ec2-44-208-88-195.compute-1.amazonaws.com:5432/d13dggive4g2mb'
)
}
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