"""
Module for accessing Kardia database through MariaDB (MySQLDataAccessor) or JSON (RestApiDataAccessor)
"""
import requests
import logging
import json
import datetime
import os
import MySQLdb
from dotenv import load_dotenv
load_dotenv()

BASE_PATH = '/usr/local/src/cx-git/centrallix-os'
SERVER_PREFIX = 'http://10.5.11.230:800'
BASE_REQUEST = SERVER_PREFIX + '/apps/kardia/data/Kardia_DB'

class Document:
    """
    A document, as represented in the Kardia database. Contains an id and a filename
    """
    def __init__(self, i, f):
        """
        :param i: document id
        :type i: int
        :param f: filename
        :type f: str
        """
        self.id = i
        self.filename = f

class Word:
    """
    A word, as represented in the Kardia database. Contains id, text, and relevance.
    """
    def __init__(self, i, t, r):
        """
        :param i: id
        :type id: int
        :param t: text
        :type t: str
        :param r: relevance
        :type r: float
        """
        self.id = i
        self.text = t
        self.relevance = r

class Occurrence:
    """
    A word occurrence, as represented in the Kardia database. Contains word id, document id, sequence, res id, and is end of line
    """
    def __init__(self, w_id, d_id, seq, r_id, is_eol):
        """
        :param w_id: word id
        :type w_id: int
        :param d_id: document id
        :type d_id: int
        :param seq: TODO: what is this?
        :param r_id: TODO: what is thist?
        :param is_eol: indicates whether the occurrence is at the end of a line
        :type is_eol: bool
        """
        self.word_id = w_id
        self.document_id = d_id
        self.sequence = seq
        self.res_id = r_id
        self.is_eol = is_eol

class Relationship:
    """
    A word relationship, as represented in the Kardia database. Contains word id, target word id, and relevance
    """
    def __init__(self, w_id, t_w_id, r):
        """
        :param w_id: word id
        :type w_id: int
        :param t_w_id: target word id
        :type t_w_id: int
        :param r: relevance - a measure of how similar the two words are
        :type r: float
        """
        self.word_id = w_id
        self.target_word_id = t_w_id
        self.relevance = r

def document_from_json(doc_object):
    """
    :param doc_object: json code that describes a document
    :type doc_object: json object that contains e_document_id, e_current_folder, and e_current_filename
    :return: a Document object that corresponds to doc_object
    :rtype: Document
    """
    return Document(doc_object['e_document_id'],
            BASE_PATH + doc_object['e_current_folder'] + '/' + doc_object['e_current_filename'])

def word_from_json(word_object):
    """
    :param word_object: json code that describes a word
    :type word_object: json object that contains e_word_id, e_word, and e_word_relevance
    :return: a Word object that corresponds to word_object
    :rtype: Word
    """
    return Word(word_object['e_word_id'], word_object['e_word'], word_object['e_word_relevance'])

def occurrence_from_json(occur_object):
    """
    :param occur_object: json code that describes an occurrence
    :type occur_object: json object that contains e_word_id, e_document_id, e_sequence, @id, and e_eol
    :return: an Occurrence object that corresponds to occur_object
    :rtype: Occurrence
    """
    is_eol = False
    if occur_object['e_eol'] == 1:
        is_eol = True
    return Occurrence(occur_object['e_word_id'],
            occur_object['e_document_id'],
            occur_object['e_sequence'],
            occur_object['@id'],
            is_eol)

def relationship_from_json(rel_object):
    """
    :param rel_object: json code that describes a word relationship
    :type rel_object: json object that contains e_word_id, e_target_word_id, and e_rel_relevance
    :return: a Relationship object that corresponds to rel_object
    :rtype: Relationship
    """
    return Relationship(rel_object['e_word_id'],
            rel_object['e_target_word_id'],
            rel_object['e_rel_relevance'])

def json_from_response(response):
    """
    Decode json
    :param response: a json response
    :return: a python object of the response
    """
    return json.loads(response.content.decode('utf8'))

def get_current_date():
    """
    :return: current date in json format with year, month, day, hour, minute, and second
    """
    now = datetime.datetime.now()
    return { 'year': now.year, 
             'month': now.month, 
             'day': now.day, 
             'hour': now.hour, 
             'minute': now.minute, 
             'second': now.second } 

def get_auth():
    """
    :return: username and password for the current user (as indicated by checking the system environment)
    :rtype: tuple
    """
    return (os.getenv('USER'), os.getenv('PASS'))

