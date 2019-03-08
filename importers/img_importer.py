import subprocess
import os
import tempfile

def importer(filename, type):
    contents = ''
    with tempfile.TemporaryDirectory() as tmpdir:
        if type == 'png':
            path = tmpdir + '/out'
            redirected_output_file = open(os.devnull, "w")
            subprocess.call(['tesseract', filename, path], stderr=redirected_output_file)
            redirected_output_file.close()
        elif type == 'jpg':
            path = tmpdir + '/out'
            redirected_output_file = open(os.devnull, "w")
            subprocess.call(['tesseract', filename, path], stderr=redirected_output_file)
            redirected_output_file.close()
        output_file = open(path+'.txt', 'r')
        contents = output_file.read()
        output_file.close()

    return contents;

# test run:
# UwU = importer('../test_files/test.png', 'png')
# print(UwU)
