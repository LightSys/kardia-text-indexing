# File description:
#
# 0.  Get long string from importer
# 1.  Split long string into multiple strings based on
#     the newline character
# 2. Tokenize the words from the array of strings

from nltk.tokenize import RegexpTokenizer
import string

def tokenize(imported_string):
    # remove punctuation and empty strings
    imported_string = imported_string.translate(str.maketrans('','',string.punctuation))
    string_array = imported_string.split("\n")
    tokenizer = RegexpTokenizer('\w+')
    words = []
    for idx, elem in enumerate(string_array):
        words.append(tokenizer.tokenize(elem))
    return words;
