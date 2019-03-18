### Tokenizing problems

- contractions: should "don't" be "don't" or ["do","n't"]?
- hyphens: "ice-cream" = "ice cream" or "icecream" or something else?
- numbers: do numbers count as tokens?
- are tokens strictly alpha (i.e., letters), or do we sometimes allow other characters within tokens, such as "cat's" or "co-educator"?
- email addresses?
- web addresses?
- do we want a manual regular expression, or do we want to use tokenizer from NLTK?
