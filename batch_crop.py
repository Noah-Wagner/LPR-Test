from PIL import Image

import os


def crop_image(img):
    right, bottom = img.size
    return img.crop((0, 28, right, bottom))


base_directory = r"N:\User\NAWagner\LPR\Curated"
directory = os.fsencode(base_directory)

for folder_name in os.listdir(directory):
    folder_name = os.fsdecode(folder_name)
    if folder_name.endswith(".db"):
        continue
    folder_path = os.path.join(base_directory, folder_name)
    for image_name in os.listdir(folder_path):
        if image_name.endswith('.jpg'):
            print(image_name)
            image_file_path = os.path.join(folder_path, image_name)
            image = Image.open(image_file_path)
            image = crop_image(image)
            image.save(image_file_path)
