import pyodbc
import time

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=100.109.91.46,1433;"
    "DATABASE=TiendaVideojuegosDB;"
    "UID=lider_dba2;"
    "PWD=PasswordSeguroDBA123!;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=5;"
)

print("Intentando conectar con pyodbc...")
start = time.time()
try:
    conn = pyodbc.connect(conn_str)
    print(f"¡Conectado en {time.time() - start:.2f} segundos!")
    conn.close()
except Exception as e:
    print(f"Error tras {time.time() - start:.2f} segundos: {e}")