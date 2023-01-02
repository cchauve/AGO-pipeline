#!/usr/bin/env python3
# coding: utf-8

""" Create GeneRax input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os

def read_families(in_families_file):
    family2genes = {}
    with open(in_families_file, 'r') as families:
        for family in families.readlines():
            fam_id,genes = family.rstrip().split('\t')
            family2genes[fam_id] = genes.split()
    return family2genes

def read_genes(in_gene_orders_file):
    gene2species = {}
    with open(in_gene_orders_file, 'r') as gene_orders:
        for species_gene_order in gene_orders.readlines():
            species,gene_order_file = species_gene_order.rstrip().split('\t')
            with open(gene_order_file, 'r') as gene_order:            
               for gene in gene_order.readlines():
                   gene_name = gene.split('\t')[0]
                   gene2species[gene_name] = species
    return gene2species

def read_alignments(in_alignments_file, in_suffix):
    family2alignment = {}
    with open(in_alignments_file, 'r') as alignments:
        for family in alignments.readlines():
            fam_id,alignment_file = family.rstrip().split('\t')
            if alignment_file.endswith(in_suffix):
                family2alignment[fam_id] = alignment_file
    return family2alignment

def main():
    in_families_file = sys.argv[1]
    in_gene_orders_file = sys.argv[2]
    in_alignments_file = sys.argv[3]
    in_suffix = sys.argv[4]
    in_subst_model = sys.argv[5]
    out_families_file = sys.argv[6]
    out_map_files_dir = sys.argv[7]

    # Read all families
    family2genes = read_families(in_families_file)
    # Read all genes
    gene2species = read_genes(in_gene_orders_file)
    # Read alignmed families
    family2alignment = read_alignments(in_alignments_file, in_suffix)
    # Create GeneRax input files
    with open(out_families_file, 'w') as out_families:
        out_families.write('[FAMILIES]')
        for fam_id in family2alignment.keys():
            out_families.write(f'\n- {fam_id}')
            out_families.write(f'\nalignment = {family2alignment[fam_id]}')
            out_map_file = os.path.join(out_map_files_dir, f'map_{fam_id}.txt')
            with open(out_map_file, 'w') as out_map:
                for gene in family2genes[fam_id]:
                    out_map.write(f'{gene}\t{gene2species[gene]}\n')
            out_families.write(f'\nmapping = {out_map_file}')
            out_families.write(f'\nsubst_model = {in_subst_model}')
        
if __name__ == "__main__":
    main()
