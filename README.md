# Kardia Text Indexing Service

This repository contains the code for a python program that indexes files
uploaded into a Kardia application. This is a standalone application in the
sense that it does not provide search functionality, but merely populates
database tables so that the actual search engine obtain results in a performant
manner.

## Architecture

The tool has several parts.

1. *Importers* convert files into a string, which represents the lines
   of the file. Importers for various filetypes exist, including txt, odt,
   docx, pdf, png, and jpeg. Image-based files (which includes image-based
   pdfs) use the Tesseract OCR library, which is currently poorly tuned, so the
   default configuration of this tool does not use the image importers.
2. *Tokenization* converts the string into a list of lists of strings.
   That is, we've broken the file into a list of lines, with each line being a
   list of words. The reason we maintain each line as its own list is that we
   want to be able to detect when a word is at the end of a line.
3. *Indexing* takes the results of the tokenization step and inserts new words
   and word occurrences into the database. Words which already exist do not get
   re-inserted.
4. *Data Access* is swappable in this tool. Two backends exist in the current
   codebase: one using the Centrallix REST API, and one which makes direct SQL
   statements. The SQL backend is far more performant because it is able to
   send many statements all at once, and avoid the overhead that http has with
   the REST API. Other backends can be implemented if the server uses a
   database other than MySQL.
5. *Synchronization* is the stage in which the tool analyzes which documents
   need to be indexed, re-indexed, or removed from the index. A file called
   `index_events` keeps a running log of which files have been indexed and
   when, so that if a file's modification date is after the last time it was
   indexed, then we know that it should be re-indexed. In addition, if the is a
   document which is logged in the `index_events` file but is not in the
   documents table in the database, then we must remove it from the index.
6. *Database polling* allows the tool to be set off running as a long-running
   process. Every fixed amoutn of time the synchronization stage is kicked off
   again.


## Extending and configuring

The only real configuration options that are needed is to specify the type of
data accessor, and to specify the filename patterns that should match with
which importers.

However, you can extend the types of data accessors and importers that are
available.

## Data Accessors

Below is the interface for creating a new data accessor implementation.

```
class MyCustomDataAccessor:

    # Any initializatio of the class. This could include setting up an http
    # session, or connecting to an SQL database for example.
    def __init__(self):
        pass

    def get_all_documents(self):
        pass

    # Makes sure that the database already has the specified word stored. If the
    # word is already stored, this should do nothing.
    def put_word(self, word, relevance):
        pass

    def add_occurrence(self, word_text, document_id, sequence, is_eol):
        pass

    def add_relationship(self, word, target_word, relevance):
        pass

    # This should delete all items from the occurrences table referencing the
    # specified document.
    def delete_document_occurrences(self, document_id):
        pass

    # This function is part of the interface to allow data accessors to support
    # batching of commands. For example, an SQL backend may build up a single
    # query and send all the commands all at once.
    def flush(self):
        pass

    # The rest of these functions are not necessary for the tool to work, but
    # are useful for the included debugging scripts.


    def get_all_words(self):
        pass

    def get_all_occurrences(self):
        pass

    def delete_all_index_data(self):
        pass
```

All of these methods return `Document`, `Word`, `Occurrence`, and
`Relationship` objects, which are described in `data_access.py`.

## Importers


Importers turn a file's contents into a string that can then be tokenized and
indexed.

---

Every importer will take in a filename and then return a string with that
file's contents.

So, calling the text importer may look like this: `importer('myFileName.txt')`

Any new importer added must have an `importer` function. Importers usually
utilize the `subprocess` function of python to convert files to plain text. An
outside program is called using `subprocess.call()` that converts whatever file
type you are given to plain text, which is then stored in a temporary file.

For example, `pdftotext` is used to convert text-based pdf files to plain text.
So, `pdftotext` is called using the filename passed to the importer, then it
outputs to a temp file. Then, python can read in the temp file and turn it into
a string.

---

Temporary files are used for the output reduce clutter of the file system and
to avoid reading in previous versions of a file. In the case of some importers,
due to some inconveniences with the python API, however, regular files are
stored inside of a temporary *directory*. When the function is done, that
directory and all of its contents are removed from the system.

## Unimplemented features

We did not put much effort into the following intended features of this tool.

1. *Tokenizing*. While we made a basic tokenizer, it is still very rough. We
   used NLTK, but did not do too much to make sure that the output tokens were
   really good.
2. *Heuristics to avoid indexing stopwords*. Words like 'the', 'an', and 'a'
   are so common that they really should not be indexed because it would not be
   very helpful. We did not use any techniques to avoid such words.
3. *Tuning Tesseract OCR*. The library works for some images, but for some
   clear images it does not work. We didn't figure out a good way to pull text
   from images. We did however, figure out how to pull images from pdfs, so the
   only issue is with the OCR.
4. *Relevance of words*. The words in the database have a
   relevance field, but we just inserted 1.0 as the value. This relevance value
   should be investigated.
5. *Relationships between words*. We have not yet inserted any relationships
   between words, nor have we considered how to determine the relevance of a
   relationship.
6. *Thorough unit testing*. Sorry guys, you get to have fun with this. We did
   do a tiny bit, but a lot of the parts of this system are difficult to write
   unit tests for (although it still would be good to have them).

## Project infrastructure

Of course, the project is written in python. We used python 3, with virtualenv
and pip to manage dependencies. To get the project setup, make sure python 3 is
installed, along with pip3 and virtualenv for python 3. Navigate to the project
directory, and execute the following command:

```
virtualenv .
```

After that command, you can execute `source bin/activate` to setup the shell to
use the right python version and library dependencies.

Inside the activated environment, execute

```
chmod +x setup.sh
./setup.sh
```

to install all the python dependencies. At any point, if you have installed
extra dependencies, execute `pip freeze` to see the currently installed
packages. To persist these as dependencies, execute `pip freeze >
requirements.txt`.

In addition to the python directories, the following command line programs were
used by importers, so make sure they are installed on your system..

1. libreoffice
2. imagemagick
3. pdftotext
4. [tesseract](https://github.com/tesseract-ocr/tesseract)
