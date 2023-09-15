import os
import tempfile

import pypdfium2 as pdfium
from PIL import Image
from transformers import LayoutLMv3ImageProcessor


def convert_pdf_to_image(pdf_file_path, temp_folder):
    pdf = pdfium.PdfDocument(pdf_file_path)
    n_pages = len(pdf)
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        pil_image = page.render(scale=300 / 72).to_pil()
        pil_image.save(temp_folder + f"/image_{page_number + 1}.jpg")
    return n_pages


def layout_ocr(file_path, output_path):
    with tempfile.TemporaryDirectory() as temp_folder:
        no_of_pages = convert_pdf_to_image(file_path, temp_folder)

        for page_number in range(no_of_pages):
            filename = f"image_{page_number + 1}.jpg"
            image_file = os.path.join(temp_folder, filename)
            image = Image.open(image_file)
            feature_extractor = LayoutLMv3ImageProcessor(apply_ocr=True)

            features = feature_extractor(image)

            print(page_number, f"Words: {features['words'][0]}")
            # print(f"Boxes: {features['boxes'][0]}")
            # print(f"Image pixels: {features['pixel_values'][0].shape}")

            predicted_ocr = ""
            for word in features['words'][0]:
                predicted_ocr += word + " "

            with open(output_path + f"page_{page_number}.txt", "w") as file:
                file.write(predicted_ocr)

            # image = Image.open(image_file)
            #
            # draw = ImageDraw.Draw(image)
            #
            # width_scale = image.width / 1000
            # height_scale = image.height / 1000
            #
            # for boundary_box in features['boxes'][0]:
            #     draw.rectangle([boundary_box[0] * width_scale, boundary_box[1] * height_scale,
            #                     boundary_box[2] * width_scale, boundary_box[3] * height_scale],
            #                    outline='red', width=2)
            # filename = "result.png"
            #
            # plt.imshow(image)
            # plt.savefig("result.jpg")
            # # cv2.imwrite(filename, image)
