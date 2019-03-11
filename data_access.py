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
    def __init__(self, i, f):
        self.id = i
        self.filename = f

class Word:
    def __init__(self, i, t, r):
        self.id = i
        self.text = t
        self.relevance = r

class Occurrence:
    def __init__(self, w_id, d_id, seq, r_id, is_eol):
        self.word_id = w_id
        self.document_id = d_id
        self.sequence = seq
        self.res_id = r_id
        self.is_eol = is_eol

class Relationship:
    def __init__(self, w_id, t_w_id, r):
        self.word_id = w_id
        self.target_word_id = t_w_id
        self.relevance = r

def document_from_json(doc_object):
    return Document(doc_object['e_document_id'],
            BASE_PATH + doc_object['e_current_folder'] + '/' + doc_object['e_current_filename'])

def word_from_json(word_object):
    return Word(word_object['e_word_id'], word_object['e_word'], word_object['e_word_relevance'])

def occurrence_from_json(occur_object):
    is_eol = False
    if occur_object['e_eol'] == 1:
        is_eol = True
    return Occurrence(occur_object['e_word_id'],
            occur_object['e_document_id'],
            occur_object['e_sequence'],
            occur_object['@id'],
            is_eol)

def relationship_from_json(rel_object):
    return Relationship(rel_object['e_word_id'],
            rel_object['e_target_word_id'],
            rel_object['e_rel_relevance'])

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

def get_all_resource(resource_name, resource_maker):
    response = requests.get(
        BASE_REQUEST + '/' + resource_name + '/rows',
        params={'cx__mode': 'rest', 
                'cx__res_format': 'attrs', 
                'cx__res_type': 'collection',
                'cx__res_attrs': 'basic'},
        auth=get_auth())
    if response.ok:
        objs = json.loads(response.content.decode('utf8'))
        for o_id in objs:
            print(o)
            if o_id != '@id':
                yield resource_maker(objs[o_id])
    else:
        print('Request for all ' + resource_name + ' yielded bad response:', response)

def get_all_words():
    return get_all_resource('e_text_search_word', word_from_json)

def get_all_documents():
    return get_all_resource('e_document', document_from_json)

def get_all_occurrences():
    return get_all_resource('e_text_search_occur', occurrence_from_json)

class MySQLDataAccessor:
    def __init__(self):
        self.database = mysql.connect('connection string')
        self.pending_words = []
        self.pending_occurrences = []
        self.pending_relationships = []

    def get_all_documents(self):
        result = []
        for (doc_id, filename) in self.database.get_rows():
            result.append(Document(doc_id, filename))
        return result

    def put_word(self, word, relevance):
        'insert into e_text_search_word (e_word, e_relevance) select %word, %relevance
         where not exists (select 1 from e_text_search_word where e_word = %word'
        pass

    def add_occurrence(self, word_text, document, sequence, is_eol):
        pass

    def add_relationship(self, word, target_word, relevance):
        pass

    def delete_document_occurrences(self, document):
        pass

    def flush(self):
        pass

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
        for occurrence in get_all_occurrences():
            if occurrence.document_id not in self.all_occurrences:
                self.all_occurrences[occurrence.document_id] = []
        self.all_occurrences[occurrence.document_id].append(occurrence.res_id)

    def get_all_documents(self):
        return list(get_all_documents())

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
                word = word_from_json(json_from_response(response))
                self.all_words[word.text] = word
            else:
                print('Failed to create new word')

    def add_occurrence(self, word_text, document_id, sequence, is_eol):
        word_id = self.all_words[word_text].id
        eol = 0
        if is_eol:
            eol = 1
        response = self.create_resource('e_text_search_occur',
                {'e_word_id': word_id, 'e_document_id': document_id, 'e_sequence': sequence, 'e_eol': eol})
        if response.ok:
            occurrence = occurrence_from_json(json_from_response(response))
            self.all_occurrences[occurrence.document_id].append(occurrence)
            return occurrence
        else:
            print('Failed to create new occurrence')

    def add_relationship(self, word, target_word, relevance):
        response = self.create_resource('e_text_search_rel',
            {'e_word_id': word_id, 'e_target_word_id': target_word_id, 'e_rel_relevance': relevance})
        if response.ok:
            return relationship_from_json(json_from_response(response))
        else:
            print('Failed to create new occurrence')

    def delete_document_occurrences(self, document):
        for res_id in self.all_occurrences[document.id]:
            self.session.delete(SERVER_PREFIX + res_id)
        del self.all_occurrences[document.id]

    def flush(self):
        pass

# Retrieves a list of all the documents in the database currently.
# def get_all_documents(self):

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
