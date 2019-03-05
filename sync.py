import requests
import json
import tokenize

class Document:
    def __init__(self, doc_object):
        self.id = doc_object['e_document_id']
        self.filename = doc_object['e_current_folder'] + '/' + doc_object['e_current_filename']

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

# def get_file_modified_date(filename):
#     return
# 
# for document in get_documents():
#     print(document)
# 
# for document in synchronize({}):
#     print(document)
# 
# def synchronize(indexed_documents, importer_associations=None):
#     for document in get_documents():
#         if document.id in indexed_documents:
#             file_last_modified = get_file_modified_date(document.filename)
#             file_last_indexed = indexed_documents[document.id]
#             if file_last_modified > file_last_indexed:
#                 yield document
