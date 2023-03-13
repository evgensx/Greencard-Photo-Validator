from os.path import getsize, getmtime
from os import remove as rm
from datetime import datetime as dt
from datetime import timedelta
from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt
import re
# from ctypes import windll
from logging import log


def get_image_object(image_path):
    return Image.open(image_path)


def get_image_qt(image_pil):
    return ImageQt(image_pil)


def get_mirror_image(image):
    return ImageOps.mirror(image)


def image_width(image):
    width = image.width
    if 600 <= width <= 1200:
        result = True
    else:
        result = False
    return result, str(width)


def image_height(image):
    height = image.height
    if 600 <= height <= 1200:
        result = True
    else:
        result = False
    return result, str(height)


def get_aspect_ratio(image):
    width, height = image.size
    aspect_ratio = width / height
    if aspect_ratio == 1.0:
        return True, "Да"
    else:
        return False, "Нет"


def file_size(file_path):
    size = getsize(file_path) / 1024
    if size < 240.0:
        result = True
    else:
        result = False
    return result, f"{size:.2f}"


def image_format(image):
    frmt = image.format
    if frmt == 'JPEG':
        result = True
    else:
        result = False
    return result, frmt


def image_color_depth(image):
    color_depth = image.mode

    if color_depth == '1':
        bits_per_pixel = '1'
        result = False
    elif color_depth == 'L':
        bits_per_pixel = '8'
        result = False
    elif color_depth == 'P':
        bits_per_pixel = '8'
        result = False
    elif color_depth == 'RGB':
        bits_per_pixel = '24'
        result = True
    elif color_depth == 'RGBA':
        bits_per_pixel = '32'
        result = False
    else:
        result = None
        bits_per_pixel = 'Unknown'
    return result, bits_per_pixel


def icc_profile(image):
    try:
        icc: bytes = re.sub(b'\x00', b'', image.info.get('icc_profile'))
    except TypeError:
        return None, 'Unknown'
    if b'sRGB' and b'Google' in icc:
        return True, 'sRGB G'
    elif b'sRGB IEC61966-2.1' in icc:
        return True, 'sRGB'
    elif b'Adobe RGB' in icc:
        return False, 'Adobe RGB'


def file_date(file_path):
    now_date = dt.now()
    date_image = dt.fromtimestamp(getmtime(file_path))
    delta = now_date - date_image
    if delta < timedelta(days=182):
        result = True
    else:
        result = False
    return result, date_image.strftime('%d.%m.%Y')


def is_valid_filename(filename):
    fn = filename.split('/')[-1]
    if bool(re.match(r'^[a-z0-9_-]+\.jpg$', fn, flags=re.IGNORECASE)):
        return True, 'Да'
    return False, 'Нет'


def compression_ratio(file_path, image):
    original_size = getsize(file_path)
    img_name = 'compressed.' + image.format
    image.save(img_name, optimize=True, quality=50)
    # windll.kernel32.SetFileAttributesW(img_name, 2)
    compressed_size = getsize(img_name)
    try:
        rm(img_name)
    except FileNotFoundError:
        log(1, 'файла нет')
    _compression_ratio = compressed_size / original_size
    if _compression_ratio < 20.0:
        result = True
    else:
        result = False
    return result, f"{(_compression_ratio * 100):.0f}:1"


# if __name__ == '__main__':
#     paths = ['materials/input_srgb-g.jpg',
#              'materials/input-srgb.jpg',
#              'materials/input_adobe-rgb.jpg',
#              'materials/input_none.jpg',
#              'materials/input.png',
#              'materials/img.JPG']
#
#     for path in paths:
#         # response = []
#         img = get_image_object(path)
#         print()
