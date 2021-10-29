import os
from PIL import Image
"""
dir_name = 'raw_data'
new_dir_name = "target_data"
files = os.listdir(dir_name)

for file in files:
    photo = Image.open(os.path.join(dir_name, file))
    photo_resize = photo.resize((768,1024))
    photo_resize.save(os.path.join(new_dir_name, file))
"""


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

dir_name = 'raw_data'
new_dir_name = "target_data"
files = os.listdir(dir_name)
for file in files:
    with Image.open(os.path.join(dir_name, file)) as im:
        im_new = crop_center(im, 768, 1024)
        im_new.save(os.path.join(new_dir_name, file), quality=95)