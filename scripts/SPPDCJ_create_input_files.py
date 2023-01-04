#!/usr/bin/env python3
# coding: utf-8

""" Create SPP-DCJ input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import ete3
from DeCoSTAR_statistics import decostar_sign2extremity

''' Creates a map from node names to children '''
def newick_get_children(tree_file):
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

''' Creates SPP-DCJ species tree file '''
def sppdcj_species_trees(in_species_tree, out_species_tree, species_list=None):
    '''
    input:
    - path to a Newick tree file with internal nodes named
    - path to output SPP-DCJ species tree file
    - list of species to consider (None means all)
    output: out_species_tree
    '''
    children_map = newick_get_children(in_species_tree)
    with open(out_species_tree, 'w') as out_tree:
        for species,children in children_map.items():
            if species_list is None or species in species_list:                
                out_tree.write(f'{species}\t{children[0]}\n')
                out_tree.write(f'{species}\t{children[1]}\n')

''' Creates the SPP-DCJ adjacencies file '''
def sppdcj_adjacencies(
        in_adjacencies_file,
        in_weight_threshold,
        out_adjacencies_file,
        species_list=None):
    '''
    input:
    - path to DeCoSTAR adjacencies file
    - minimum weight threshold to keep adjacencies
    - path to output SPP-DCJ adjacencies file
    - list of species to consider (None means all)
    output: out_adjacencies_file
    '''
    sppdcj_sep = '\t'
    decostar_sep = '|'
    with open(in_adjacencies_file, 'r') as in_species_adjacencies, \
         open(out_adjacencies_file, 'w') as out_adjacencies:
        header_str = [
            "#Species","Gene_1","Ext_1","Species","Gene_2","Ext_2","Weight"
        ]
        out_adjacencies.write(f'{sppdcj_sep.join(header_str)}')
        for species_data in in_species_adjacencies.readlines():
            species,species_adjacencies_file = species_data.rstrip().split()
            if species_list is None or species in species_list:
                with open(species_adjacencies_file, 'r') as in_adjacencies:
                    for adj in in_adjacencies.readlines():
                        gene1,gene2,sign1,sign2,_,weight = adj.rstrip().split()
                        signs = decostar_sign2extremity[(sign1,sign2)]
                        fam1,gene1_name = gene1.split(decostar_sep)
                        fam2,gene2_name = gene2.split(decostar_sep)
                        if float(weight) >= in_weight_threshold:
                            adj_str = [
                                species,f'{fam1}_{gene1_name}',signs[0],
                                species,f'{fam2}_{gene2_name}',signs[1],
                                weight
                            ]
                            out_adjacencies.write(f'\n{sppdcj_sep.join(adj_str)}')

                
def main():
    in_adjacencies_file = sys.argv[1]
    in_species_tree = sys.argv[2]
    in_extant_species = sys.argv[3]
    in_weight_threshold = float(sys.argv[4])
    out_species_tree = sys.argv[5]
    out_adjacencies_file = sys.argv[6]

    if in_extant_species == 'all':
        species_list = None
    else:
        species_list = newick_get_lca_species(in_species_tree, in_extant_species.split())
    
    sppdcj_species_trees(in_species_tree, out_species_tree, species_list=species_list)
    sppdcj_adjacencies(in_adjacencies_file, in_weight_threshold, out_adjacencies_file, species_list=species_list)
        
if __name__ == "__main__":
    main()