import os
import pandas

file = r"20151124-075524_FXR8668.jpg"

base_directory = r"N:\User\NAWagner\LPR\Curated"


def get_plate(file):
    return file[file.rfind('_') + 1:file.rfind('.')]


assert get_plate(file) == 'FXR8668'

directory = os.fsencode(base_directory)

file_names = []
license_plates = []

for file in os.listdir(directory):
    file_name = os.fsdecode(file)
    if file_name.endswith(".jpg"):
        file_names.append(file_name)
        license_plates.append(get_plate(file_name))

writer = pandas.ExcelWriter(os.path.join(base_directory, "manifest.xlsx"))
data_frame = pandas.DataFrame({'Filenames': file_names, 'LP': license_plates})
data_frame.to_excel(writer, index=False)
writer.save()

print("Done")
