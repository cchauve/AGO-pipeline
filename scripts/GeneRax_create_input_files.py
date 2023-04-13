#!/usr/bin/env python3
# coding: utf-8

""" Create GeneRax input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

import sys
import os

from data_utils import (
    data_family2genes,
    data_gene2species,
    data_family2alignment_path
)

''' Write the GeneRax families file from paths to alignments '''
def GeneRax_write_families_file(
        in_family2genes, in_gene2species, in_family2alignment,
        in_subst_model,
        out_map_files_dir, out_families_file
):
    with open(out_families_file, 'w') as out_families:
        out_families.write('[FAMILIES]')
        for fam_id,alignment_file in in_family2alignment.items():
            # Writing the gene to species map file
            out_map_file = os.path.join(
                out_map_files_dir,
                f'map_{fam_id}.txt'
            )
            with open(out_map_file, 'w') as out_map:
                for gene in in_family2genes[fam_id]:
                    out_map.write(
                        f'{gene}\t{in_gene2species[gene]}\n'
                    )
            # Updating the families file
            out_families.write(
                f'\n- {fam_id}'
                f'\nalignment = {alignment_file}'
                f'\nmapping = {out_map_file}'
                f'\nsubst_model = {in_subst_model}'
            )

def main():
    in_families_file = sys.argv[1]
    in_gene_orders_file = sys.argv[2]
    in_alignments_file = sys.argv[3]
    in_suffix = sys.argv[4]
    in_subst_model = sys.argv[5]
    out_families_file = sys.argv[6]
    out_map_files_dir = sys.argv[7]

    # Read all families
    family2genes = data_family2genes(in_families_file)
    # Read all genes
    gene2species = data_gene2species(in_gene_orders_file)
    # Read alignmed families
    family2alignment = data_family2alignment_path(
        in_alignments_file, in_suffix
    )
    # Create GeneRax input files
    GeneRax_write_families_file(
        family2genes, gene2species, family2alignment, in_subst_model,
        out_map_files_dir, out_families_file
    )

        
if __name__ == "__main__":
    main()
