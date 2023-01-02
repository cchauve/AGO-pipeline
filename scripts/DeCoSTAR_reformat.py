#!/usr/bin/env python3
# coding: utf-8

""" Reformat DeCoSTAR genes and adjacencies """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os
from collections import defaultdict
import ete3
from DeCoSTAR_create_input_files import read_families as decostar_genes_map

''' Creates a map from node names to list of descendant extant species '''
def newick_get_leaves(tree_file):
    '''
    input: paths to a Newick tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    tree = ete3.Tree(tree_file, format=1)
    leaves = defaultdict(list)
    for node in tree.traverse():
        for leaf in node:
            leaves[node.name].append(leaf.name)
        leaves[node.name].sort()
    return(leaves)

''' Reads the map from nodes to descendant leaves from DeCoSTAR output '''
def decostar_get_leaves(in_species_file):
    '''
    input:
    - DeCoSTAR species file
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    leaves = {}
    with open(in_species_file, 'r') as in_species:
        for node in in_species.readlines():
            node_data = node.rstrip().split()
            leaves[node_data[0]] = node_data[1:]
            leaves[node_data[0]].sort()
    return(leaves)

''' Returns a map of correspondance between species names of species tree and DeCoSTAR species '''
def decostar_species_map(in_species_tree_file, in_species_file):
    '''
    input:
    - original species tree file
    - DeCoSTAR species file
    output: dict(str->str) indexd by DeCoSTAR species labels
    '''
    newick_leaves_map = newick_get_leaves(in_species_tree_file)
    decostar_leaves_map = decostar_get_leaves(in_species_file)
    map_aux = defaultdict(list)
    for species,leaves in newick_leaves_map.items():
        map_aux[''.join(leaves)].append(species)
    for species,leaves in decostar_leaves_map.items():
        map_aux[''.join(leaves)].append(species)
    species_map = {}
    for species_pair in map_aux.values():
        species_map[species_pair[1]] = species_pair[0]
    return(species_map)

''' Returns a list of reconciled families '''
def decostar_reconciled_families(in_reconciliations_file):
    '''
    input: reconciliations access file
    output: list of reconciled families
    '''
    families = []
    with open(in_reconciliations_file, 'r') as reconciliations:
        for reconciliation in reconciliations.readlines():
            fam_id = reconciliation.split()[0]
            families.append(fam_id)
    return families

''' Reformat DeCoSTAR genes file '''
def decostar_reformat_genes_file(
        in_species_map,
        in_families_file,
        in_reconciliations_file,
        in_genes_file,
        out_genes_file,
        char_sep='|'
):
    '''
    input:
    - dict(str->str): mapping from DeCoSTAR species names to species names
    - original families file
    - reconciliations access file
    - DeCoSTAR genes file
    - reformated genes file
    - [optional] separator family<char_sep>gene
    output:
    dict(str->str): mapping from DeCoSTAR gene names to reformated gene names
    of format family_name<char_sep>gene_name for ancestral genes
    '''
    genes_map = decostar_genes_map(in_families_file)
    genes_name = {
        gene: f'{fam_id}{char_sep}{gene}'
        for gene,fam_id in genes_map.items()
    }
    families = decostar_reconciled_families(in_reconciliations_file)
    with open(in_genes_file, 'r') as in_genes, \
         open(out_genes_file, 'w') as out_genes:
        for line in in_genes.readlines():
            line_split = line.rstrip().split()
            in_species,in_gene = line_split[0:2]
            out_species = in_species_map[in_species]
            if char_sep in in_gene:
                family,gene_id = in_gene.split(char_sep)
                out_gene = f'{families[int(family)]}{char_sep}{gene_id}'
                genes_name[in_gene] = out_gene
            else:
                out_gene = genes_name[in_gene]
            out_gene_str = ' '.join(
                [out_species, out_gene] +
                [genes_name[gene] for gene in line_split[2:]]
            )
            out_genes.write(f'{out_gene_str}\n')
    return(genes_name)

''' Reformat DeCoSTAR adjacencies file '''
def decostar_reformat_adjacencies_file(
        in_species_map,
        in_genes_name,
        in_adjacencies_file,
        out_adjacencies_file):
    '''
    input:
    - dict(str->str): mapping from DeCoSTAR species names to species names
    - dict(str->str): mapping from DeCoSTAR gene names to reformated gene names
      of format family_name|gene_name for ancestral genes
    - DeCoSTAR adjacencies file
    - reformatted adjacencies file
    '''
    with open(in_adjacencies_file, 'r') as in_adjacencies, \
         open(out_adjacencies_file, 'w') as out_adjacencies:
        for line in in_adjacencies.readlines():
            line_split = line.rstrip().split()
            in_species,in_gene1,in_gene2 = line_split[0],line_split[1],line_split[2]
            out_species = in_species_map[in_species]
            out_gene1,out_gene2 = in_genes_name[in_gene1],in_genes_name[in_gene2]
            out_adjacency_str = ' '.join(
                [out_species, out_gene1, out_gene2] + line_split[3:]
            )
            out_adjacencies.write(f'{out_adjacency_str}\n')


def main():
    in_species_tree_file = sys.argv[1]
    in_species_file = sys.argv[2]
    in_families_file = sys.argv[3]
    in_reconciliations_file = sys.argv[4]
    in_genes_file = sys.argv[5]
    in_adjacencies_file = sys.argv[6]
    out_genes_file = sys.argv[7]
    out_adjacencies_file = sys.argv[8]

    species_map = decostar_species_map(in_species_tree_file, in_species_file)
    genes_map = decostar_reformat_genes_file(
        species_map, in_families_file, in_reconciliations_file, in_genes_file, out_genes_file
    )
    decostar_reformat_adjacencies_file(
        species_map, genes_map, in_adjacencies_file, out_adjacencies_file
    )
    
if __name__ == "__main__":
    main()

