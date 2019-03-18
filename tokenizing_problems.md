### Tokenizing problems

- does case matter?
- contractions: should "don't" be "don't" or ["do","n't"]?
- hyphens: "ice-cream" = "ice cream" or "icecream" or something else?
  - what about end-of-line hyphens?
- numbers: do numbers count as tokens?
- are tokens strictly alpha (i.e., letters), or do we sometimes allow other characters within tokens, such as "cat's" or "co-educator"?
- how do we handle abbreviations (e.g., "dr.")?
- email addresses, web addresses, phone numbers, and other complex symbols
- do we want a manual regular expression, or do we want to use tokenizer from NLTK?

Note: string.punctuation is !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
