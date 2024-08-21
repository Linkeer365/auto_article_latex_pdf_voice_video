from pdf2image import convert_from_path
from PIL import Image
import os
from global_used_paths import poppler_path,pdf_out_path_collect_list

def convert_pdf_to_jpg(pdf_out_path, output_folder, poppler_path):
    images = convert_from_path(pdf_out_path, poppler_path=poppler_path)

    for idx, image in enumerate(images,1):
        output_filename = f"{str(idx).zfill(3)}.jpg"
        output_path = os.path.join(output_folder, output_filename)
        image.save(output_path, 'JPEG')

def main():
    for pdf_out_path_idx,pdf_out_path in enumerate(pdf_out_path_collect_list):
        pdf_pic_out_dir = os.path.dirname(pdf_out_path)+os.sep+"pic_mp3"
        convert_pdf_to_jpg(pdf_out_path, pdf_pic_out_dir, poppler_path)

if __name__ == '__main__':
    main()
