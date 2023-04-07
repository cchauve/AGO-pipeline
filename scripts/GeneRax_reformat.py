#!/usr/bin/env python3
# coding: utf-8

""" Reformat GeneRax recPhyloXML files to be read by DeCoSTAR """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os

from recPhyloXML_utils import xml_reformat_file

def main():
    in_GeneRax_families_file = sys.argv[1]
    results_dir = sys.argv[2]
    suffix = sys.argv[3]

    with open(in_GeneRax_families_file, 'r') as families:
        current_gene_id = 0 # current gene number
        families = [
            f.rstrip()[2:]
            for f in families.readlines()
            if f.startswith('- ')
        ]
        for fam_id in families:
            in_file = os.path.join(
                results_dir, 'reconciliations',
                f'{fam_id}_reconciliated.xml'
            )
            out_file = os.path.join(
                results_dir, 'reconciliations',
                f'{fam_id}{suffix}'
            )
            if os.path.isfile(in_file):
                current_gene_id = xml_reformat_file(
                    in_file, out_file,
                    start_id=current_gene_id
                )

if __name__ == "__main__":
    main()

