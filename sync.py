import data_access
import tokenize
import os
import indexer
import time
import logging

INDEX_FILE='./index_events'

def get_file_modified_date(filename):
    """
    :param filename: filename to be checked
    :param filename: str
    :return: time 
    """
    return os.path.getmtime(filename)


def get_indexing_state():
    """
    Reads the `index_events` file to figure out when or if each document has been indexed.
    :return: result dictionary with the time of indexing or uptated by removing the document entry of a document that was removed
    """
    result = {}

    # Ensure that the file exists
    if not os.path.isfile('index_events'):
        f = open('index_events', 'w')
        f.close()

    # For each line in the file, update the results dictionary. Only the last
    # entry for each document ends up inside the result. If a document is
    # indexed multiple times, it will have multiple lines in the file, but only
    # one in the result dictionary.
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
    """
    Appends an event for a document with the current time.
    :param doc_id: document id
    :type doc_id: int
    :return: None
    """
    print('appending log')
    try:
        f = open(INDEX_FILE, 'a')
        f.write(str(doc_id) + ':' + str(time.time()) + '\n')
    except Exception as e:
        logging.warning('Failed to append to the index_events file')
        logging.warning(str(e))


def append_log_removal(doc_id):
    """
    Append an event for a document, but with a remove event.
    :param doc_id: document id
    :type doc_id: int
    :return: None
    """
    try:
        f = open(INDEX_FILE, 'a')
        f.write(str(doc_id) + ':removed\n')
    except Exception as e:
        logging.warning('Failed to append to the index_events file')
        logging.warning(str(e))


def synchronize(importer_associations, data_accessor):
    """
    Compares the current state of the datbase with the index_events file 
    and the file modification dates of each file. Re-indexes files modified since last index
    :param importer_associations: list of tuples matching filetypes to importer functions
    :param data_accessor: data access object containing methods to retrieve data from the database
    :return: None
    """
    indexed_documents = get_indexing_state()
    documents = data_accessor.get_all_documents()
    for document in documents:
        logging.debug('Processing <doc %d>' % document.id)
        if document.id in indexed_documents:
            if os.path.isfile(document.filename):
                try:
                    file_last_modified = get_file_modified_date(document.filename)
                    file_last_indexed = indexed_documents[document.id]
                    if file_last_modified > file_last_indexed:
                        logging.info('Indexing <doc %d>' % document.id)
                        indexer.smart_index(document, importer_associations, data_accessor)
                        append_log(document.id)
                except Exception as e:
                    logging.error(str(e))
            else:
                logging.warning('<doc %d> points to a nonexistent file.' % document.id)
                logging.warning(document.filename)
        else:
            logging.info('Indexing <doc %d>' % document.id)
            indexer.smart_index(document, importer_associations, data_accessor)
            append_log(document.id)
    # For each document in the index_events file, check if it is still in the
    # database, and remove it if it is not.
    doc_ids = {d.id for d in documents}
    for indexed_doc_id in indexed_documents:
        if indexed_doc_id not in doc_ids:
            print('Removing <doc %d>' % indexed_doc_id)
            try:
                indexer.remove_document(indexed_doc_id, data_accessor)
                append_log_removal(indexed_doc_id)
            except Exception as e:
                logging.error('Attempting to remove <doc %d>' % indexed_doc_id)
                logging.error(str(e))
