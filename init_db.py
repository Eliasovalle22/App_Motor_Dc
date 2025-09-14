import bcrypt
from db import get_connection

# ============================
# CREAR TABLAS
# ============================
def crear_tablas():
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            # Tabla usuarios
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Tabla acciones (control de motor/LEDs)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS acciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                dispositivo ENUM('MOTOR', 'LED_VERDE', 'LED_ROJO') NOT NULL,
                accion ENUM('ENCENDER', 'APAGAR') NOT NULL,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            );
            """)

        conexion.commit()
        print("✅ Tablas creadas correctamente.")
    finally:
        conexion.close()


# ============================
# CREAR USUARIO ADMIN
# ============================
def crear_usuario_admin():
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            usuario = "admin"
            password = "1234".encode("utf-8")
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())

            cursor.execute("""
                INSERT IGNORE INTO usuarios (username, password)
                VALUES (%s, %s)
            """, (usuario, hashed.decode("utf-8")))

        conexion.commit()
        print("✅ Usuario admin creado (si no existía).")
    finally:
        conexion.close()


# ============================
# MAIN
# ============================
if __name__ == "__main__":
    crear_tablas()
    crear_usuario_admin()