import bcrypt
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2805",
    database="db_motor"
)
cursor = conexion.cursor()

usuario = "admin"
password = "1234".encode("utf-8")
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

cursor.execute("INSERT IGNORE INTO usuarios (username, password) VALUES (%s, %s)", (usuario, hashed.decode("utf-8")))
conexion.commit()

cursor.close()
conexion.close()