def get_all_resource(resource_name, resource_maker):
    """
    Get all resources with a given name (i.e., get one column of the database) using Rest API
    :param resource_name: name of the resource (e.g., e_text_search_word)
    :type resource_name: str
    :param resource_maker: the function to convert the json to the appropriate object (e.g., word_from_json makes a Word object)
    :type resource_maker: function
    :return: the given resource. Note: this is a yield, not a return. The function is not terminated and the local variables are preserved. The function can resume after the yield.
    :rtype: a resource. As implemented this could be one of Document, Occurrence, Word, or Relationship
    """
    response = requests.get(
        BASE_REQUEST + '/' + resource_name + '/rows',
        params={'cx__mode': 'rest', 
                'cx__res_format': 'attrs', 
                'cx__res_type': 'collection',
                'cx__res_attrs': 'basic'},
        auth=get_auth())
    if response.ok:
        objs = json_from_response(response)
        for o_id in objs:
            if o_id != '@id':
                yield resource_maker(objs[o_id])
    else:
        logging.error('Request for all %s yielded bad response.' % resource_name)
        logging.error(response.content)

def get_all_words():
    """
    Query the database using json to find all the words
    :return: all the words in the database. Note: get_all_resource does yield not return
    :rtype: Word
    """
    return get_all_resource('e_text_search_word', word_from_json)

def get_all_documents():
    """
    Query the database using json to find all the documents
    :return: all the documents in the database. Note: get_all_resource does yield not return
    :rtype: Document
    """
    return get_all_resource('e_document', document_from_json)

def get_all_occurrences():
    """
    Query the database using json to find all the word occurrences
    :return: all the word occurrences in the database. Note: get_all_resource does yield not return
    :rtype: Occurrence
    """
    return get_all_resource('e_text_search_occur', occurrence_from_json)

def get_all_relationships():
    return get_all_resource('e_text_search_rel', relationship_from_json)

