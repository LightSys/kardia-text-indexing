import data_access

data_accessor = data_access.MySQLDataAccessor()
for word in data_accessor.get_all_words():
    print(word.text)

