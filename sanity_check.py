import data_access
import fnmatch
import tokenizer
import os
import importers.txt_importer as txt
import importers.pdf_importer as pdf
import importers.doc_importer as doc

data_accessor = data_access.MySQLDataAccessor()

occ_counts = {}
line_counts = {}
for occ in data_accessor.get_all_occurrences():
    if occ.document_id not in occ_counts:
        occ_counts[occ.document_id] = 0
    occ_counts[occ.document_id] += 1
    if occ.is_eol == True:
        if occ.document_id not in line_counts:
            line_counts[occ.document_id] = 0
        line_counts[occ.document_id] += 1

print('==== Word count ====')

print('---- Database ----')
for doc_id in occ_counts:
    print(doc_id, ':', occ_counts[doc_id])

importer_associations = [
    ('*.txt', txt.importer),
    ('*.docx', doc.importer),
    ('*.odt', doc.importer),
    ('*.pdf', pdf.importer)
]

print('---- Importer + Tokenizer ----')
for doc in data_accessor.get_all_documents():
    for (pattern, importer) in importer_associations:
        if fnmatch.fnmatch(doc.filename, pattern) and os.path.isfile(doc.filename):
            text = importer(doc.filename)
            tokens = tokenizer.tokenize(text)
            print(doc.id, ':', sum(map(len, tokens)))

print()
print('==== Nonempty Line count ====')

print('---- Database ----')
for doc_id in line_counts:
    print(doc_id, ':', line_counts[doc_id])

print('---- Importer + Tokenizer ----')
for doc in data_accessor.get_all_documents():
    for (pattern, importer) in importer_associations:
        if fnmatch.fnmatch(doc.filename, pattern) and os.path.isfile(doc.filename):
            text = importer(doc.filename)
            tokens = tokenizer.tokenize(text)
            num_lines = len([x for x in tokens if x != []])
            print(doc.id, ':', num_lines)
