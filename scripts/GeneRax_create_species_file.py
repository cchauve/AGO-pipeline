#!/usr/bin/env python3
# coding: utf-8

""" Create GeneRax species list files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os
from newick_utils import newick_get_species_status

def main():
    in_species_tree_file = sys.argv[1]
    out_species_file = sys.argv[2]

    species = newick_get_species_status(in_species_tree_file)
    with open(out_species_file, 'w') as out_species:
        for species,status in species.items():
            out_species.write(f'{species}\t{status}\n')
        
if __name__ == "__main__":
    main()
