import boto3
import os

from manifest import Manifest
import validate_file_name

path_prefix = r"N:\User\NAWagner\LPR\Curated"
responses = []


def open_image(image_path):
    with open(image_path, 'rb') as image:
        image_read = image.read()
    return image_read


def create_client():
    return boto3.client('rekognition')


def run_detect_text(image_path):
    return client.detect_text(
        Image={
            'Bytes': open_image(image_path)
        }
    )


def get_highest_confidence_line(text_list):
    max = 0.0
    for item in text_list:
        if max < item['Confidence'] and item['Type'] == 'LINE':
            max_item = item
            max = item['Confidence']
    return max_item


def license_plate_format(string):
    string = "".join(string.split())
    string = string.upper()
    string = string.replace('O', '0')
    string = string.replace('B', '8')
    string = string.replace('Q', '0')
    string = string.replace('D', '0')
    return string


def check_results(results, correct_lp):
    lines = []
    correct_lp = license_plate_format(correct_lp)
    for line_item in results:
        if line_item['Type'] == 'LINE':
            text = line_item['DetectedText']
            text = license_plate_format(text)
            lines.append(text)
    return correct_lp in lines


def run_test(image, correct_lp):
    image_full_path = os.path.join(path_prefix, image)
    results = run_detect_text(image_full_path)
    results_text_detections = results['TextDetections']
    responses.append(results_text_detections)
    return check_results(results_text_detections, correct_lp)


client = create_client()

manifest = Manifest.load_manifest(os.path.join(path_prefix, "manifest.xlsx"))

i = 1
success = []
success_count = 0
total_count = 0
for row in manifest.data_frame.values:
    test_result = run_test(row[1], row[0])
    if test_result:
        success_count += 1
    total_count += 1
    success.append(test_result)
    i += 1

manifest.write_success(success, responses)

print("Done")
print("Success Rate: " + str(100 * float(success_count) / total_count) + '%')
