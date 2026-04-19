import wn
from wn.similarity import path
from wn.similarity import lch
from wn.similarity import wup
import wn.taxonomy

import networkx as nx
from pyvis.network import Network

def setupWordnet():
    ### This only needs to be run once to download the dataset
    # wn.download("oewn")
    return

def setupGraph():
    G = nx.Graph()

    # TODO: use a different system beyond hard coding the starting nodes in
    G.add_node("elephant", color="red")
    G.add_node("leaf", color="blue")
    return G

oewn = wn.Wordnet("oewn")
# this is noun depth. there are possibly different depths for different POS
# n_depth = wn.taxonomy.taxonomy_depth(oewn, "n")
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
                #test_similarity = path(synset_one,synset_two)

                ### Taxonomy / Leacock-Chodorow
                    ### This is based on taxonomy depth; the higher the score the better
                    ### This one is *much* slower than Path
                #test_similarity = lch(synset_one,synset_two, n_depth)

                ### Taxonomy / Wu-Palmer
                    ### The closer to 1, the more similar the synsets
                test_similarity = wup(synset_one,synset_two)

                if test_similarity > highest_similarity:
                    highest_similarity = test_similarity
                    #print(test_similarity)
            except wn.Error:
                #print("Not the same parts of speech")
                continue

    return highest_similarity

def addWord(gameGraph, new_word):
    gameGraph.add_node(new_word, color="gray")
    current_nodes = gameGraph.nodes
    for node in current_nodes:
        if node != new_word:
            similarity_number = calculateSimilarity(new_word, node)
            #print(similarity_number)
            if similarity_number >= .5:
                edge_color = "blue"
                # TODO: better way of updating colors, including to nodes that previously weren't connected
                gameGraph.nodes[new_word]['color'] = "blue"
                gameGraph.add_edge(new_word, node, weight=similarity_number, color=edge_color)


    return gameGraph

setupWordnet()
gameGraph = setupGraph()
net = Network(height = "500px", width = "600px", notebook = True)


# TODO: do I have to keep passing my graph? idk someone else figure that out
# TODO: figure out how to end the game (besides number of words)
while len(gameGraph.nodes) < 10:
    new_word = input("New connection word: ")
    gameGraph = addWord(gameGraph, new_word)
    net.from_nx(gameGraph)
    #net.toggle_physics(True)
    net.show('testing.html')