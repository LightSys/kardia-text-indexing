import subprocess
import tempfile

def importer(filename):
    contents = ''
    with tempfile.NamedTemporaryFile() as temp:
        subprocess.call(['pdftotext', filename, temp.name])
        temp.seek(0)
        # file = open(, 'r')
        contents = temp.read().decode("utf-8")
        # file.close()
    return contents;

# test run:
UwU = importer('../test_files/test.pdf')
print(UwU)
