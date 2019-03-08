import data_access
import fnmatch
import tokenizer
import os
import importers.txt_importer as txt
import importers.pdf_importer as pdf
import importers.doc_importer as doc

data_accessor = data_access.MySQLDataAccessor()
for word in data_accessor.get_all_words():
    print(word.text)

occ_counts = {}
for occ in data_accessor.get_all_occurrences():
    if occ.document_id not in occ_counts:
        occ_counts[occ.document_id] = 0
    occ_counts[occ.document_id] += 1

print()

print('Occurrence counts')
for doc_id in occ_counts:
    print(doc_id, ':', occ_counts[doc_id])

print()

importer_associations = [
    ('*.txt', txt.importer),
    ('*.docx', doc.importer),
    ('*.odt', doc.importer),
    ('*.pdf', pdf.importer)
]


print('Tokenization counts')
for doc in data_accessor.get_all_documents():
    for (pattern, importer) in importer_associations:
        if fnmatch.fnmatch(doc.filename, pattern) and os.path.isfile(doc.filename):
            text = importer(doc.filename)
            tokens = tokenizer.tokenize(text)
            print(doc.id, ':', sum(map(len, tokens)))
