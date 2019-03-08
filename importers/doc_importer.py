import subprocess
import tempfile
import os

def importer(filename):
    contents = ''
    with tempfile.TemporaryDirectory() as tmpdir:
        f = open(tmpdir+'/file.txt', "w")
        subprocess.call(['soffice', '--cat', filename], stdout=f)
        f.close()
        f = open(tmpdir+'/file.txt', "r")
        contents = f.read()
        f.close()
    return contents;

# test run:
# UwU = importer('../test_files/test.odt')
# print(UwU)
