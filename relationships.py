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

def add_relationships_synset(word, synset, relevance, data_accessor):
    for lemma in synset.lemmas():
        data_accessor.add_relationship(word, lemma.name(), relevance)
        for form in lemma.derivationally_related_forms():
            data_accessor.add_relationship(word, form.name(), relevance - 0.01)

def add_relationships(word, data_accessor):
    if word in data_accessor.get_all_words():
        return  # we already indexed this word, don't get all the relationships again
    synsets = wordnet.synsets(word)
    for syn in synsets:
        add_relationships_synset(word, syn, 0.99, data_accessor)
        for hypernym in syn.closure(lambda s: s.hypernyms()):
            relevance = hypernym.path_similarity(syn)
            add_relationships_synset(word, hypernym, relevance, data_accessor)
        for hyponym in syn.closure(lambda s: s.hyponyms()):
            relevance = hyponym.path_similarity(syn)
            add_relationships_synset(word, hyponym, relevance, data_accessor)
        for part_meronym in syn.closure(lambda s: s.part_meronyms()):
            relevance = part_meronym.path_similarity(syn)
            add_relationships_synset(word, part_meronym, relevance, data_accessor)
        for substance_meronym in syn.closure(lambda s: s.substance_meronyms()):
            relevance = substance_meronym.path_similarity(syn)
            add_relationships_synset(word, substance_meronym, relevance, data_accessor)
        for part_holonym in syn.closure(lambda s: s.part_holonyms()):
            relevance = part_holonym.path_similarity(syn)
            add_relationships_synset(word, part_holonym, relevance, data_accessor)
        for substance_holonym in syn.closure(lambda s: s.substance_holonyms()):
            relevance = substance_holonym.path_similarity(syn)
            add_relationships_synset(word, substance_holonym, relevance, data_accessor)
        for entailment in syn.closure(lambda s: s.entailments()):
            relevance = entailment.path_similarity(syn)
            add_relationships_synset(word, entailment, relevance, data_accessor)

