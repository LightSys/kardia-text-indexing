from __future__ import print_function
from wand.image import Image
import img_importer as scan
import subprocess
import tempfile

def importer(filename):
    contents = ''
    with tempfile.TemporaryDirectory() as tmpdir:
        page_num = 0
        with Image(filename=filename) as img:
            page_num = len(img.sequence)
            with img.convert('png') as converted:
                converted.save(filename=tmpdir+'/out.png')

        if page_num == 1:
            subprocess.call(['convert', tmpdir+'/out.png', '-filter', 'point', '-resize', '380%', tmpdir+'/out.png'])
        else:
            for x in range(page_num):
                input = tmpdir+'/out-' + str(x) + '.png'
                subprocess.call(['convert', input, '-filter', 'point', '-resize', '380%', input])

        if page_num == 1:
            contents = scan.importer(tmpdir+'/out.png', 'png')
        else:
            for x in range(page_num):
                input = tmpdir+'/out-' + str(x) + '.png'
                contents = contents + scan.importer(input, 'png')
    return contents;

# test run:
# UwU = importer('../test_files/test.pdf')
# print(UwU)
