import tokenizer
import data_access
import requests
import importers.txt_importer as i
import fnmatch

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
    total_index = 0
    for line in lines:
        last_line_index = len(lines) - 1
        for (line_index, word) in enumerate(line):
            is_eol = False
            if index == last_line_index:
                is_eol = True
            data_accessor.put_word(word, 1.0)
            data_accessor.add_occurrence(word, document.id, total_index, is_eol)
        total_index += 1

def remove_from_index(document, data_accessor):
    data_accessor.delete_document_occurrences(document)

def smart_index(document_id, importer_associations, all_words, token, session):
    document = data_access.get_document(document_id)
    for (pattern, importer) in importer_associations:
        if fnmatch.fnmatch(document.filename, pattern):
            index(document.id, all_words, importer, token, session)
