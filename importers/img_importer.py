import subprocess
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
import os

def importer(filename, type):
    cmd = ''
    if type == 'png':
        f = open(os.devnull, "w")
        subprocess.call(['tesseract', filename, 'out'], stderr=f)
        f.close()
    elif type == 'jpg':
        f = open(os.devnull, "w")
        subprocess.call(['tesseract', filename, 'out'], stderr=f)
        f.close()
    file = open('out.txt', 'r')
    contents = file.read()
    file.close()
    return contents;

# test run:
# UwU = importer('../test_files/test.png', 'png')
# print(UwU)
