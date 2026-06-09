import psycopg
import os

def get_connection():
    return psycopg.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        dbname=os.getenv('DB_NAME'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT')
    )