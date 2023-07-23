#!/usr/bin/env python3
# coding: utf-8

""" Data handling utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "count"
__status__    = "Development"

import sys
from collections import defaultdict

def gene_families_size_distribution(in_families_file):
    out_distribution = defaultdict(int)
    max_size = 0
    with open(in_families_file) as in_file:
        for family in in_file.readlines():
            family_size = len(family.rstrip().split('\t')[1].split())
            if family_size > max_size:
                max_size = family_size
            out_distribution[family_size] += 1
    for family_size in range(max_size+1):
        if out_distribution[family_size] > 0:
            print(f'{family_size}\t{out_distribution[family_size]}')

gene_families_size_distribution(sys.argv[1])
