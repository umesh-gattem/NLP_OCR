import os

from layout_lm import layout_ocr

input_folder = "actual_files"

output_folder = "ocr_output/"

for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)

    output_file_name = filename[:-4]
    output_path = output_folder + "/" + output_file_name + "/"
    os.makedirs(output_path, exist_ok=True)

    layout_ocr.layout_ocr(file_path, output_path)