class MySQLDataAccessor:
    """
    Interface for Kardia database using MySQL
    """
    def __init__(self):
        (username, password) = get_auth()
        self.username = username
        self.database = MySQLdb.connect(user=username, passwd=password, db='Kardia_DB')
        self.database.autocommit(True)
        self.pending_words = []
        self.pending_occurrences = []
        self.pending_relationships = []

    def get_all_documents(self):
        """
        Query the database using MySQL to find all the documents
        :return: a list of all the documents in the database
        :rtype: list of Document
        """
        cursor = self.database.cursor()
        cursor.execute('select e_document_id, e_current_folder, e_current_filename from e_document')
        result = []
        for (doc_id, curr_folder, curr_filename) in cursor.fetchall():
            filename = BASE_PATH + curr_folder + '/' + curr_filename
            result.append(Document(doc_id, filename))
        return result

    def get_all_words(self):
        """
        Query the database using MySQL to find all the words
        :return: a list of all the words in the database
        :rtype: list of str
        """
        cursor = self.database.cursor()
        cursor.execute('select e_word_id, e_word, e_word_relevance from e_text_search_word')
        result = []
        for (word_id, word_text, word_relevance) in cursor.fetchall():
            result.append(Word(word_id, word_text, word_relevance))
        return result

    def get_all_occurrences(self):
        """
        Query the database using MySQL to find all the word occurrences
        :return: a list of all the word occurrences in the database
        :rtype: list of Occurrence
        """
        cursor = self.database.cursor()
        cursor.execute('select e_word_id, e_document_id, e_sequence, e_eol from e_text_search_occur')
        result = []
        for (w_id, d_id, seq, eol) in cursor.fetchall():
            is_eol = False
            if eol == b'\x01':
                is_eol = True
            result.append(Occurrence(w_id, d_id, seq, None, is_eol))
        return result

    def get_all_relationships(self):
        cursor = self.database.cursor()
        cursor.execute('select e_word_id, e_target_word_id, e_rel_relevance from e_text_search_rel')
        result = []
        for (w_id, t_w_id, rel) in cursor.fetchall():
            result.append(Relationship(w_id, t_w_id, rel))
        return result

    def get_all_relationship_tuples(self):
        """
        :return: a list of tuples for each relationship in the database
        :rtype: list of tuples of word_id, target_word_id, and relationship relevance
        """
        cursor = self.database.cursor()
        cursor.execute('select e_word_id, e_target_word_id, e_rel_relevance from e_text_search_rel')
        result = []
        for (w_id, t_w_id, rel) in cursor.fetchall():
            result.append((w_id, t_w_id, rel))
        return result

    def get_all_relationship_tuples_from_word_id(self, word_id):
        """
        :param word_id: id of the word the relationship is from
        :type word_id: int
        :return: a list of tuples for each relationship from the word specified by word id
        :rtype: list of tuples of word_id, target_word_id, and relationship relevance
        """
        cursor = self.database.cursor()
        cursor.execute('select e_word_id, e_target_word_id, e_rel_relevance from e_text_search_rel '
                       'where e_word_id = %d' % word_id)
        result = []
        for (w_id, t_w_id, rel) in cursor.fetchall():
            result.append((w_id, t_w_id, rel))
        return result

    def get_all_relationship_tuples_from_word(self, word):
        """
        :param word: the word the relationship is from
        :return: a list of tuples for each relationship from word
        :rtype: list of tuples of word_id, target_word_id, and relationship relevance
        """
        cursor = self.database.cursor()
        cursor.execute("select e_word_id from e_text_search_word where e_word = '%s'" % word)
        word_id = cursor.fetchone()
        if word_id is None:  # if this word is not in the database
            return []  # return an empty list
        return self.get_all_relationship_tuples_from_word_id(word_id)

    def put_word(self, word, relevance):
        """
        Add a word into the database. (Note: this adds the word to pending_words. You must call flush to actually add the word.)
        :param word: the word to add
        :type word: str
        :param relevance: a measure of how useful the word is in a search (e.g., "email" is more relevant than "and").
        :type relevance: float
        :return: None
        """
        self.pending_words.append((word, relevance))

    def add_occurrence(self, word_text, document, sequence, is_eol):
        """
        Add an occurrence into the database. (Note: this adds the occurrence to pending_occurrences. You must call flush to actually add the occurrence.)
        :param word_text: text of the word
        :type word_text: str
        :param document: the document the word occurs in
        :type document: TODO: what is this
        :param sequence: TODO: what is this
        :param is_eol: indicates whether the occurrence is at the end of the line
        :type is_eol: bool
        :return: None
        """
        self.pending_occurrences.append((word_text, document.id, sequence, is_eol))

    def add_relationship(self, word, target_word, relevance):
        """
        Add a relationship
        :param word: word
        :param target_word: a word that 'word' is related to
        :param relevance: the relevance of the relationship
        :return: None
        """
        self.pending_relationships.append((word, target_word, relevance))

    # Use document_id because we may not have the document
    def delete_document_occurrences(self, document_id):
        """
        Remove document from the database
        :param document_id: ID of the document to be removed
        :return: None
        """
        self.database.cursor().execute('delete from e_text_search_occur where e_document_id = %s', (document_id,))
        self.database.commit()

    def delete_all_index_data(self):
        """
        Deletes all index data from the database
        :return: None
        """
        self.database.cursor().execute('delete from e_text_search_occur')
        self.database.cursor().execute('delete from e_text_search_rel')
        self.database.cursor().execute('delete from e_text_search_word')
        self.database.commit()

    def flush(self):
        """
        Pushes all database changes from other functions to database
        :return: None
        """
        (username, _) = get_auth()
        cursor = self.database.cursor()
        cursor.execute('select max(e_word_id) from e_text_search_word')
        (max_word_id,) = cursor.fetchone()
        if not max_word_id: max_word_id = 0
        logging.info('Max word_id %d' % max_word_id)
        self.database.cursor().executemany(
            '''insert into e_text_search_word
                 (e_word_id, e_word, e_word_relevance, s_date_created, s_created_by, s_date_modified, s_modified_by) 
               select %s, %s, %s, now(), %s, now(), %s
               from e_document
               where not exists (select * from e_text_search_word where e_word = %s)
               limit 1''',
            [(max_word_id + 1 + i, word_text, relevance, username, username, word_text) for (i, (word_text, relevance)) in  enumerate(self.pending_words)])
        self.database.commit()
        self.pending_words = []

        self.database.cursor().executemany(
            '''insert into e_text_search_occur (e_word_id, e_document_id, e_sequence, e_eol)
               select e_word_id, %s, %s, %s
               from e_text_search_word
               where e_word = %s''',
            [(doc_id, sequence, eol, word_text) for (word_text, doc_id, sequence, eol) in self.pending_occurrences])
        self.database.commit()
        self.pending_occurrences = []

        self.database.cursor().executemany(
               "insert ignore into e_text_search_rel "  # ignore so that we get warnings instead of errors for duplicate entries
                   "(e_word_id, e_target_word_id, e_rel_relevance, "
                    "s_date_created, s_created_by, s_date_modified, s_modified_by) "
               "select w.e_word_id, tw.e_word_id, %s, now(), %s, now(), %s "
               "from (select e_word_id from e_text_search_word where e_word = %s) as w,"
                " (select e_word_id from e_text_search_word where e_word = %s) as tw",
            [(t[2], username, username, t[0], t[1]) for t in self.pending_relationships])
        self.database.commit()
        self.pending_relationships = []

