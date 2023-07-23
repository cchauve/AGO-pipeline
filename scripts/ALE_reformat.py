#!/usr/bin/env python3
# coding: utf-8

""" Reformat ALE recPhyloXML files to change species name and relabel loss and ancestral genes """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Released"

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

    # Creates a map from ALE species names to original species names
    species_map = newick_create_species_map(in_ale_species_tree, in_data_species_tree)
    # Read an ALE recPhyloXML file
    tree = ET.parse(in_rec_xml_file)
    # If the file includes an HGT, we do not create a reformatted file
    if not xml_check_transfer(tree, xml_ALE_identify_transfer):
        # Rename species
        xml_rename_species(tree, species_map)
        # Reformat losses
        xml_rename_losses(tree, xml_ALE_identify_loss, 'loss')
        # Reformat ancestral gene names with integers ID starting at 1
        _ = xml_rename_ancestral_genes(tree, xml_ALE_identify_ancestral_gene, start_id=1)
        # Create a temporary recPhyloXML file
        tmp_rec_file = f'{out_rec_xml_file}_tmp'
        tree.write(tmp_rec_file)
        # Reformat the temporary recPhyloXML file int the final recPhyloXML file
        _ = xml_reformat_file(tmp_rec_file, out_rec_xml_file)
        # Delete the temporary recPhyloXML file
        os.remove(tmp_rec_file)

if __name__ == "__main__":
    main()


