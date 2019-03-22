import subprocess
import tempfile
import textract
from bs4 import UnicodeDammit
import sys
from wand.image import Image
import img_importer
import os

def textBasedImport(file_path):
    text = UnicodeDammit(textract.process(file_path)).unicode_markup
    return text

def imageBasedImport(file_path):
    contents = ''
    with tempfile.TemporaryDirectory() as tmpdir:
        page_num = 0
        with Image(filename=file_path, resolution=400) as img:
            page_num = len(img.sequence)
            with img.convert('png') as converted:
                converted.save(filename=tmpdir+'/out.png')

        if page_num == 1:
            contents = img_importer.importer(tmpdir+'/out.png', 'png')
        else:
            for x in range(page_num):
                input = tmpdir+'/out-' + str(x) + '.png'
                contents = contents + img_importer.importer(input, 'png')

    return contents

def importer(file_path):
    text = textBasedImport(file_path)
    if not text.strip():
        text = imageBasedImport(file_path)
    return text

if __name__ == '__main__':
    UwU = importer(sys.argv[1])
    print(UwU)
