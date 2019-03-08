import sync
import watcher
import data_access
import time
import importers.txt_importer as txt
import importers.pdf_importer as pdf
import importers.doc_importer as doc
import logging

logging.basicConfig(level=logging.DEBUG)

data_accessor = data_access.MySQLDataAccessor()

def on_file_change():
    logging.info('Synchronizing because filesystem changed')
    try:
        sync.synchronize([
            ('*.txt', txt.importer),
            ('*.docx', doc.importer),
            ('*.odt', doc.importer),
            ('*.pdf', pdf.importer)], data_accessor)
    except Exception as e:
        logging.error('Attempted to synchronize')
        logging.error(str(e))

watcher.watch(on_file_change, '/usr/local/src/cx-git/centrallix-os/apps/kardia/files/')
