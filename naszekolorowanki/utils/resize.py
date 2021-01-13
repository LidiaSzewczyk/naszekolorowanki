from PIL import Image
import os


path = os.path.abspath(os.path.dirname(__file__))
resized_path = os.path.join(path, '..', 'uploaded_pictures', 'resized')
# path = "D:/.../.../.../resized/"
# dirs = os.listdir(path)

def resize(item):
    # if item == '.jpg':
    #     continue
    if os.path.isfile(item):
        image = Image.open(item)
        file_path, extension = os.path.splitext(item)

        size = image.size

        new_image_height = 190
        new_image_width = int(size[1] / size[0] * new_image_height)

        image = image.resize((new_image_height, new_image_width), Image.ANTIALIAS)
        image.save(file_path + "_small" + extension, 'JPEG', quality=90)


resize('/home/lidka/projects/python/naszekolorowanki/naszekolorowanki/uploaded_pictures/20210110T202045lidkaaf_IMG_20210102_135051.jpg')
