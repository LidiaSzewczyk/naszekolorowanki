import os
from datetime import datetime
from secrets import token_hex

from werkzeug.utils import secure_filename

path = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(path, '..', 'uploaded_pictures')


def save_image(image, username):
    now = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    random_string = token_hex(1)

    filename = now + username + '_' + random_string + "_" + image.data.filename
    filename = secure_filename(filename)
    image.data.save(os.path.join(upload_path, filename))
    return filename
