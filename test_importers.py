import unittest
import importers.txt_importer as txt
import importers.doc_importer as doc
import importers.pdf_importer as pdf

class TestImporters(unittest.TestCase):

    def test_txt_importer(self):
        expected = "this is\na multiple line\ntext file\n"
        actual = txt.importer('test_files/small.txt')
        self.assertEqual(actual, expected)

    def test_docx_importer(self):
        expected = "multiple lines in a\n\nword file with formatting.\n"
        actual = doc.importer('test_files/small.docx', 'docx')
        self.assertEqual(actual, expected)

    def test_odt_importer(self):
        expected = "multiple lines in a\n\nlibreoffice file with formatting."
        actual = doc.importer('test_files/small.odt', 'odt')
        self.assertEqual(actual.strip(), expected)

    def test_pdf_importer(self):
        expected = "multiple lines in a\npdf file with formatting.\n"
        actual = pdf.importer('test_files/small.pdf')
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
