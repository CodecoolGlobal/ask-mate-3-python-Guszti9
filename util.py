import os
from werkzeug.utils import secure_filename
from markupsafe import Markup
import bcrypt


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


def marking(dictionary, search_phrase):
    dictionary['message'] = dictionary['message'].casefold()
    dictionary['message'] = Markup(dictionary['message'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
    dictionary['title'] = dictionary['title'].casefold()
    dictionary['title'] = Markup(dictionary['title'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))


def upload_image(image):
    if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))


def delete_image(image_name):
    os.remove(os.path.join(UPLOAD_FOLDER, image_name))


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
