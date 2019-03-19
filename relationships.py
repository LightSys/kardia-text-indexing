"""
Relationships (in order of highest relevance factor to lowest relevance factor)
1. derivationally related forms (lemma.derivationally_related_forms())
2. synonyms
3. hypernym (more general term)
4. hyponym (more specific term)
5. meronym (part)
6. holonym (whole)
7. entailment (implication)
8. corpus.similar (appear in similar contexts)
"""

from nltk.corpus import wordnet

def get_relationships_synset(word, synset, relevance):
    for lemma in synset.lemmas():
        rel_tup = (word, lemma.name(), relevance)  # TODO: add this relationship to database
        for name in lemma.derivationally_related_forms():
            rel_tup = (word, lemma.name(), relevance - 0.01)  # TODO: add this relationship to database

def get_relationships(word):
    synsets = wordnet.synsets(word)
    for syn in synsets:
        get_relationships_synset(word, syn, 0.99)
        for hypernym in syn.closure(lambda s: s.hypernyms()):
            relevance = hypernym.path_similarity(syn)
            get_relationships_synset(word, hypernym, relevance)
        for hyponym in syn.closure(lambda s: s.hyponyms()):
            relevance = hyponym.path_similarity(syn)
            get_relationships_synset(word, hyponym, relevance)
        for meronym in syn.closure(lambda s: s.meronyms()):
            relevance = meronym.path_similarity(syn)
            get_relationships_synset(word, meronym, relevance)
        for holonym in syn.closure(lambda s: s.holonyms()):
            relevance = holonym.path_similarity(syn)
            get_relationships_synset(word, holonym, relevance)
        for entailment in syn.closure(lambda s: s.entailments()):
            relevance = holonym.path_similarity(syn)
            get_relationships_synset(word, entailment, relevance)
