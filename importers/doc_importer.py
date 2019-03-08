import subprocess
import tempfile

def importer(filename, type):
    contents = ''
    with tempfile.NamedTemporaryFile() as temp:
        if type == 'docx':
            subprocess.call(['pandoc', filename, '-f', 'docx', '-o', temp.name])
        elif type == 'odt':
            subprocess.call(['pandoc', filename, '-f', 'odt', '-o', temp.name])
        temp.seek(0)
        contents = temp.read().decode("utf-8")
    return contents;

# test run:
# UwU = importer('../test_files/test.docx', 'docx')
# print(UwU)
