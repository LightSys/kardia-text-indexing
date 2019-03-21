import tokenizer
import requests
import importers.txt_importer as i
import fnmatch
import logging
from nltk.corpus import stopwords

# This function adds all indexing data for a particular document to the
# database. It uses the data_access, so this code does not directly touch the
# database (i.e. database manipulation is abstracted from this function).
def index(document, importer, data_accessor):
    text = importer(document.filename)
    lines = tokenizer.tokenize(text)

    # Every word in the document ought to be inserted as an occurrence in the
    # document. However, we also have to make sure that we track which words
    # are used at the end of a line. Thus, we must loop over each line, and
    # then over each word in each line. When the `line_index` of the current
    # word matches the last word index of the current line, then that word must
    # be at the end of a line.
    stop_words = set(stopwords.words('english'))

    total_index = 0
    for line in lines:
	# Find the number of words in the current line and subtract 1 to find
	# the index of the last word in the line.
        last_line_index = len(line) - 1
        for (line_index, word) in enumerate(line):
            is_end_of_line = False
	    # If the current word is the last word in the line, then say that
	    # the word is at the end of the line.
            if line_index == last_line_index:
                is_end_of_line = True
            #Checks for stop words and assigns 0.2 to stopwords and 1.0 to other words
            if word in stop_words:
                data_accessor.put_word(word, 0.2)
            else:
                data_accessor.put_word(word, 1.0)
            data_accessor.add_occurrence(word, document, total_index, is_end_of_line)
            total_index += 1
    data_accessor.flush()

def remove_document(document_id, data_accessor):
    data_accessor.delete_document_occurrences(document_id)

# Indexes a document, but checks it's filename pattern to make a decision about
# which importer to use.
def smart_index(document, importer_associations, data_accessor):
    for (pattern, importer) in importer_associations:
        if fnmatch.fnmatch(document.filename, pattern):
            logging.info('selecting "%s" pattern for <doc %d>' % (pattern, document.id))
	    # We might as well remove the document every time we index. When
	    # the document is not already in the database, the remove function
	    # will do nothing.
            remove_document(document.id, data_accessor)
            index(document, importer, data_accessor)
