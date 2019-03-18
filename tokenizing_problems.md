### Tokenizing problems

- does case matter?
  - A: no. Exception is acronym (e.g., SOAP is different from soap). Could use word relationship table.
- contractions: should "don't" be "don't" or ["do","n't"]?
  - can be one word
- hyphens: "ice-cream" = ["ice", "cream"] or "icecream" or something else?
  - split into separate words
  - what about end-of-line hyphens?
    - recombine end-of-line hyphens before indexing
- numbers: do numbers count as tokens?
  - in some cases, yes. Someone may want to search for a phone number, for example. Don't need to index single digits. 
  Index longer numbers. Don't index numbers in a list. Standalone longer numbers (at least 2 digits) might be useful to index.
  It would be good to find years.
- are tokens strictly alpha (i.e., letters), or do we sometimes allow other characters within tokens, such as "cat's" or "co-educator"?
  - not strictly alpha
  - NOTE: normalize apostrophe and quote styles (standard ascii, not smart quotes)
- how do we handle abbreviations (e.g., "dr.")?
  - remove the period
- email addresses, web addresses, phone numbers, and other complex symbols
  - try to index those things
  - just lump them in like other words
- do we want a manual regular expression, or do we want to use tokenizer from NLTK?

Note: string.punctuation is !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
