import sync
import data_access
import time
import importers.txt_importer as txt
import importers.pdf_importer as pdf
import importers.doc_importer as doc
import logging

logging.basicConfig(format='%(levelname)s\t%(message)s', level=logging.DEBUG)

data_accessor = data_access.MySQLDataAccessor() #contains databse accessing methods

POLLING_DELAY = 10

while True:
    """
    Run a loop checking and updating the database indexing state with sync
    """
    time.sleep(POLLING_DELAY)
    try:
        sync.synchronize([
            ('*.txt', txt.importer),
            ('*.docx', doc.importer),
            ('*.odt', doc.importer),
            ('*.rtf', doc.importer),
            ('*.html', doc.importer),
            ('*.pdf', pdf.importer)], data_accessor)
    except Exception as e:
        logging.error('Attempted to synchronize')
        logging.error(str(e))
