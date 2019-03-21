# File description:
#
# 0.  Get long string from importer
# 1.  Split long string into multiple strings based on
#     the newline character
# 2. Tokenize the words from the array of strings

from nltk.tokenize import RegexpTokenizer
import string

def tokenize(imported_string):
    imported_string = imported_string.translate(str.maketrans("’", "'"))
    imported_string = imported_string.lower()
    string_array = imported_string.split("\n")
    # a word is one or more letters, optionally followed by an apostrophe and more letters
    # or a number with at least 2 digits (note: currently this will split "abc123def" into ["abc", "123", "def"])
    '''
    A word is a url, an email, one or more letters optionally followed by an apostrophe and more letters,
        a phone number, or a number with at least two digits.
    The order is such that more specific cases are checked first and general cases are checked later.
    '''
    regexp = "(?:https?|ftp)://[^\s/$.?#].[^\s]*|" \
             "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+|" \
             "[a-z]+(?:'[a-z]+)?|" \
             "\d{3}\D*\d{3}\D*\d{4}(?:\D*\d+)?|" \
             "[0-9]{2,}"
    tokenizer = RegexpTokenizer(regexp)
    # tokenizer = RegexpTokenizer("[a-z|']+|[0-9]{2,}")
    lines = []
    for idx, elem in enumerate(string_array):
        lines.append(tokenizer.tokenize(elem))
    return lines;
