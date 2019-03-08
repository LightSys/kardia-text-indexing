import subprocess
import tempfile
import os

def importer(filename):
    contents = ''
    with tempfile.TemporaryDirectory() as tmpdir:
        # make output file in temp directory to write to
        output_file = open(tmpdir+'/file.txt', "w")
        subprocess.call(['soffice', '--cat', filename], stdout=output_file)
        # close file and reopen it in read mode
        output_file.close()
        output_file = open(tmpdir+'/file.txt', "r")
        contents = output_file.read()
        output_file.close()
    return contents;

# test run:
# UwU = importer('../test_files/Professional_Test_Doc.docx')
# print(UwU)
