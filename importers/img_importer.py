import cv2
import subprocess
import pytesseract
from PIL import Image
import os
import tempfile


def importer(filename, type):
    dir_name = os.path.dirname(__file__)
    cleaner_path = os.path.join(dir_name, "utils/textcleaner")

    with tempfile.TemporaryDirectory() as temp_dir:
        outfile = temp_dir + "/test." + type
        # Pre-process image with ImageMagick's textcleaner script
        # See: http://www.fmwconcepts.com/imagemagick/textcleaner/index.php
        cleaner_params = [cleaner_path, filename, outfile]
        # TODO: These flags are pretty standard, but may want to make it easier to configure
        cleaner_flags = ['-g', '-e stretch', '-f 25', '-o 20', '-t 30', '-u', '-s 1']
        cleaner_params.extend(cleaner_flags)
        subprocess.call(cleaner_params)

        # Process image
        img = cv2.imread(outfile, 0)
        text = pytesseract.image_to_string(Image.fromarray(img))
        contents = text.split()

    return contents;

if __name__ == '__main__':
    # test run:
    UwU = importer('/Users/andrewthomas/kardia-text-indexing/andrewTest/loyal.jpg', 'jpg')
    print(UwU)
