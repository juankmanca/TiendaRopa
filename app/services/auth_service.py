from datetime import datetime, timedelta
import jwt

from app.repositories import auth_repo
from app.config import SECRET_KEY, JWT_EXP_HOURS


class AuthService:
    def login(self, email: str, password: str) -> dict | None:
        """Realiza login usando el repo y, si existe usuario, retorna un dict con token JWT."""
        user = auth_repo.login(email, password)
        if not user:
            return None

        token = self._create_token(user)
        return {"access_token": token}

    def crear_usuario(self, nombre: str, email: str, password: str, telefono: str | None = None, rol_id: int = 1) -> dict | None:
        """Crea usuario y devuelve token JWT (llama a sp_create_user y luego sp_login)."""
        res = auth_repo.create_user(nombre, email, password, telefono, rol_id)
        if not res:
            return None

        # obtener usuario completo para generar token
        user = auth_repo.login(email, password)
        if not user:
            return None

        token = self._create_token(user)
        return {"access_token": token}

    def _create_token(self, user: dict) -> str:
        exp = datetime.utcnow() + timedelta(hours=JWT_EXP_HOURS)
        payload = {
            "sub": user.get("UsuarioID"),
            "nombre": user.get("Nombre"),
            "email": user.get("Email"),
            "rol": user.get("RolID"),
            "exp": exp,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        # PyJWT >=2.0 returns str, but ensure string
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token
