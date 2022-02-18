from datetime import datetime
from secrets import token_hex

from flask import current_app
from werkzeug.utils import secure_filename

import os
import PIL
from PIL import Image


def save_resize_image(image, author):
    now = datetime.utcnow().strftime("%y%m%dT%H%M")
    random_string = token_hex(1)

    filename = now + author + random_string + "_" + image.data.filename
    filename = secure_filename(filename)
    file_path = os.path.join(current_app.config["IMAGE_UPLOADS"], filename)
    image.data.save(file_path)

    target_size = [300, 1920]
    file_list = []
    orig_img = Image.open(file_path)

    for basewidth in target_size:
        img = orig_img
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)

        identificator = "t" if basewidth == target_size[0] else 'i'
        new_filename = filename.rsplit('.', 1)[0] + '_' + str(basewidth) + identificator + '.' + \
                       filename.rsplit('.', 1)[1]
        new_path = current_app.config["THUMBNAIL"] if basewidth == target_size[0] else current_app.config[
            "IMAGE_RESIZED"]

        new_filepath = os.path.join(new_path, new_filename)
        file_list.append(new_filename)
        img.save(new_filepath)
    os.remove(file_path)

    return file_list
