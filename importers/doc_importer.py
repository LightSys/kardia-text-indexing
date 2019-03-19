'''
author: Andrew Thomas
Code-a-thon 2019
'''
import textract
import tempfile
from bs4 import UnicodeDammit

def importer(file_path):
    text = UnicodeDammit(textract.process(file_path)).unicode_markup
    lines = text.split('\n')
    contents = []
    for line in lines:
        if line != '':
            contents.append(line.split())
    return contents;

if __name__ == '__main__':
    UwU = importer('test_files/Professional_Test_Doc.odt')
    print(UwU[0])