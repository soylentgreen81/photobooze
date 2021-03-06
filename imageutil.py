from PIL import Image
from resizeimage import resizeimage
from flask import current_app
from os.path import join

def create_thumbs(image_name, image_folder, scaled_folder, thumb_folder):
     with open(join(image_folder, image_name), 'r+b') as f:
        with Image.open(f) as image:
            current_app.logger.info('creating scaled image')
            scaled = resizeimage.resize_width(image, 1920)
            scaled.save(join(scaled_folder, image_name), image.format, resample=Image.NEAREST,  optimize=True, progressive=True)
            current_app.logger.info('creating thumb image')
            cover = resizeimage.resize_cover(scaled, [256, 256])
            cover.save(join(thumb_folder, image_name), scaled.format)
