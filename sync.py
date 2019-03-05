import requests
import json
import tokenize
import os

BASE_PATH='/usr/local/src/cx-git/centrallix-os'

class Document:
    def __init__(self, doc_object):
        self.id = doc_object['e_document_id']
        self.filename = BASE_PATH + doc_object['e_current_folder'] + '/' + doc_object['e_current_filename']

base_request = "http://10.5.11.230:800/apps/kardia/data/Kardia_DB"

def get_documents():
    response = requests.get(base_request + "/e_document/rows?cx__mode=rest&cx__res_format=attrs&cx__res_type=collection&cx__res_attrs=basic", auth=('devel', 'food.air.bets'))
    if response.status_code == 200:
        document_objects = json.loads(response.content.decode('utf8'))
        for doc_id in document_objects:
            print(doc_id)
            if doc_id != '@id':
                yield Document(document_objects[doc_id])
    else:
        print('Request for documents yielded bad response', response);

def get_file_modified_date(filename):
    return os.path.getmtime(filename)

def synchronize(indexed_documents, importer_associations=None):
    documents = get_documents()
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
