import mysql.connector
from mysql.connector import Error
import time
from contextlib import contextmanager
from src.config import Config

def get_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

def get_connection_with_retry(max_retries=30, delay=2):
    for attempt in range(max_retries):
        try:
            conn = get_connection()
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Attente BDD ({attempt+1}/{max_retries})...")
            time.sleep(delay)
    raise Exception("Connexion BDD impossible")

@contextmanager
def database_connection():
    conn = get_connection_with_retry()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()