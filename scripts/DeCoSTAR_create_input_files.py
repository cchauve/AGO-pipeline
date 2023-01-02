#!/usr/bin/env python3
# coding: utf-8

""" Create DeCoSTAR input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys

def read_families(in_families_file):
    gene2family = {}
    with open(in_families_file, 'r') as families:
        for family in families.readlines():
            fam_id,genes = family.rstrip().split('\t')
            for gene in genes.split():
                gene2family[gene] = fam_id
    return gene2family

def create_adjacencies(in_gene_orders_file, gene2family, reconciled_families, out_adjacencies_file):
    orientation = {'1': '+', '0': '-'}
    
    with open(out_adjacencies_file, 'w') as adjacencies, \
         open(in_gene_orders_file, 'r') as gene_orders:
        for species_data in gene_orders.readlines():
            species,gene_order_file = species_data.rstrip().split()
            with open(gene_order_file, 'r') as gene_order:
                prev_gene = None
                for gene in gene_order.readlines():
                    gene_data = gene.rstrip().split()
                    gene_name = gene_data[0]
                    if gene2family[gene_name] in reconciled_families:
                        gene_chr,gene_sign = gene_data[5],gene_data[1]
                        gene_orientation = orientation[gene_sign]
                        if prev_gene is not None and prev_gene[1] == gene_chr:
                            adj = [prev_gene[0], gene_name] + \
                                [prev_gene[2],gene_orientation,'1']
                            adjacencies.write(f'{" ".join(adj)}\n')
                        prev_gene = [gene_name,gene_chr,gene_orientation]

def create_gene_distribution(in_reconciliations_file, out_trees_file):
    families = []
    with open(out_trees_file, 'w') as trees, \
         open(in_reconciliations_file, 'r') as reconciliations:
        for reconciliation in reconciliations.readlines():
            reconciliation_data = reconciliation.rstrip().split()
            fam_id = reconciliation_data[0]
            reconciliation_file = reconciliation_data[1]
            trees.write(f'{reconciliation_file}\n')
            families.append(fam_id)
    return families
    
def main():
    in_gene_orders_file = sys.argv[1]
    in_reconciliations_file = sys.argv[2]
    in_families_file = sys.argv[3]
    out_adjacencies_file = sys.argv[4]
    out_trees_file = sys.argv[5]

    reconciled_families = create_gene_distribution(in_reconciliations_file, out_trees_file)
    gene2family = read_families(in_families_file)
    create_adjacencies(in_gene_orders_file, gene2family, reconciled_families, out_adjacencies_file)
        
if __name__ == "__main__":
    main()
