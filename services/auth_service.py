import bcrypt
from models.usuario_model import Usuario


class AuthService:
    def login(self, username, password):
        """
        Verifica usuario y contraseña.
        Retorna el id del usuario si es válido, None si no.
        """
        user = Usuario.obtener_por_username(username)

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            return user["id"]

        return None

    def registrar_usuario(self, username, password):
        """
        Crea un nuevo usuario con contraseña encriptada.
        """
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        Usuario.crear(username, password_hash)
