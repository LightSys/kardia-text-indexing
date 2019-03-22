import data_access

"""
prints the indexed words in the database and their assigned relevances
"""
data_accessor = data_access.MySQLDataAccessor()
for word in data_accessor.get_all_words():
    print(word.text, word.relevance) 

