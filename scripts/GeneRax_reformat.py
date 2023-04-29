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

# Suffix of reconciliation files created by GeneRax
GENERAX_XML_SUFFIX = '_reconciliations.xml'
# Nam of a GeneRax gene tree in Newick format
GENERAX_GT_NEWICK = 'geneTree.newick'

''' Read families ID from a GeneRax families file '''
def generax_get_families_from_input(in_generax_families_file):
    '''
    input: path to GeneRax families file
    output: list of families ID
    '''
    with open(in_generax_families_file, 'r') as in_file:
        generax_families = [
            f.rstrip()[2:]
            for f in in_file.readlines()
            if f.startswith('- ')
        ]
    return generax_families

''' Reformat the recPhyloXML files created by GeneRax '''
def generax_reformat_reconciliations(generax_families, results_dir, suffix):
    '''
    input: 
    - list of GeneRax families ID
    - directory containing GeneRax results
    - suffix of refortmated reconciliations files
    output:
    - creates one reformatted file for every GeneRax reconciliation
    - labels all ancestral genes by integers in increasing order (starting at 0)
    '''
    current_gene_id = 0 # current gene number
    for fam_id in generax_families:
        in_file = os.path.join(
            results_dir, 'reconciliations', f'{fam_id}{GENERAX_XML_SUFFIX}'
        )
        out_file = os.path.join(
            results_dir, 'reconciliations', f'{fam_id}{suffix}'
        )
        if os.path.isfile(in_file):
            current_gene_id = xml_reformat_file(
                in_file, out_file, start_id=current_gene_id
            )

''' Creates a tabulated file <family ID><TA><GeneRax gene tree file path> '''
def generax_create_gene_trees_file(generax_families, results_dir, out_gene_trees_file):
    '''
    input: 
    - list of families ID
    - directory containing GeneRax results
    - tabulated file to create
    output:
    - creates out_gene_trees_file
    '''
    with open(out_gene_trees_file, 'w') as out_file:
        for fam_id in generax_families:
            gt_file = os.path.join(
                results_dir, 'results', fam_id, GENERAX_GT_NEWICK
            )
            if os.path.isfile(gt_file):
                out_file.write(f'{fam_id}\t{gt_file}\n')

def main():
    in_generax_families_file = sys.argv[1]
    results_dir = sys.argv[2]
    rec_ext = sys.argv[3]
    out_gene_trees_file = sys.argv[4]

    # Read GeneRax families ID from GenRax families file
    generax_families = generax_get_families_from_input(
        in_generax_families_file
    )
    # Reformat GeneRax reconciliations files
    generax_reformat_reconciliations(
        generax_families, results_dir, rec_ext
    )
    # Creates a gene trees file from GeneRax gene trees
    generax_create_gene_trees_file(
        generax_families, results_dir, out_gene_trees_file
    )

if __name__ == "__main__":
    main()

