#!/usr/bin/env python3
# coding: utf-8

""" Create DeCoSTAR input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

import sys
from data_utils import (
    data_gene2family,
    data_species2gene_order_path,
    data_family2reconciliation_path,
    data_read_gene_order_file
)

''' Read a gene order file and returns an order list of adjacencies strings '''
def decostar_gene_order2adjacencies_str(
        in_gene_order_file, in_gene2family_map, in_reconciled_families
):
    '''
    input: 
    - path to gene order file
    - map of gene to family ID
    - list of reconciled families to consider 
    (genes from other families are not accounted for)
    output: list(str)
    '''
    orientation = {'1': '+', '0': '-'}
    adjacencies = []
    gene_order = data_read_gene_order_file(in_gene_order_file)
    prev_gene = None
    for (gene_name,gene_chr,_,_,gene_sign) in gene_order:
        if in_gene2family_map[gene_name] in in_reconciled_families:
            gene_orientation = orientation[gene_sign]
            if prev_gene is not None and prev_gene[1] == gene_chr:
                adjacency = [
                    prev_gene[0],gene_name,
                    prev_gene[2],gene_orientation,'1'
                ]
                adjacencies.append(f'{" ".join(adjacency)}')
            prev_gene = [gene_name,gene_chr,gene_orientation]
    return adjacencies

''' 
Creates the DeCoSTAR input gene trees distribution file 
Compute a list of families for which the reconciled gene tree is available
'''
def create_gene_distribution_file(in_reconciliations_file, out_trees_file):
    '''
    input: 
    - dataset file with link from family to reconciled gene tree
    output: 
    - creates out_trees_file
    - list(str) of families for which a reonciliation is available
    '''
    family2reconciliation_path = data_family2reconciliation_path(
        in_reconciliations_file
    )
    reconciled_families = []
    with open(out_trees_file, 'w') as trees:
        for fam_id,reconciliation_file in family2reconciliation_path.items():
            trees.write(f'{reconciliation_file}\n')
            reconciled_families.append(fam_id)
    return reconciled_families

''' Creates the DeCoSTAR input adjacencies file '''
def create_adjacencies_file(
        in_gene_orders_file, in_families_file, in_reconciled_families,
        out_adjacencies_file
):
    '''
    input: 
    - dataset file with link from species to gene order file
    - dataset families file
    - list of reconciled families
    output: 
    creates out_adjacencies_file
    '''
    gene_order_files= data_species2gene_order_path(in_gene_orders_file)
    gene2family_map = data_gene2family(in_families_file)
    with open(out_adjacencies_file, 'w') as out_adjacencies:
        for species,gene_order_file in gene_order_files.items():
            species_adjacencies = decostar_gene_order2adjacencies_str(
                gene_order_file, gene2family_map, in_reconciled_families            
            )
            for adjacency in species_adjacencies:
                out_adjacencies.write(f'{adjacency}\n')


    
def main():
    in_gene_orders_file = sys.argv[1]
    in_reconciliations_file = sys.argv[2]
    in_families_file = sys.argv[3]
    out_adjacencies_file = sys.argv[4]
    out_trees_file = sys.argv[5]

    reconciled_families = create_gene_distribution_file(in_reconciliations_file, out_trees_file)
    create_adjacencies_file(in_gene_orders_file, in_families_file, reconciled_families, out_adjacencies_file)
        
if __name__ == "__main__":
    main()
