from db import get_connection


class Accion:
    @staticmethod
    def registrar(usuario_id, dispositivo, accion):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO acciones (usuario_id, dispositivo, accion)
                    VALUES (%s, %s, %s)
                """, (usuario_id, dispositivo, accion))
            conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_usuario(usuario_id):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT id, dispositivo, accion, fecha_hora
                    FROM acciones
                    WHERE usuario_id=%s
                    ORDER BY fecha_hora DESC
                """, (usuario_id,))
                return cursor.fetchall()
        finally:
            conexion.close()
