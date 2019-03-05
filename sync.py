import data_access
import tokenize
import os

def get_file_modified_date(filename):
    return os.path.getmtime(filename)

def synchronize(indexed_documents, importer_associations=None):
    documents = data_access.get_documents()
    for document in documents:
        if document.id in indexed_documents:
            print('document found')
            file_last_modified = get_file_modified_date(document.filename)
            file_last_indexed = indexed_documents[document.id]
            print(file_last_modified, file_last_indexed)
            if file_last_modified > file_last_indexed:
                print('re-indexing document:', document.id)
        else:
            print('indexing document:', document.id)
    doc_ids = {d.id for d in documents}
    for indexed_doc_id in indexed_documents:
        if indexed_doc_id not in doc_ids:
            print('removing document:', indexed_doc_id)
