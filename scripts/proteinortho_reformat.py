#!/usr/bin/env python3
# coding: utf-8

""" Reformat proteinrtho gene families file """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Development"

import sys

def main():
    in_OG_file = sys.argv[1]
    out_family_file = sys.argv[2]

    with open(in_OG_file) as in_file, open(out_family_file, 'w') as out_file:
        fam_nb = 1
        for in_fam in in_file.readlines():
            if in_fam[0] != '#':
                fam_split = in_fam.rstrip().split('\t')
                fam_id = f'PO{fam_nb}'
                fam_nb += 1
                fam_genes_list = []
                for species_gene in fam_split[3:]:
                    fam_genes_list += species_gene.split(',')
                fam_genes_str = ' '.join(fam_genes_list)
                out_file.write(f'{fam_id}\t{fam_genes_str}\n')

if __name__ == "__main__":
    main()


