#!/usr/bin/env python3
# coding: utf-8

""" Newick and NHX utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Released"

import sys
from collections import defaultdict
import ete3

''' Check that the tree is rooted '''
def newick_check_rooted(species_tree_file):
    '''
    input: paths to a Newick species tree
    output: boolean
    '''
    tree = ete3.Tree(species_tree_file, format=1)
    root = tree.get_tree_root()
    nb_children = len(root.children)
    return  (nb_children == 2)

''' Check that internal nodes of a tree are named '''
def newick_check_internal_names(species_tree_file):
    '''
    input: paths to a Newick species tree
    output: boolean
    '''
    tree = ete3.Tree(species_tree_file, format=1)
    for node in tree.traverse():
        if len(node.name)==0:
            return False
    return True

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
    return leaves

''' Creates a list of list of leaves names from a file of gene trees '''
def newick_get_gene_trees_leaves(gene_trees_file):
    '''
    input: paths to a file where each line is a Newick gene tree sequence
    output: list of leave names in first tree
    '''
    with open(gene_trees_file, 'r') as in_file:
        gene_tree = in_file.readline()
        tree = ete3.Tree(gene_tree.rstrip(), format=1)
        return [node.name for node in tree.traverse() if node.is_leaf()]

''' List of species names '''
def newick_get_species(species_tree_file, extant=False):
    '''
    input: paths to a Newick species tree file with internal nodes named
    output: list of species names
    '''
    tree = ete3.Tree(species_tree_file, format=1)
    if extant:
        return [node.name for node in tree.traverse() if node.is_leaf()]
    else:
        return [node.name for node in tree.traverse()]

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

'''
Remove internal node names from a species tree
'''
def newick_remove_internal_names(in_species_tree_file, out_species_tree_file):
    tree = ete3.Tree(in_species_tree_file, format=1)
    tree.write(format=5, outfile=out_species_tree_file)

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

''' Creates a map of species names between two identical trees on same leaves '''
def newick_create_species_map(in_tree_file_1, in_tree_file_2):
    '''
    input: two species tree files of same topology and on the same set of leaves
    output: dict(species in tree 1 -> species in tree 2)
    '''
    leaves_map_1 = newick_get_leaves(in_tree_file_1)
    leaves_map_2 = newick_get_leaves(in_tree_file_2)
    species_map = {}
    for species_1,leaves_1 in leaves_map_1.items():
        for species_2,leaves_2 in leaves_map_2.items():
            if leaves_1 == leaves_2:
                species_map[species_1] = species_2
    return species_map
    

def main():
    command = sys.argv[1]

    if command == 'species':
        # Creates a species -> descendants file from a species tree
        in_species_tree_file = sys.argv[2]
        out_species_file = sys.argv[3]
        newick_create_species_file(in_species_tree_file, out_species_file)
    elif command == 'unlabel':
        # Creates a new file with internal nodes unlabeled
        in_species_tree_file = sys.argv[2]
        out_species_tree_file = sys.argv[3]
        newick_remove_internal_names(in_species_tree_file, out_species_tree_file)

if __name__ == "__main__":
    main()
