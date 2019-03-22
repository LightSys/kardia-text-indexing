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

Any new importer added must have an `importer` function. Importers use a variety of methods
to extract text, but the [textract library](https://textract.readthedocs.io/en/latest/index.html) can be used to easy support more file types.

---

Temporary files are used for the output reduce clutter of the file system and
to avoid reading in previous versions of a file. In the case of some importers,
due to some inconveniences with the python API, however, regular files are
stored inside of a temporary *directory*. When the function is done, that
directory and all of its contents are removed from the system.

## Unimplemented features

We did not put much effort into the following intended features of this tool.

1. *Tuning Tesseract OCR*. OCR requires very specific enviornments for preforming
    its operations, usually through image pre-processing. Some pre-processing is in place
    but it could be expanded.
2. *Relevance of words*. The words in the database have a
   relevance field. Stop words have a relevance of 0.2 and other words are set to 1.0.
   Further development is reccomended.
3. *Relationships between words*. The basic structure for relationship finding is in place,
    but integration with relevance is reccomended, especially when duplicate relationships are
    found.
4. *Thorough unit testing*. Some unit testing is in place, but could be more thorough. 
5. *More importers*. A good number of file types are supported, but more cannot hurt.
6. *Image PDF Support*. Image-based PDFs are currently read by the OCR, but typically do not        generate good results, if any results.

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


Install the following system packages:
1. imagemagick
2. [textract dependencies](https://textract.readthedocs.io/en/latest/installation.html)
3. pulseaudio
4. [tesseract](https://github.com/tesseract-ocr/tesseract)
5. GhostScript (We think this is required, but we didn't have a chance to test)

Inside the activated environment, execute

```
chmod +x setup.sh
./setup.sh
```

At any point, if you have installed
extra dependencies, execute `pip freeze` to see the currently installed
packages. To persist these as dependencies, execute `pip freeze >
requirements.txt`.

Update `config.tesseract_path` in config.py.