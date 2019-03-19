# File description:
#
# 0.  Get long string from importer
# 1.  Split long string into multiple strings based on
#     the newline character
# 2. Tokenize the words from the array of strings

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def tokenize(imported_string):
    imported_string = imported_string.translate(str.maketrans("’", "'"))
    imported_string = imported_string.lower()
    string_array = imported_string.split("\n")
    # a word is one or more letters, optionally followed by an apostrophe and more letters
    # or a number with at least 2 digits (note: currently this will split "abc123def" into ["abc", "123", "def"])
    # TODO: figure out why "[a-z]+('[a-z]+)?|[0-9]{2,}" doesn't work
    tokenizer = RegexpTokenizer("[a-z|']+|[0-9]{2,}")
    stopWords = set(stopwords.words('english'))
    lines = []
    for idx, line in enumerate(string_array):
        real_line = []
        tokenized_line = tokenizer.tokenize(line)
        for word in tokenized_line:
            if word not in stopWords:
                real_line.append(word)
        if len(real_line) > 0:        
            lines.append(real_line)
    return lines
