#!/usr/bin/env python3
# coding: utf-8

""" Reformat ALE recPhyloXML files to change species name and relabel loss and ancestral genes """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os

import xml.etree.ElementTree as ET

from newick_utils import newick_create_species_map
from recPhyloXML_utils import (
    xml_rename_species,
    xml_rename_losses,
    xml_rename_ancestral_genes,
    xml_reformat_file,
    xml_check_transfer
)

def xml_ALE_identify_loss(node):
    return node.text.endswith('|LOSS')

def xml_ALE_identify_transfer(node):
    return node.text.startswith('.T@')

def xml_ALE_identify_ancestral_gene(node):
    return (node.text.startswith('.') and not xml_ALE_identify_loss(node))

    
def main():
    in_data_species_tree = sys.argv[1]
    in_ale_species_tree = sys.argv[2]
    in_rec_xml_file = sys.argv[3]
    out_rec_xml_file = sys.argv[4]

    species_map = newick_create_species_map(in_ale_species_tree, in_data_species_tree)
    tree = ET.parse(in_rec_xml_file)
    if not xml_check_transfer(tree, xml_ALE_identify_transfer):
        xml_rename_species(tree, species_map)
        xml_rename_losses(tree, xml_ALE_identify_loss, 'loss')
        _ = xml_rename_ancestral_genes(tree, xml_ALE_identify_ancestral_gene, start_id=1)    
        out_rec_xml_file_tmp = f'{out_rec_xml_file}_tmp'
        tree.write(out_rec_xml_file_tmp)
        _ = xml_reformat_file(out_rec_xml_file_tmp, out_rec_xml_file)
        os.remove(out_rec_xml_file_tmp)

if __name__ == "__main__":
    main()


