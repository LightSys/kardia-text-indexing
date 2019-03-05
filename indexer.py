import tokenizer
import data_access
import requests
import importers.txt_importer as i

def index(document_id, all_words, importer, token, session):
    document = data_access.get_document(document_id)
    text = importer(document.filename)
    lines = tokenizer.tokenize(text)
    total_index = 0
    for line in lines:
        last_line_index = len(lines) - 1
        for (line_index, word) in enumerate(line):
            is_eol = False
            if index == last_line_index:
                is_eol = True
            if word not in all_words:
                word = data_access.insert_word(word, 1.0, token, session)
                all_words[word] = word
            current_word = all_words[word]
            data_access.insert_occurrence(current_word.id, document_id, total_index, is_eol, token, session)
        total_index += 1
