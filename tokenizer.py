# File description:
#
# 0.  Get long string from importer
# 1.  Split long string into multiple strings based on
#     the newline character
# 2. Tokenize the words from the array of strings

from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.corpus import stopwords
import string

def tokenize(imported_string):
    punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'  # same as string.punctuation, but allows for apostrophes

    # convert smart apostrophes "’" to regular apostrophes "'"
    imported_string = imported_string.translate(str.maketrans("’", "'"))
    imported_string = imported_string.lower()
    string_array = imported_string.split("\n")
    # a word is one or more letters, optionally followed by an apostrophe and more letters
    # or a number with at least 2 digits (note: currently this will split "abc123def" into ["abc", "123", "def"])
    # TODO: figure out why "[a-z]+('[a-z]+)?|[0-9]{2,}" doesn't work
    tokenizer = RegexpTokenizer("[a-z|']+|[0-9]{2,}")
    stopWords = set(stopwords.words('english')) #makes a dict of stopwords

    words = []
    wordsFiltered = []
    for idx, elem in enumerate(string_array):
        words.append(tokenizer.tokenize(elem))
    for word in words:
        for w in word: #each word in word is a list
            if w not in stopWords:
                wordsFiltered.append(w)
    return wordsFiltered;
