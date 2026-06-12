import os
import subprocess
from datetime import datetime


DB_NAME = os.getenv("DB_NAME", "images_db")
DB_USER = os.getenv("DB_USER", "postgres")
CONTAINER = "image_server_db"

BACKUP_DIR = "backups"


os.makedirs(BACKUP_DIR, exist_ok=True)


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}.sql")

print(f"Creating backup: {backup_path}")


try:
    with open(backup_path, "w", encoding="utf-8") as f:
        subprocess.run(
            [
                "docker", "exec", CONTAINER,
                "pg_dump", "-U", DB_USER, DB_NAME
            ],
            stdout=f,
            stderr=subprocess.PIPE,
            check=True
        )

    print("backup created successfully!")

except subprocess.CalledProcessError as e:
    print(" Backup failed!")
    print(e.stderr.decode("utf-8", errors="ignore"))