from typing import Any, List, Tuple
import logging

from database.db import get_connection


def save_metadata(
    filename: str,
    original_name: str,
    size: int,
    file_type: str
) -> None:

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO images (
                        filename,
                        original_name,
                        size,
                        file_type
                    )
                    VALUES (%s, %s, %s, %s)
                """

                cursor.execute(
                    sql,
                    (filename, original_name, size, file_type)
                )


            conn.commit()

        logging.info(
            "Метаданные файла %s успешно сохранены",
            filename
        )

    except Exception:
        logging.exception(
            "Ошибка при сохранении метаданных файла %s",
            filename
        )
        raise


def get_images(per_page: int, offset: int) -> List[Tuple[Any, ...]]:

    try:
        with get_connection() as conn:

            with conn.cursor() as cursor:
                sql = """
                    SELECT
                        id,
                        filename,
                        original_name,
                        size,
                        upload_time,
                        file_type
                    FROM images
                    ORDER BY upload_time DESC
                    LIMIT %s OFFSET %s
                """

                cursor.execute(sql, (per_page, offset))
                rows = cursor.fetchall()

        return rows

    except Exception:
        logging.exception(
            "Ошибка получения изображений из БД"
        )
        raise


def get_count_images() -> int:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM images"
                )
                total = cursor.fetchone()[0]

        return total

    except Exception:
        logging.exception(
            "Ошибка получения количества изображений"
        )
        raise

def get_image_by_id(image_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        id,
                        filename,
                        original_name,
                        size,
                        upload_time,
                        file_type
                    FROM images
                    WHERE id = %s
                    """,
                    (image_id,)
                )

                return cursor.fetchone()

    except Exception:
        logging.exception(
            "Ошибка получения изображения по id=%s",
            image_id
        )
        raise


def delete_image_by_id(image_id: int) -> None:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM images
                    WHERE id = %s
                    """,
                    (image_id,)
                )

            conn.commit()

        logging.info(
            "Изображение id=%s удалено из БД",
            image_id
        )

    except Exception:
        logging.exception(
            "Ошибка удаления изображения id=%s",
            image_id
        )
        raise