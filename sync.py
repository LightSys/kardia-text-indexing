import data_access
import tokenize
import os
import indexer
import time
import importers.txt_importer as txt
import importers.pdf_importer as pdf
import importers.doc_importer as doc

INDEX_FILE='./index_events'

def get_file_modified_date(filename):
    return os.path.getmtime(filename)

def get_indexing_state():
    result = {}
    f = open(INDEX_FILE, 'r')
    for line in f:
        line = line.strip()
        if len(line) != 0:
            doc_id, timestamp = line.split(':')
            i = int(doc_id)
            if timestamp == 'removed':
                del result[i]
            else:
                result[i] = float(timestamp)
    f.close()
    return result

def append_log(doc_id):
    f = open(INDEX_FILE, 'a')
    f.write(str(doc_id) + ':' + str(time.time()) + '\n')

def append_log_removal(doc_id):
    f = open(INDEX_FILE, 'a')
    f.write(str(doc_id) + ':removed\n')

def synchronize(importer_associations, data_accessor):
    indexed_documents = get_indexing_state()
    documents = data_accessor.get_all_documents()
    for document in documents:
        print('document found', document.id)
        if document.id in indexed_documents:
            file_last_modified = get_file_modified_date(document.filename)
            file_last_indexed = indexed_documents[document.id]
            print(file_last_modified, file_last_indexed)
            if file_last_modified > file_last_indexed:
                print('re-indexing document:', document.id)
                indexer.remove_document(document.id, data_accessor)
                indexer.smart_index(document, importer_associations, data_accessor)
                append_log(document.id)
        else:
            print('indexing document:', document.id)
            indexer.smart_index(document, importer_associations, data_accessor)
            append_log(document.id)
    doc_ids = {d.id for d in documents}
    print(list(doc_ids))
    for indexed_doc_id in indexed_documents:
        if indexed_doc_id not in doc_ids:
            print('removing document:', indexed_doc_id)
            indexer.remove_document(indexed_doc_id, data_accessor)
            append_log_removal(indexed_doc_id)

data_accessor = data_access.MySQLDataAccessor()

for d in data_accessor.get_all_documents():
    print(d)

print('synchronizing')
synchronize([
    ('*.txt', txt.importer),
    ('*.docx', lambda filename: doc.importer(filename, 'docx')),
    ('*.odt', lambda filename: doc.importer(filename, 'odt')),
    ('*.pdf', pdf.importer)], data_accessor)
