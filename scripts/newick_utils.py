#!/usr/bin/env python3
# coding: utf-8

""" Newick and NHX utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

from collections import defaultdict
import ete3

''' Creates a map from node names to list of descendant extant species '''
def newick_get_leaves(species_tree_file):
    '''
    input: paths to a Newick species tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in 
      species_tree_file, each list is sorted in alphabetical order
    '''
    tree = ete3.Tree(species_tree_file, format=1)
    leaves = defaultdict(list)
    for node in tree.traverse():
        for leaf in node:
            leaves[node.name].append(leaf.name)
        leaves[node.name].sort()
    return(leaves)

