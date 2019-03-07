import requests
import logging
import http.client as http_client
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger('requests.packages.urllib3')
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

BASE_PATH = '/usr/local/src/cx-git/centrallix-os'
SERVER_PREFIX = 'http://10.5.11.230:800'
BASE_REQUEST = SERVER_PREFIX + '/apps/kardia/data/Kardia_DB'

class Document:
    def __init__(self, doc_object):
        self.id = doc_object['e_document_id']
        self.filename = BASE_PATH + doc_object['e_current_folder'] + '/' + doc_object['e_current_filename']

class Word:
    def __init__(self, word_object):
        self.id = word_object['e_word_id']
        self.text = word_object['e_word']
        self.relevance = word_object['e_word_relevance']

class Occurrence:
    def __init__(self, occur_object):
        self.word_id = occur_object['e_word_id']
        self.document_id = occur_object['e_document_id']
        self.sequence = occur_object['e_sequence']
        self.res_id = occur_object['@id']
        if occur_object['e_eol'] == 0:
            self.is_eol = False
        else:
            self.is_eol = True

class Relationship:
    def __init__(self, rel_object):
        self.word_id = rel_object['e_word_id']
        self.target_word_id = rel_object['e_target_word_id']
        self.relevance = rel_object['e_rel_relevance']

def json_from_response(response):
    return json.loads(response.content.decode('utf8'))

def get_current_date():
    now = datetime.datetime.now()
    return { 'year': now.year, 
             'month': now.month, 
             'day': now.day, 
             'hour': now.hour, 
             'minute': now.minute, 
             'second': now.second } 

def get_auth():
    return (os.getenv('USER'), os.getenv('PASS'))

def get_all_words():
    response = requests.get(
        BASE_REQUEST + '/e_text_search_word/rows',
        params={'cx__mode': 'rest', 
                'cx__res_format': 'attrs', 
                'cx__res_type': 'collection',
                'cx__res_attrs': 'basic'},
        auth=get_auth())
    if response.ok:
        content = json_from_response(response)
        for word_id in content:
            print(word_id)
            if word_id != '@id':
                yield Word(content[word_id])
    else:
        print('Failed to get word', response)

def get_all_documents():
    response = requests.get(
        BASE_REQUEST + '/e_document/rows',
        params={'cx__mode': 'rest', 
                'cx__res_format': 'attrs', 
                'cx__res_type': 'collection',
                'cx__res_attrs': 'basic'},
        auth=get_auth())
    if response.ok:
        document_objects = json.loads(response.content.decode('utf8'))
        for doc_id in document_objects:
            print(doc_id)
            if doc_id != '@id':
                yield Document(document_objects[doc_id])
    else:
        print('Request for documents yielded bad response', response)

class RestApiDataAccessor:
    def __init__(self):
        self.session = requests.session()
        response = self.session.get(
            SERVER_PREFIX, 
            params={'cx__mode': 'appinit', 'cx__appname': 'IXING'},
            auth=get_auth())
        if response.ok:
            content = json.loads(response.content.decode('utf8'))
            self.akey = content['akey']
        else:
            print('Getting the access token failed')
        self.all_words = {word.text: word for word in get_all_words()}
        self.all_occurrences = {}
        for occurrence in geta_all_occurrences():
            if occurrence.document_id not in self.all_occurrences:
                self.all_occurrences[occurrence.document_id] = []
        self.all_occurrences[occurrence.document_id].append(occurrence.res_id)

    def get_all_documents(self):
        pass

    def create_resource(self, resource_name, data):
        current_date = get_current_date()
        user = os.environ.get('USER', 'devel')
        data['s_date_modified'] = current_date
        data['s_date_created'] = current_date
        data['s_created_by'] = user
        data['s_modified_by'] = user
        return self.session.post(
            BASE_REQUEST + '/' + resource_name + '/rows',
            params={'cx__mode': 'rest', 
                    'cx__res_format': 'attrs', 
                    'cx__res_type': 'collection',
                    'cx__res_attrs': 'basic',
                    'cx__akey': self.token},
            json=data,
            auth=get_auth())

    def put_word(self, word, relevance):
        if word not in self.all_words:
            response = self.create_resource('e_text_search_word', 
                    {'e_word': word, 'e_word_relevance': word_relevance})
            if response.ok:
                word = Word(json_from_response(response))
                self.all_words[word.text] = word
            else:
                print('Failed to create new word')

    def add_occurrence(self, word_text, document, sequence, is_eol):
        word_id = self.all_words[word_text].id
        eol = 0
        if is_eol:
            eol = 1
        response = self.create_resource('e_text_search_occur',
                {'e_word_id': word_id, 'e_document_id': document_id, 'e_sequence': sequence, 'e_eol': eol})
        if response.ok:
            occurrence = Occurrence(json_from_response(response))
            self.all_occurrences[occurrence.document_id].append(occurrence)
            return occurrence
        else:
            print('Failed to create new occurrence')

    def add_relationship(self, word, target_word, relevance):
        response = self.create_resource('e_text_search_rel',
            {'e_word_id': word_id, 'e_target_word_id': target_word_id, 'e_rel_relevance': relevance})
        if response.ok:
            return Relationship(json_from_response(response))
        else:
            print('Failed to create new occurrence')

    def delete_document_occurrences(self, document):
        for res_id in self.all_occurrences[document.id]:
            self.session.delete(SERVER_PREFIX + res_id)
        del self.all_occurrences[document.id]

    def flush(self):
        pass

# Makes sure that the database already has the specified word stored. If the
# word is already stored, this should do nothing.
# def put_word(self, word, relevance):

# This should delete all items from the occurrences table referencing the specified document.
# def delete_document_occurrences(self, document):

# def add_relationship(self, word, target_word, relevance):

# def add_occurrence(self, word_text, document, sequence, is_eol):

# This function is part of the interface to allow data accessors to support
# batching of commands. For example, a SQL backend may build up a single query
# and send all the commands all at once.
# def flush(self):
