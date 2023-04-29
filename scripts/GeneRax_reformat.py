#!/usr/bin/env python3
# coding: utf-8

""" Reformat GeneRax recPhyloXML files to be read by DeCoSTAR and creates a gene trees file """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.3"
__status__    = "Released"

import sys
import os

from recPhyloXML_utils import xml_reformat_file

def get_families_from_input(in_GeneRax_families_file):
    with open(in_GeneRax_families_file, 'r') as in_file:
        families = [
            f.rstrip()[2:]
            for f in in_file.readlines()
            if f.startswith('- ')
        ]
    return families

def reformat_reconciliations(families, results_dir, suffix):
    current_gene_id = 0 # current gene number
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

def create_gene_trees_file(families, results_dir, out_gene_trees_file):
    with open(out_gene_trees_file, 'w') as out_file:
        for fam_id in families:
            in_file = os.path.join(
                results_dir, 'results', fam_id,
                'geneTree.newick'
            )
            if os.path.isfile(in_file):
                out_file.write(f'{fam_id}\t{in_file}\n')

def main():
    in_GeneRax_families_file = sys.argv[1]
    results_dir = sys.argv[2]
    rec_ext = sys.argv[3]
    out_gene_trees_file = sys.argv[4]

    families = get_families_from_input(in_GeneRax_families_file)
    reformat_reconciliations(families, results_dir, rec_ext)
    create_gene_trees_file(families, results_dir, out_gene_trees_file)

if __name__ == "__main__":
    main()

