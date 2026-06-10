import os
from datetime import datetime

DB_NAME = os.getenv("DB_NAME", "images_db")
DB_USER = os.getenv("DB_USER", "postgres")
CONTAINER = "image_server_db"

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

filename = f"backups/backup_{timestamp}.sql"

os.system(
    f'docker exec -t {CONTAINER} pg_dump -U {DB_USER} {DB_NAME} > {filename}'
)

print("Backup created:", filename)