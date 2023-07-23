#!/usr/bin/env python3
# coding: utf-8

""" Create Count input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "count"
__status__    = "Development"

import sys
sys.path.append('/home/chauvec/projects/ctb-chauvec/AGO-pipeline/scripts')
from data_utils import (
    data_family2genes,
    data_species_list,
    data_gene2species,
)

def create_family_content(gene2species_dict, species_list, family2genes_map):
    '''
    Creates a dictionary (family -> dict(species -> content))
    '''    
    family_content = {}
    for fam_id,genes_list in family2genes_map.items():
        family_content[fam_id] = {species: 0 for species in species_list}
        for gene in genes_list:
            species = gene2species_dict[gene]
            family_content[fam_id][species] += 1
    return family_content

def create_family_content_file(family_content, species_list, out_content_file):
    with open(out_content_file, 'w') as out_content:
        header = '\t'.join(['family']+species_list)
        out_content.write(header)
        for fam_id,content in family_content.items():
            content_str = '\t'.join(
                [fam_id]+[str(content[species]) for species in species_list]
            )
            out_content.write(f'\n{content_str}')

def main():
    in_gene_orders_file = sys.argv[1]
    in_families_file = sys.argv[2]
    out_content_file = sys.argv[3]

    species_list = data_species_list(in_gene_orders_file)
    family2genes_map = data_family2genes(in_families_file)
    gene2species_dict = data_gene2species(in_gene_orders_file)
    family_content = create_family_content(gene2species_dict, species_list, family2genes_map)
    create_family_content_file(family_content, species_list, out_content_file)
    
if __name__ == "__main__":
    main()
