### Relationships
Relationships (in order of highest relevance factor to lowest relevance factor)
1. derivationally related forms (lemma.derivationally_related_forms())
2. synonyms
3. hypernym (more general term)
4. hyponym (more specific term)
5. meronym (part)
6. holonym (whole)
7. entailment (implication)
8. corpus.similar (appear in similar contexts)

### Similarity
- Thesaurus based:
    - Path similarity
    - Leacock-Chodorow Similarity (Leacock and Chodorow 1998)
    - Wu-Palmer Similarity (Wu and Palmer 1994)
- Thesaurus + corpus based:
    - Resnik Similarity (Resnik 1995)
    - Lin Similarity (Lin 1998b)
    - Jiang-Conrath distance (Jiang and Conrath 1997)

According to https://linguistics.stackexchange.com/questions/9084/what-do-wordnetsimilarity-scores-mean,
Jiang-Conrath distance is the best. But if we don't want to use a corpus, Wu-Palmer Similarity looks like the next best option.
