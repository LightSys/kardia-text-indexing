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
    # print("word %s synset %s relevance %f" % (word, synset, relevance))
    for lemma in synset.lemmas():
        # print("synset %s lemma %s relevance %f" % (synset.name(), lemma.name(), relevance))
        name = str(lemma.name()).lower()
        if "_" in name:
            continue
        if name in names:
            pass
            # print("skipping duplicate lemma", name)
        else:
            # TODO: figure out why duplicates are being added to database.
            # For now, this line should fix the symptom until we can eventually figure out the cause
            if str(name) == "hope" or str(name) == "co":
                print("name identity from %s to %s" % (name, word))
            if str(word) == "hope" or str(word) == "co":
                print("word identity from %s to %s" % (name, word))
            if str(name).strip() == str(word):
                print("identity relationship from %s to %s" % (name, word))
                continue
            data_accessor.add_relationship(word, name, relevance)
            names.append(name)
        for form in lemma.derivationally_related_forms():
            # print("synset %s lemma %s related form %s" % (synset.name(), lemma.name(), form.name()))
            name = form.name()
            if name in names:
                pass
                # print("skipping duplicate form", name)
            else:
                if str(name) == "hope" or str(name) == "co":
                    print("form name identity from %s to %s" % (name, word))
                if str(word) == "hope" or str(word) == "co":
                    print("form word identity from %s to %s" % (name, word))
                if str(name).strip() == str(word):
                    print("form identity relationship from %s to %s" % (name, word))
                    continue
                data_accessor.add_relationship(word, name, relevance - 0.01)
                names.append(name)

def add_relationships(word, data_accessor, threshold = 0.5):
    if word in data_accessor.get_all_words():
        return  # we already indexed this word, don't get all the relationships again
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
        add_relationships_synset(word, syn, 0.99, data_accessor, names)  # add synonym
        for relationship in relationship_funs:
            for related_syn in relationship(syn):
                if related_syn in added_synsets:
                    print("skipping duplicate syn", related_syn)
                    continue
                relevance = related_syn.path_similarity(syn)
                if relevance < threshold:
                    continue
                added_synsets.add(related_syn)
                add_relationships_synset(word, related_syn, relevance, data_accessor, names)  # add related words