class RestApiDataAccessor:
    def __init__(self):
        self.session = requests.session()
        response = self.session.get(
            SERVER_PREFIX, 
            params={'cx__mode': 'appinit', 'cx__appname': 'IXING'},
            auth=get_auth())
        if response.ok:
            content = json.loads(response.content.decode('utf8'))
            self.token = content['akey']
        else:
            logging.error('Getting the access token failed')
            logging.error(response.content)
        self.all_words = {word.text: word for word in get_all_words()}
        self.all_occurrences = {}
        for occurrence in get_all_occurrences():
            if occurrence.document_id not in self.all_occurrences:
                self.all_occurrences[occurrence.document_id] = []
        self.all_occurrences[occurrence.document_id].append(occurrence.res_id)

    def get_all_documents(self):
        """
        :return: all documents in the database
        """
        return list(get_all_documents())

    def create_resource(self, resource_name, data):
        """
        Create a database record in given table
        :param resource_name: database table name
        :type resource_name: str
        :param data: column and value names of the table
        :type data: dict
        :return: the server reply from POST, either success or fail message
        """
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
        """
        Add a word into the database. (Note: this adds to pending words. You must call flush to actually add the word.)
        :param word: the word to add
        :type word: str
        :param relevance: a measure of how useful the word is in a search (e.g. "email" is more relevant than "and").
        :type relevance: float
        :return: None
        """        
        if word not in self.all_words:
            response = self.create_resource('e_text_search_word', 
                    {'e_word': word, 'e_word_relevance': relevance})
            if response.ok:
                word = word_from_json(json_from_response(response))
                self.all_words[word.text] = word
                logging.info('Put word %s' % word.text)
            else:
                logging.error('Failed to create new word')
                logging.error(response.content)

    def add_occurrence(self, word_text, document_id, sequence, is_eol):
        """
        Add an occurrence into the database. (Note: this adds the occurrence to pending_occurrences. You must call flush to actually add the occurrence.)
        :param word_text: text of the word
        :type word_text: str
        :param document_id: the document_id of the document the word occurs in
        :type document_id: int
        :param sequence: TODO: what is this
        :param is_eol: indicates whether the occurrence is at the end of the line
        :type is_eol: bool
        :return: an occurrence object of the word
        :rtype: Occurrence
        """

        word_id = self.all_words[word_text].id
        eol = 0
        if is_eol:
            eol = 1
        response = self.create_resource('e_text_search_occur',
                {'e_word_id': word_id, 'e_document_id': document_id, 'e_sequence': sequence, 'e_eol': eol})
        if response.ok:
            occurrence = occurrence_from_json(json_from_response(response))
            self.all_occurrences[occurrence.document_id].append(occurrence)
            logging.info('Added_occurrence %s' % word_text)
            return occurrence
        else:
            logging.error('Failed to create new occurrence')
            logging.error(response.content)

    def add_relationship(self, word, target_word, relevance):
        """
        Add a relationship
        :param word: word
        :type word: str
        :param target_word: the other word related to word
        :type target_word: str
        :param relevance: the relevance of the relationship between the words. A higher number indicates a stronger relationship
        :type relevance: float
        :return: a relationship object of the relationship between word and target_word
        :rtype: Relationship
        """
        response = self.create_resource('e_text_search_rel',
            {'e_word_id': word_id, 'e_target_word_id': target_word_id, 'e_rel_relevance': relevance})
        if response.ok:
            return relationship_from_json(json_from_response(response))
        else:
            logging.error('Failed to create new relationship')
            logging.error(response.content)

    def delete_document_occurrences(self, document_id):
        """Delete occurrences of the document from the database
        :param document_id: id of the document since the document may have been removed
        :return: None
        """
        for res_id in self.all_occurrences[document_id]:
            self.session.delete(SERVER_PREFIX + res_id)
        del self.all_occurrences[document_id]

    def flush(self):
        pass
