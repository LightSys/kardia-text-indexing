import subprocess
import os
import tempfile

def importer(filename, type):
    contents = ''
    with tempfile.TemporaryDirectory() as tmpdir:
        if type == 'png':
            path = tmpdir + '/out'
            f = open(os.devnull, "w")
            subprocess.call(['tesseract', filename, path], stderr=f)
            f.close()
        elif type == 'jpg':
            path = tmpdir + 'out'
            f = open(os.devnull, "w")
            subprocess.call(['tesseract', filename, path], stderr=f)
            f.close()
        file = open(path+'.txt', 'r')
        contents = file.read()
        file.close()

    return contents;

# test run:
# UwU = importer('../test_files/test.png', 'png')
# print(UwU)
