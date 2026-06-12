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

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__, template_folder="templates")


BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(os.getenv('IMAGES_DIR', str(BASE_DIR / 'images')))
LOGS_DIR = Path(os.getenv('LOGS_DIR', str(BASE_DIR / 'logs')))

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


MAX_FILE_SIZE = 5 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE + 1024 * 1024

ALLOWED_IMAGE_FORMATS = {
    'JPEG': 'jpg',
    'PNG': 'png',
    'GIF': 'gif'
}


logging.basicConfig(
    filename=LOGS_DIR / 'app.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


def detect_image_extension(file_data: bytes):
    try:
        with Image.open(BytesIO(file_data)) as img:
            fmt = img.format
            img.verify()
            return ALLOWED_IMAGE_FORMATS.get(fmt)
    except (UnidentifiedImageError, OSError):
        return None




@app.get('/')
def home():
    return render_template('index.html')


@app.get('/upload')
def upload_page():
    return render_template('upload.html')




@app.get('/images/')
def images_page():

    images = []

    for image_path in sorted(
        IMAGES_DIR.iterdir(),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    ):
        if not image_path.is_file():
            continue

        images.append({
            "id": image_path.name,
            "name": image_path.name,
            "url": url_for('get_image', filename=image_path.name),
            "full_url": url_for('get_image', filename=image_path.name, _external=True)
        })

    return render_template('images.html', images=images)


@app.post('/delete/<image_id>')
def delete_image_filesystem(image_id):

    file_path = IMAGES_DIR / image_id

    if not file_path.exists():
        return jsonify({"error": "Файл не найден"}), 404

    try:
        file_path.unlink()
        logging.info("Deleted file: %s", image_id)
        return redirect(url_for('images_page'))

    except Exception:
        logging.exception("Filesystem delete error")
        return jsonify({"error": "Ошибка удаления"}), 500




@app.get('/images-list')
def images_list():

    page = max(request.args.get('page', 1, type=int), 1)
    per_page = 10
    offset = (page - 1) * per_page

    total_images = get_count_images()
    rows = get_images(per_page=per_page, offset=offset)

    images = [
        {
            "id": r[0],
            "filename": r[1],
            "original_name": r[2],
            "size": r[3],
            "upload_time": r[4],
            "file_type": r[5],
            "url": f"http://localhost:8080/images/{r[1]}"
        }
        for r in rows
    ]

    total_pages = max((total_images + per_page - 1) // per_page, 1)

    return render_template(
        'images_list.html',
        images=images,
        page=page,
        total_pages=total_pages,
        total_images=total_images
    )


@app.post('/delete/db/<int:image_id>')
def delete_image_db(image_id):

    image = get_image_by_id(image_id)

    if not image:
        return jsonify({"error": "Изображение не найдено"}), 404

    filename = image[1]
    file_path = IMAGES_DIR / filename

    try:
        if file_path.exists():
            file_path.unlink()

        delete_image_by_id(image_id)

        logging.info("Deleted DB image id=%s", image_id)

        return redirect(url_for('images_list'))

    except Exception:
        logging.exception("DB delete error")
        return jsonify({"error": "Ошибка удаления"}), 500




@app.post('/upload')
def upload_image():

    uploaded_file = request.files.get('image')

    if not uploaded_file:
        return jsonify({'error': 'Файл не найден'}), 400

    original_filename = uploaded_file.filename or 'unknown'
    file_data = uploaded_file.read()

    if not file_data:
        return jsonify({'error': 'Файл пустой'}), 400

    if len(file_data) > MAX_FILE_SIZE:
        return jsonify({'error': 'Максимум 5MB'}), 413

    ext = detect_image_extension(file_data)

    if not ext:
        return jsonify({'error': 'Только JPG, PNG, GIF'}), 400

    filename = f"{uuid.uuid4().hex}.{ext}"
    safe_filename = secure_filename(filename)

    file_path = IMAGES_DIR / safe_filename
    file_path.write_bytes(file_data)

    try:
        save_metadata(
            filename=safe_filename,
            original_name=original_filename,
            size=len(file_data),
            file_type=ext
        )
    except Exception:
        file_path.unlink(missing_ok=True)
        logging.exception("DB save error")
        return jsonify({'error': 'Ошибка БД'}), 500

    return jsonify({
        "id": safe_filename,
        "url": f"http://localhost:8080/images/{safe_filename}",
        "full_url": f"http://localhost:8080/images/{safe_filename}"
    }), 201




@app.get('/images/<path:filename>')
def get_image(filename):
    filename = secure_filename(filename)
    return send_from_directory(IMAGES_DIR, filename)



@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(_):
    return jsonify({'error': 'Файл слишком большой (max 5MB)'}), 413



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)