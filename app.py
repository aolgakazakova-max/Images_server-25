from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    send_from_directory,
    url_for
)

from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

import logging
import uuid
import os


from io import BytesIO
from pathlib import Path



app = Flask(__name__)


# BASE DIRS
BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(os.getenv('IMAGES_DIR', str(BASE_DIR / 'images')))
LOGS_DIR = Path(os.getenv('LOGS_DIR', str(BASE_DIR / 'logs')))
print(IMAGES_DIR.resolve())
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# CONFIG
MAX_FILE_SIZE = 5 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE + 1 * 1024 * 1024


# FORMATS
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
def detect_image_extension(file_data: bytes):
    try:
        with Image.open(BytesIO(file_data)) as img:
            fmt = img.format
            img.verify()
            return ALLOWED_IMAGE_FORMATS.get(fmt)
    except (UnidentifiedImageError, OSError):
        return None


# ROUTES
@app.get('/')
def home():
    return render_template('index.html')


@app.get('/upload')
def upload_page():
    return render_template('upload.html')


@app.get('/images/')
def images_page():
    images = []

    for image_path in sorted(IMAGES_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not image_path.is_file():
            continue

        images.append({
            'name': image_path.name,
            'url': url_for('get_image', filename=image_path.name),
            'full_url': url_for('get_image', filename=image_path.name, _external=True)
        })

    return render_template('images.html', images=images)


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

    path = IMAGES_DIR / safe_filename
    path.write_bytes(file_data)

    # DEBUG: проверка что файл реально сохранился
    print("IMAGES CONTENT:")
    print(list(IMAGES_DIR.iterdir()))

    logging.info(f'Upload: {original_filename} -> {safe_filename}')

    return jsonify({
        'message': 'OK',
        'id': safe_filename,
        'url': url_for('get_image', filename=safe_filename),
        'full_url': url_for('get_image', filename=safe_filename, _external=True)
    }), 201


@app.post('/delete/<filename>')
def delete_image(filename):
    filename = secure_filename(filename)
    file_path = IMAGES_DIR / filename

    if file_path.exists() and file_path.is_file():
        file_path.unlink()
        logging.info(f'Deleted: {filename}')
        return jsonify({'message': 'deleted'}), 200

    return jsonify({'error': 'not found'}), 404


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(_):
    return jsonify({'error': 'Файл слишком большой (max 5MB)'}), 413


@app.get('/images/<path:filename>')
def get_image(filename):
    filename = secure_filename(filename)
    return send_from_directory(IMAGES_DIR, filename)




if __name__ == '__main__':


    app.run(host='0.0.0.0', port=3000, debug=True)