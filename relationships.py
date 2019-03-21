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
    print("word %s synset %s relevance %f" % (word, synset, relevance))
    names = []  # track the words we've added so that we don't have duplicates
    for lemma in synset.lemmas():
        print("synset %s lemma %s relevance %f" % (synset.name(), lemma.name(), relevance))
        name = lemma.name()
        if name in names:
            pass
            # print("skipping duplicate", name)
        else:
            data_accessor.add_relationship(word, lemma.name(), relevance)
            names.append(name)
        for form in lemma.derivationally_related_forms():
            print("synset %s lemma %s related form %s" % (synset.name(), lemma.name(), form.name()))
            name = form.name()
            if name in names:
                pass
                # print("skipping duplicate", name)
            else:
                data_accessor.add_relationship(word, form.name(), relevance - 0.01)
                names.append(name)
    return names

def add_relationships(word, data_accessor, threshold = 0.5):
    if word in data_accessor.get_all_words():
        return  # we already indexed this word, don't get all the relationships again
    synsets = wordnet.synsets(word)
    added_synsets = set(synsets)
    for syn in synsets:
        add_relationships_synset(word, syn, 0.99, data_accessor)
        for hypernym in syn.closure(lambda s: s.hypernyms()):
            if hypernym in added_synsets:
                print("skipping duplicate hypernym", hypernym)
                continue
            relevance = hypernym.path_similarity(syn)
            if relevance < threshold:
                break
            print("adding hypernym", hypernym)
            added_synsets.add(hypernym)
            add_relationships_synset(word, hypernym, relevance, data_accessor)
        for hyponym in syn.closure(lambda s: s.hyponyms()):
            if hyponym in added_synsets:
                print("skipping duplicate hyponym", hyponym)
                continue
            relevance = hyponym.path_similarity(syn)
            if relevance < threshold:
                break
            print("adding hyponym", hyponym)
            added_synsets.add(hyponym)
            add_relationships_synset(word, hyponym, relevance, data_accessor)
        for part_meronym in syn.part_meronyms():
            if part_meronym in added_synsets:
                print("skipping duplicate part meronym", part_meronym)
                continue
            relevance = part_meronym.path_similarity(syn)
            print("adding part meronym", part_meronym)
            added_synsets.add(part_meronym)
            add_relationships_synset(word, part_meronym, relevance, data_accessor)
        for substance_meronym in syn.substance_meronyms():
            if substance_meronym in added_synsets:
                print("skipping duplicate substance meronym", substance_meronym)
                continue
            relevance = substance_meronym.path_similarity(syn)
            print("adding substance meronym", substance_meronym)
            added_synsets.add(substance_meronym)
            add_relationships_synset(word, substance_meronym, relevance, data_accessor)
        for part_holonym in syn.part_holonyms():
            if part_holonym in added_synsets:
                print("skipping duplicate part_holonym", part_holonym)
                continue
            relevance = part_holonym.path_similarity(syn)
            print("adding part holonym", part_holonym)
            added_synsets.add(part_holonym)
            add_relationships_synset(word, part_holonym, relevance, data_accessor)
        for substance_holonym in syn.substance_holonyms():
            if substance_holonym in added_synsets:
                print("skipping duplicate substance holonym", substance_holonym)
                continue
            relevance = substance_holonym.path_similarity(syn)
            print("adding substance holonym", substance_holonym)
            added_synsets.add(substance_holonym)
            add_relationships_synset(word, substance_holonym, relevance, data_accessor)
        for entailment in syn.entailments():
            if entailment in added_synsets:
                print("skipping duplicate entailment", entailment)
                continue
            relevance = entailment.path_similarity(syn)
            print("adding entailment", entailment)
            added_synsets.add(entailment)
            add_relationships_synset(word, entailment, relevance, data_accessor)

