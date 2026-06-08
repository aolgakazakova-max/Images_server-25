import psycopg
import os

def get_connection():
    return psycopg.connect(
        host=os.getenv('DB_HOST', 'db'),
        user=os.getenv('DB_USER', 'postgres'),
        dbname=os.getenv('DB_NAME', 'images_db'),
        password=os.getenv('DB_PASSWORD', 'password'),
        port=int(os.getenv('DB_PORT', '5432'))
    )