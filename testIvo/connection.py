from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

# Diccionario Datos de Conexion
config_mysql = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_DATABASE"),
}


# Objeto Conexion
conexion_mysql = mysql.connector.connect(**config_mysql)

# Objeto cursor
cursor = conexion_mysql.cursor()

# Cerrar Conexion
def closeConnection():
    conexion_mysql.close()

# Diccionario Datos de Conexion
config_mysql_2 = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_DATABASE_2"),
}


# Objeto Conexion
conexion_mysql_2 = mysql.connector.connect(**config_mysql_2)

# Objeto cursor
cursor_2 = conexion_mysql_2.cursor()

# Cerrar Conexion
def closeConnection2():
    conexion_mysql_2.close()