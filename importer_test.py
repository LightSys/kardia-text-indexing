import unittest
import importers.txt_importer as txt
import importers.doc_importer as doc
import importers.PDF_importer as pdf

class TestAdd(unittest.TestCase):

    def test_txt_importer(self):
        file = open('test_files/test.txt')
        file_contents = file.read()
        file.close()
        expected = file_contents
        actual = txt.importer('test_files/test.txt')
        self.assertEqual(actual, expected)

    def test_docx_importer(self):
        expected = "This is an additional test for the .docx file type.\n\nI really want to know if this makes a new line as it should.\n\nThis is a paragraph of sorts. It is going to eventually wrap all the way\naround to the next line, but will it be in the same line in the text\nfile or will there be a new line?\n"
        actual = doc.importer('test_files/test.docx', 'docx')
        self.assertEqual(actual, expected)

    def test_odt_importer(self):
        expected = "This is a test for the doc converter.\n"
        actual = doc.importer('test_files/test.odt', 'odt')
        self.assertEqual(actual, expected)

    def test_pdf_importer(self):
        expected = "Hello my\nfriend, this is\nan example of\na fantastically\ncrafted test\nfile. For this\n\n\x0ctest, I have\ncreated a PDF\nfile that is\nthree pages\nlong, and it\nshould be\n\n\x0cable to read\nall of this.\n\n\x0c"
        actual = pdf.importer('test_files/test.pdf')
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
