from __future__ import print_function
from wand.image import Image
import img_importer as scan
import subprocess

def importer(filename):
    contents = ''
    page_num = 0
    with Image(filename=filename) as img:
        page_num = len(img.sequence)
        with img.convert('png') as converted:
            converted.save(filename='out/out.png')

    if page_num == 1:
        subprocess.call(['convert', 'out/out.png', '-filter', 'point', '-resize', '380%', 'out/out.png'])
    else:
        for x in range(page_num):
            input = 'out/out-' + str(x) + '.png'
            subprocess.call(['convert', input, '-filter', 'point', '-resize', '380%', input])

    if page_num == 1:
        contents = scan.importer('out/out.png', 'png')
    else:
        for x in range(page_num):
            input = 'out/out-' + str(x) + '.png'
            contents = contents + scan.importer(input, 'png')
    return contents;

UwU = importer('../test_files/Professional_Test_PDF.pdf')
print(UwU)
