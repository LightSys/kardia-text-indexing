"""
Get word relationships.
Written by Catherine DeJager, for LightSys Code-a-Thon 2019
Relationships (in order of highest relevance factor to lowest relevance factor)
1. derivationally related forms (lemma.derivationally_related_forms())
2. synonyms
3. hypernym (more general term)
4. hyponym (more specific term)
5. meronym (part)
6. holonym (whole)
7. entailment (implication)
"""
from nltk.corpus import wordnet

def add_relationships_synset(word, synset, relevance, data_accessor, names):
    """
    Given a WordNet synset, add relationships to the database from the given word to each target word.
    target words are the lemmas (and their related forms (e.g., walk, walking, walked)) from the synset
    :param word: the base word
    :type word: str
    :param synset: the synset for the target words
    :type synset: wordnet.Synset
    :param relevance: a numerical indication of how similar synset is to word
    :type relevance: float
    :param data_accessor: the interface to the database
    :param names: a list of the words that we have already added relationships for. This list will be modified
    :type names: list of strings
    :return:
    """
    for lemma in synset.lemmas():
        name = lemma.name().lower()
        if "_" in name or "-" in name:  # some lemmas have _ or - in their names, but words in our database never do, so those relationships are useful
            continue
        if name in names:  # we already added a relationship from this word
            pass
        else:
            for relationship in data_accessor.get_all_relationship_tuples_from_word(word):
                if name == relationship[1]:  # we already have a relationship like this in the database
                    break
            else:  # no duplicate relationship found; this is a unique relationship
                data_accessor.add_relationship(word, name, relevance)
                names.append(name)
        for form in lemma.derivationally_related_forms():
            name = form.name().lower()
            if name in names:  # we already added a relationship from this word
                pass
            else:
                for relationship in data_accessor.get_all_relationship_tuples_from_word(word):
                    if name == relationship[1]:  # we already have a relationship like this in the database
                        break
                else:  # no duplicate relationship found; this is a unique relationship
                    data_accessor.add_relationship(word, name, relevance)
                    names.append(name)

def add_relationships(word, data_accessor, threshold = 0.5):
    """
    Given a word, find all words that are related and add the corresponding relationships to the database.
    :param word: the word the relationships are from
    :type word: str
    :param data_accessor: data accessor
    :param threshold: if the relevance of a relationship is lower than this number, don't add the relationship to the database.
    :type threshold: float
    :return:
    """
    synsets = wordnet.synsets(word)  # get the collection of WordNet Synset objects. A Synset is a collection of lemmas with similar meanings.
    added_synsets = set(synsets)
    hypernym_fun = lambda s: s.hypernyms()
    hyponym_fun = lambda s: s.hyponyms()
    part_meronym_fun = lambda s: s.part_meronyms()
    substance_meronym_fun = lambda s: s.substance_meronyms()
    part_holonym_fun = lambda s: s.part_holonyms()
    substance_holonym_fun = lambda s: s.substance_holonyms()
    entailment_fun = lambda s: s.entailments()
    relationship_funs = [hypernym_fun, hyponym_fun, part_meronym_fun, substance_meronym_fun,
                         part_holonym_fun, substance_holonym_fun, entailment_fun]
    # a list of the words that we have already added relationships to. This list will be modified
    names = [word]  # because we don't want to add a relationship from word to word
    for syn in synsets:
        add_relationships_synset(word, syn, 0.8, data_accessor, names)  # add synonym. synonyms have a relevance of 0.8 (chosen because we want a relevance closer to but less than 1)
        for relationship in relationship_funs:
            for related_syn in relationship(syn):
                if related_syn in added_synsets:  # we already analyzed this synonym
                    continue
                relevance = related_syn.path_similarity(syn)
                if relevance < threshold:  # the synonym is too different to be relevant
                    continue
                added_synsets.add(related_syn)
                add_relationships_synset(word, related_syn, relevance, data_accessor, names)  # add related words
