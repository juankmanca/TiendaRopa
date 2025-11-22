import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "tienda_user")
DB_PASS = os.getenv("DB_PASS", "user123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "tiendavirtualropa")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
# JWT / seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "4433552211")
# tiempo de expiración en horas para el token JWT
JWT_EXP_HOURS = int(os.getenv("JWT_EXP_HOURS", "2"))
