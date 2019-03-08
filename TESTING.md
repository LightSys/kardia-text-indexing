# Testing is Good

We can't know that our software works unless we test it thoroughly, so let us
make sure this indexing service is well tested. For this particular tool,
testing is rather difficult, however, because of the need for manual database
interactions. To ensure that testing is still properly carried out, we have
compiled a script that can be manually run to test all the parts of the system.

There are three scripts which facilitate manual testing.

1. `reset_indexing_state.py`: Removes all occurrences, words, and relationships
   from the database.
2. `show_words_in_document.py`: Prints the list of each word in the database.
3. `sanity_check.py`: Compares the word count and line count of files (as
   calculated by the importer and tokenizer) with their corresponding entries
in the occurrences database (line count uses the `e_eol` field). Using this
tool, you can verify that the values are the same, which means that the indexer
is likely performing correctly.

## How to test

1. Upload the `small-*` files from the `test_files` folder to the database (you
   can actually upload any files you like - the more testing the merrier).
This will populate the database with files so that the indexer will actually
have work to do.
2. `python reset_indexing_state.py` - resets the database and removes the
   `index_events` file.
3. `python main.py` - runs the indexer. This process does not exit, so you will
   need to have another terminal session to continue the testing procedure.
4. `python show_words_in_document.py` in another terminal. This should output
   all the different words in each of the files you uploaded. Using small test
files makes this verification feasible. This step will be useful when improving
the tokenization part of the system.
5. `python sanity_check.py` - To check that the indexing did what it was
   supposed to do.
6. Now, to make sure that updates work well, delete one of the files you
   uploaded, and rerun the sanity check. Note that the words inside the
database are not removed currently. This may be the wrong behavior, but it is
not too significant since the number of unique words is dwarfed by the number
of occurrences of words. After deletion of the file, the main process should
have logged a message saying that a particular document was removed.
7. Re-upload the deleted file. This should cause the main process to spend some
   time indexing a new document. Run the sanity check again.
8. Now modify one of the files from the Kardia CRM UI. The main process should
   reindex the file. Run the sanity check and make sure that the numbers of
occurrences and lines updated how you edited.

This script should hopefully not take too much time to complete. You can modify
it and cut out some parts when you only want to test certain features.
