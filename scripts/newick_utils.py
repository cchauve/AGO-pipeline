#!/usr/bin/env python3
# coding: utf-8

""" Newick and NHX utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

from collections import defaultdict
import ete3

NEWICK_EXTANT='extant'
NEWICK_ANCESTRAL='ancestral'

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

''' 
Creates from a species tree file a species file of format
<node><TAB><space-separated list of extant descendants>
'''
def newick_create_species_file(species_tree_file, species_file):
    leaves_map = newick_get_leaves(species_tree_file)
    with open(species_file,'w') as out_file:
        for species,leaves in leaves_map.items():
            leaves_str = ' '.join(leaves)
            out_file.write(f'{species}\t{leaves_str}\n')

''' Creates a map from species names to species status '''
def newick_get_species_status(tree_file):
    '''
    input: paths to a Newick tree file with internal nodes named
    output: dic(str->str) node (species) name -> 'extant', 'ancestral'
    '''
    species = {}
    tree = ete3.Tree(tree_file, format=1)
    for node in tree.traverse():
        if node.is_leaf():
            species[node.name] = NEWICK_EXTANT
        else:
            species[node.name] = NEWICK_ANCESTRAL
    return(species)

''' Creates a map from node names to children '''
def newick_get_children_map(tree_file):
    '''
    input: path to a Newick tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
    '''
    tree = ete3.Tree(tree_file, format=1)
    children = {}
    for node in tree.traverse():
        if not node.is_leaf():
            children[node.name] = [ch.name for ch in node.children]
    return(children)

''' 
Returns the list of species in the subtree rooted at 
the LCA of leaves_list
'''
def newick_get_lca_species(tree_file, leaves_list):
    '''
    input: 
    - path to a Newick tree file with internal nodes named
    - list of extant species names
    output:
    list of names of the nodes in the smallest subtree 
    containing all extant leaves from list
    '''
    tree = ete3.Tree(tree_file, format=1)
    leaf1 = tree.get_leaves_by_name(leaves_list[0])[0]
    leaves2 = [tree.get_leaves_by_name(leaf)[0] for leaf in leaves_list[1:]]
    lca = leaf1.get_common_ancestor(*leaves2)
    nodes_list = [lca] + lca.get_descendants()
    return [node.name for node in nodes_list]
