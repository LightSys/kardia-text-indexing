import subprocess

def importer(filename):
    subprocess.call(['pdftotext', filename, 'out.txt'])
    file = open('out.txt', 'r')
    contents = file.read()
    file.close()
    return contents;

# test run:
# UwU = importer('test_text_pdf2.pdf')
# print(UwU)
