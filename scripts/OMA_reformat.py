#!/usr/bin/env python3
# coding: utf-8

""" Reformat OMA gene families file """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Development"

import sys
import os
from fasta_utils import fasta_get_names

def reformat_OG_results(in_OG_file, out_family_OG_file):
    with open(in_OG_file) as in_file, open(out_family_OG_file, 'w') as out_file:
        for in_fam in in_file.readlines():
            if in_fam[0] != '#':
                fam_split = in_fam.rstrip().split('\t')
                fam_id = fam_split[0]
                fam_genes = ' '.join([
                    ':'.join(x.split(':')[1:])
                    for x in fam_split[1:]
                ])                
                out_file.write(f'{fam_id}\t{fam_genes}\n')

def reformat_HOG_results(in_HOG_dir, out_family_HOG_file):
    in_HOG_files = [
        os.path.join(in_HOG_dir, in_file)
        for in_file in os.listdir(in_HOG_dir)
        if os.path.splitext(in_file)[1] == '.fa'
    ]
    with open(out_family_HOG_file, 'w') as out_file:
        for in_HOG_file in in_HOG_files:
            fam_id = os.path.splitext(os.path.basename(in_HOG_file))[0]
            fam_genes = ' '.join(fasta_get_names(in_HOG_file))
            out_file.write(f'{fam_id}\t{fam_genes}\n')

def main():
    in_results_dir = sys.argv[1]
    out_family_file_prefix = sys.argv[2]

    in_OG_file = os.path.join(in_results_dir, 'OrthologousGroups.txt')
    out_family_OG_file = f'{out_family_file_prefix}_OG.txt'
    reformat_OG_results(in_OG_file, out_family_OG_file)

    in_HOG_dir = os.path.join(in_results_dir, 'HOGFasta')
    if os.path.isdir(in_HOG_dir):
        out_family_HOG_file = f'{out_family_file_prefix}_HOG.txt'
        reformat_HOG_results(in_HOG_dir, out_family_HOG_file)

if __name__ == "__main__":
    main()


