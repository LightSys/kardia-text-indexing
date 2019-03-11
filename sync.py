import data_access
import tokenize
import os
import indexer
import time
import importers.txt_importer as txt
import importers.pdf_importer as pdf
import importers.doc_importer as doc
import requests

INDEX_FILE='./index_events'

def get_file_modified_date(filename):
    return os.path.getmtime(filename)

def get_indexing_state():
    result = {}
    f = open(INDEX_FILE, 'r')
    for line in f:
        if len(line.strip()) != 0:
            doc_id, timestamp = line.split(':')
            result[int(doc_id)] = float(timestamp)
    f.close()
    return result

def append_log(doc_id):
    f = open(INDEX_FILE, 'a')
    f.write(str(doc_id) + ':' + str(time.time()) + '\n')

def synchronize(importer_associations, token, session):
    indexed_documents = get_indexing_state()
    documents = data_access.get_documents()
    all_words = data_access.get_words()
    for document in documents:
        if document.id in indexed_documents:
            print('document found')
            file_last_modified = get_file_modified_date(document.filename)
            file_last_indexed = indexed_documents[document.id]
            print(file_last_modified, file_last_indexed)
            if file_last_modified > file_last_indexed:
                print('re-indexing document:', document.id)
                # indexer.remove_document(document_id)
                indexer.smart_index(document.id, importer_associations, all_words, token, session)
                append_log(document.id)
        else:
            print('indexing document:', document.id)
            indexer.smart_index(document.id, importer_associations, all_words, token, session)
            append_log(document.id)
    doc_ids = {d.id for d in documents}
    print(list(documents))
    for indexed_doc_id in indexed_documents:
        if indexed_doc_id not in doc_ids:
            print('removing document:', indexed_doc_id)
            # indexer.remove_document(document_id)

session = requests.session()
token = data_access.get_access_token(session)
synchronize([('*.txt', txt.importer), ('*.docx', lambda filename: doc.importer(filename, 'docx')),('*.odt', lambda filename: doc.importer(filename, 'odt')), ('*.pdf', pdf.importer)], token, session)
for d in data_access.get_documents():
    print(d)
