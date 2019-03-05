import subprocess

def importer(filename, type):
    if type == 'docx':
        subprocess.call(['pandoc', filename, '-f', 'docx', '-o', 'out.txt'])
    elif type == 'odt':
        subprocess.call(['pandoc', filename, '-f', 'odt', '-o', 'out.txt'])
    file = open('out.txt', 'r')
    contents = file.read()
    file.close()
    return contents;

# test run:
# UwU = importer('test.docx', 'docx')
# print(UwU)
