import requests
import logging
import http.client as http_client
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger('requests.packages.urllib3')
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

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
        if occur_object['e_eol'] == 0:
            self.is_eol = False
        else:
            self.is_eol = True

class Relationship:
    def __init__(self, rel_object):
        self.word_id = rel_object['e_word_id']
        self.target_word_id = rel_object['e_target_word_id']
        self.relevance = rel_object['e_rel_relevance']

class Session:
    def __init__(self, token_object):
        self.akey = token_object['akey']
        self.watchdog = token_object['watchdogtimer']

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

def create_resource(resource_name, data, token, session):
    current_date = get_current_date()
    user = os.environ.get('USER', 'devel')
    data['s_date_modified'] = current_date
    data['s_date_created'] = current_date
    data['s_created_by'] = user
    data['s_modified_by'] = user
    return session.post(
        BASE_REQUEST + '/' + resource_name + '/rows',
        params={'cx__mode': 'rest', 
                'cx__res_format': 'attrs', 
                'cx__res_type': 'collection',
                'cx__res_attrs': 'basic',
                'cx__akey': token},
        json=data,
        auth=get_auth())
    

def insert_word(word, word_relevance, token, session):
    response = create_resource('e_text_search_word', {'e_word': word, 'e_word_relevance': word_relevance}, token, session)
    if response.ok:
        return Word(json_from_response(response))
    else:
        print('Failed to create new word')

def insert_occurrence(word_id, document_id, sequence, is_eol, token, session):
    eol = 0
    if is_eol:
        eol = 1
    response = create_resource('e_text_search_occur', 
        {'e_word_id': word_id, 'e_document_id': document_id, 'e_sequence': sequence, 'e_eol': eol}, token, session)
    if response.ok:
        return Occurrence(json_from_response(response))
    else:
        print('Failed to create new occurrence')

def relate_words(word_id, target_word_id, relevance, token, session):
    response = create_resource('e_text_search_rel', 
        {'e_word_id': word_id, 'e_target_word_id': target_word_id, 'e_rel_relevance': relevance}, token, session)
    if response.ok:
        return Relationship(json_from_response(response))
    else:
        print('Failed to create new occurrence')

def get_auth():
    return (os.getenv('USER'), os.getenv('PASS'))

def get_access_token(session):
    auth = get_auth()
    response = session.get(
        SERVER_PREFIX, 
        params={'cx__mode': 'appinit', 'cx__appname': 'IXING'},
        auth=auth)
    if response.ok:
       content = json.loads(response.content.decode('utf8'))
       return content['akey']
    else:
        print('Getting the access token failed')


def get_words():
    result = {}
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
                word = Word(content[word_id])
                result[word.text] = word
        return result
    else:
        print('failed to get word', response)

def get_documents():
    result = []
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
                result.append(Document(document_objects[doc_id]))
    else:
        print('Request for documents yielded bad response', response)
        print(response.content)
    return result

def get_document(document_id):
    response = requests.get(
        BASE_REQUEST + '/e_document/rows/' + str(document_id),
        params={'cx__mode': 'rest', 
                'cx__res_format': 'attrs', 
                'cx__res_attrs': 'basic'},
        auth=get_auth())
    if response.ok:
        return Document(json_from_response(response))
    else:
        print('Request for document yielded bad response', response)
        print(response.content)
