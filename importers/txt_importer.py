def importer(filename):
    input_file = open(filename, 'r')
    contents = input_file.read()
    input_file.close()
    return contents;

# test run:
# test = importer("test_text_importer.txt")
# print(test)
