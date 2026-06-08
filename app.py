from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    send_from_directory,
    url_for,
    redirect
)

from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

import logging
import uuid
import os

from io import BytesIO
from pathlib import Path

from database.repository import (
    save_metadata,
    get_images,
    get_count_images,
    get_image_by_id,
    delete_image_by_id
)

print("TEMPLATE PATH:", os.path.join(os.getcwd(), "templates"))
app = Flask(__name__, template_folder="templates")


# BASE DIRS

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(
    os.getenv(
        'IMAGES_DIR',
        str(BASE_DIR / 'images')
    )
)

LOGS_DIR = Path(
    os.getenv(
        'LOGS_DIR',
        str(BASE_DIR / 'logs')
    )
)

IMAGES_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# CONFIG

MAX_FILE_SIZE = 5 * 1024 * 1024

app.config['MAX_CONTENT_LENGTH'] = (
    MAX_FILE_SIZE + 1024 * 1024
)

# ALLOWED FORMATS

ALLOWED_IMAGE_FORMATS = {
    'JPEG': 'jpg',
    'PNG': 'png',
    'GIF': 'gif'
}

# LOGGING

logging.basicConfig(
    filename=LOGS_DIR / 'app.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


# HELPERS

def detect_image_extension(
    file_data: bytes
) -> str | None:

    try:

        with Image.open(
            BytesIO(file_data)
        ) as img:

            image_format = img.format

            img.verify()

            return ALLOWED_IMAGE_FORMATS.get(
                image_format
            )

    except (
        UnidentifiedImageError,
        OSError
    ):
        return None


# ROUTES

@app.get('/')
def home():
    return render_template(
        'index.html'
    )


@app.get('/upload')
def upload_page():
    return render_template(
        'upload.html'
    )


@app.post('/upload')
def upload_image():

    uploaded_file = request.files.get(
        'image'
    )

    if not uploaded_file:
        return (
            jsonify(
                {
                    'error': 'Файл не найден'
                }
            ),
            400
        )

    original_filename = (
        uploaded_file.filename
        or 'unknown'
    )

    file_data = uploaded_file.read()

    if not file_data:

        return (
            jsonify(
                {
                    'error': 'Файл пустой'
                }
            ),
            400
        )

    if len(file_data) > MAX_FILE_SIZE:

        return (
            jsonify(
                {
                    'error': 'Максимум 5MB'
                }
            ),
            413
        )

    ext = detect_image_extension(
        file_data
    )

    if not ext:

        return (
            jsonify(
                {
                    'error': 'Только JPG, PNG, GIF'
                }
            ),
            400
        )

    filename = (
        f'{uuid.uuid4().hex}.{ext}'
    )

    safe_filename = secure_filename(
        filename
    )

    file_path = (
        IMAGES_DIR /
        safe_filename
    )

    file_path.write_bytes(
        file_data
    )

    try:

        save_metadata(
            filename=safe_filename,
            original_name=original_filename,
            size=len(file_data),
            file_type=ext
        )

    except Exception:

        file_path.unlink(
            missing_ok=True
        )

        logging.exception(
            'Ошибка сохранения в БД'
        )

        return (
            jsonify(
                {
                    'error':
                    'Ошибка при сохранении данных'
                }
            ),
            500
        )

    logging.info(
        'Upload: %s -> %s',
        original_filename,
        safe_filename
    )

    return (
        jsonify(
            {
                'message': 'OK',
                'id': safe_filename,
                'url': url_for(
                    'get_image',
                    filename=safe_filename
                ),
                'full_url': url_for(
                    'get_image',
                    filename=safe_filename,
                    _external=True
                )
            }
        ),
        201
    )


@app.post('/delete/<int:image_id>')
def delete_image(image_id):

    image = get_image_by_id(
        image_id
    )

    if not image:

        return (
            jsonify(
                {
                    'error':
                    'Изображение не найдено'
                }
            ),
            404
        )

    filename = image[1]

    file_path = (
        IMAGES_DIR /
        filename
    )

    try:

        if (
            file_path.exists()
            and
            file_path.is_file()
        ):
            file_path.unlink()

        delete_image_by_id(
            image_id
        )

        logging.info(
            'Удалено изображение id=%s',
            image_id
        )

        return redirect(
            url_for(
                'images_list'
            )
        )

    except Exception:

        logging.exception(
            'Ошибка удаления'
        )

        return (
            jsonify(
                {
                    'error':
                    'Ошибка удаления'
                }
            ),
            500
        )


@app.get('/images-list')
def images_list():

    page = max(
        request.args.get(
            'page',
            1,
            type=int
        ),
        1
    )

    per_page = 10

    offset = (
        page - 1
    ) * per_page

    total = get_count_images()

    rows = get_images(
        per_page=per_page,
        offset=offset
    )

    images = []

    for row in rows:

        images.append(
            {
                'id': row[0],
                'filename': row[1],
                'original_name': row[2],
                'size': row[3],
                'upload_time': row[4],
                'file_type': row[5],
                'url': url_for(
                    'get_image',
                    filename=row[1]
                )
            }
        )

    total_pages = (
        total + per_page - 1
    ) // per_page

    return render_template(
        'images_list.html',
        images=images,
        page=page,
        total_pages=total_pages
    )


@app.get('/images/<path:filename>')
def get_image(filename):

    filename = secure_filename(
        filename
    )

    return send_from_directory(
        IMAGES_DIR,
        filename
    )


@app.errorhandler(
    RequestEntityTooLarge
)
def handle_large_file(_):

    return (
        jsonify(
            {
                'error':
                'Файл слишком большой (max 5MB)'
            }
        ),
        413
    )


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000, debug=True)