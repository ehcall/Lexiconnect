import wn
from wn.similarity import path
from wn.similarity import lch
from wn.similarity import wup
import wn.taxonomy


def setupWordnet():
    ### This only needs to be run once to download the dataset
   # wn.download("oewn")
    return

oewn = wn.Wordnet("oewn")
# this is noun depth. there are possibly different depths for different POS
n_depth = wn.taxonomy.taxonomy_depth(oewn, "n")
def calculateSimilarity(word_one, word_two):
    ### There are two different types of similarity that have three different calculations
        ### Taxonomy-based Metrics include: Path, Leacock-Chodorow, and Wu-Palmer
        ### Information Content-Based Metrics include: Resnik, Jiang-Conrath, and Lin
        ### https://wn.readthedocs.io/en/latest/api/wn.similarity.html
    ### We're going to skip the IC ones because there's more stuff to download that I can't figure out.

    # TODO: compensate for different parts of speech, possibly using lemmas

    word_one_synsets = oewn.synsets(word_one)
    word_two_synsets = oewn.synsets(word_two)

    highest_similarity = 0

    for synset_one in word_one_synsets:
        for synset_two in word_two_synsets:
            try:
                ### Taxonomy / Path
                    ### The closer to one, the more similar the synsets are
                test_similarity = path(synset_one,synset_two)

                ### Taxonomy / Leacock-Chodorow
                    ### This is based on taxonomy depth; the higher the score the better
                    ### This one is *much* slower than Path
                #test_similarity = lch(synset_one,synset_two, n_depth)

                ### Taxonomy / Wu-Palmer
                    ### The closer to 1, the more similar the synsets
                #test_similarity = wup(synset_one,synset_two)

                if test_similarity > highest_similarity:
                    highest_similarity = test_similarity
                    #print(test_similarity)
            except wn.Error:
                #print("Not the same parts of speech")
                continue

    return highest_similarity

setupWordnet()
similarity = calculateSimilarity("lift", "elevator")
print(similarity)