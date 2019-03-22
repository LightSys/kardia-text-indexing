'''
Config options for kardia text indexer
'''
import importers.img_importer as img_imp
import importers.doc_importer as doc
import importers.pdf_importer as pdf
import importers.txt_importer as txt
import data_access

tesseract_path = r'/usr/local/Cellar/tesseract/4.0.0_1/bin/tesseract'

importer_links = [
            ('*.txt', txt.importer),
            ('*.docx', doc.importer),
            ('*.odt', doc.importer),
            ('*.rtf', doc.importer),
            ('*.html', doc.importer),
            ('*.pdf', pdf.importer),
            ('*.jpg', img_imp.importer),
            ('*.jpeg', img_imp.importer)
            ('*.png', img_imp.importer),
            ('*.tiff', img_imp.importer)]

data_accessor = data_access.MySQLDataAccessor()