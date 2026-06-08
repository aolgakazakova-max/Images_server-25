
from database.db import get_connection


def create_images():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            filename VARCHAR (100) NOT NULL UNIQUE,
            original_name VARCHAR (100) NOT NULL,
            size INTEGER NOT NULL,
            upload_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            file_type VARCHAR (10) NOT NULL
            );     
                       
            ''')
            conn.commit()
            return 'Таблица создалась'

if __name__ == '__main__':

    print(create_images())