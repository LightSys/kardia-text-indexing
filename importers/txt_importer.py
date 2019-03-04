def importer(filename):
    file = open(filename, 'r')
    contents = file.read()
    file.close()
    return contents;

# test run:
# test = importer("test_text_importer.txt")
# print(test)
