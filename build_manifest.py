import os
import pandas

import validate_file_name

file = r"20151124-075524_FXR8668.jpg"

base_directory = r"N:\User\NAWagner\LPR\Curated"


def get_plate(file):
    return file[file.rfind('_') + 1:file.rfind('.')]


assert get_plate(file) == 'FXR8668'

directory = os.fsencode(base_directory)

image_list = validate_file_name.get_image_list()

license_plates = []

for image in image_list:
    image_name = os.path.basename(image)
    license_plates.append(get_plate(image_name))

writer = pandas.ExcelWriter(os.path.join(base_directory, "manifest.xlsx"))
data_frame = pandas.DataFrame({'LP': license_plates, 'Path': image_list})
data_frame.to_excel(writer, index=False)
writer.save()

print("Done")
