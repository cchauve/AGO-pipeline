#!/usr/bin/env python3
# coding: utf-8

""" Creates trees for families with 2 genes """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Development"

import sys
import os

from data_utils import data_family2genes


def main():
    in_families_file = sys.argv[1]
    in_family = sys.argv[2]
    out_tree_file = sys.argv[3]
    
    family_2_genes = data_family2genes(in_families_file)
    genes = family_2_genes[in_family]

    with open(out_tree_file, 'w') as out_file:
        out_file.write(f'({genes[0]}:1.0,{genes[1]}:1.0);')
        
if __name__ == "__main__":
    main()
