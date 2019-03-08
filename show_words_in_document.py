import data_access

data_accessor = data_access.MySQLDataAccessor()
for word in data_accessor.get_all_words():
    print(word.text)

occ_counts = {}
for occ in data_accessor.get_all_occurrences():
    if occ.document_id not in occ_counts:
        occ_counts[occ.document_id] = 0
    occ_counts[occ.document_id] += 1

print()

for doc_id in occ_counts:
    print(doc_id, ':', occ_counts[doc_id])
