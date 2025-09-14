from db import get_connection


class Usuario:
    @staticmethod
    def crear(username, password_hash):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (username, password)
                    VALUES (%s, %s)
                """, (username, password_hash))
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_username(username):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id, username, password FROM usuarios WHERE username=%s", (username,))
                return cursor.fetchone()
        finally:
            conexion.close()
