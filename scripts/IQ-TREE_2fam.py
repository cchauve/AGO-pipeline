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
    in_alignment_file = sys.argv[1]
    out_tree_file = sys.argv[2]

    genes = []
    with open(in_alignment_file) as in_file:
        for line in in_file.readlines():
            if line[0] == '>':
                genes.append(line.rstrip()[1:])

    with open(out_tree_file, 'w') as out_file:
        out_file.write(f'({genes[0]}:1.0,{genes[1]}:1.0);')
        
if __name__ == "__main__":
    main()
