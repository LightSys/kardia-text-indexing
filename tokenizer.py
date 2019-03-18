# File description:
#
# 0.  Get long string from importer
# 1.  Split long string into multiple strings based on
#     the newline character
# 2. Tokenize the words from the array of strings

from nltk.tokenize import RegexpTokenizer
import string

def tokenize(imported_string):
    punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'  # same as string.punctuation, but allows for apostrophes

    # TODO: convert smart apostrophes ("’") to regular apostrophes ("'")
    imported_string = imported_string.lower()
    string_array = imported_string.split("\n")
    # a word is one or more letters, optionally followed by an apostrophe and more letters
    # or a number with at least 2 digits (note: currently this will split "abc123def" into ["abc", "123", "def"])
    "[a-z]+('[a-z]+)?" # something wrong here
    tokenizer = RegexpTokenizer("[a-z|']+|[0-9]{2,}")  # words are numbers
    words = []
    for idx, elem in enumerate(string_array):
        words.append(tokenizer.tokenize(elem))
    return words;
