#!/usr/bin/env python3
# coding: utf-8

""" Reformat reconciliations computed by ecceTERA within DeCoSTAR """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.3"
__status__    = "Released"

import sys
import os
import xml.etree.ElementTree as ET

from recPhyloXML_utils import xml_rename_species

'''
Reads DeCoSTAR original and reformatted genes 
Creates dict(ecceTERA species -> data species)
Creates dict(ecceTERA family -> data family
'''
def eccetera_read_results(in_genes_file1, in_genes_file2, sep='|'):
    '''
    input:
    - original and reformatted genes file
    output:
    - dict(ecceTERA species -> data species)
    - dict(ecceTERA family -> data family)
    '''
    species_dict,families_dict = {},{}
    # Reading original genes
    data,data_idx = {},0
    with open(in_genes_file1, 'r') as in_genes:
        for gene_data in in_genes.readlines():
            gene_split = gene_data.rstrip().split()
            species_id,gene = gene_split[0:2]
            if len(gene_split)>2:
                family_id = gene.split(sep)[0]
                data[data_idx] = (species_id,family_id)
            else:
                data[data_idx] = (species_id,family_id)
            data_idx += 1
    # Reading reformated genes
    data_idx = 0
    with open(in_genes_file2, 'r') as in_genes:
        for gene_data in in_genes.readlines():
            gene_split = gene_data.rstrip().split()
            species_id,gene = gene_split[0:2]
            family_id,gene_id = gene.split(sep,1)[0:2]
            (sp,f) = data[data_idx]            
            species_dict[sp] = species_id
            species_dict[species_id] = species_id
            families_dict[f] = family_id
            data_idx += 1
    return species_dict,families_dict

''' Read the recPhyloXML species tree created by DeCoSTAR '''
def eccetera_read_species_tree(in_species_tree_file):
    '''
    input: recPhyloXML species tree of DeCoSTAR
    output: XML string for encoding the species tree
    '''
    species_tree_str = '<spTree>'
    append_lines = False
    with open(in_species_tree_file, 'r') as in_sp_tree:
        for xml_line in in_sp_tree.readlines():
            if xml_line.lstrip().startswith('<phylogeny'):
                append_lines = True
            elif xml_line.lstrip().startswith('</phyloxml'):
                append_lines = False
            if append_lines:
                species_tree_str += f'\n{xml_line.rstrip()}'
    species_tree_str += '\n</spTree>'
    return species_tree_str

''' 
Read the DeCoSTAR file containing all reconciliations in recPhyloXML format, without a species tree 
and creates one temporary recPhyloXML file per gene family
'''
def eccetera_read_reconciliations(in_reconciliations_file, in_sp_xml_str, families_map, out_dir):
    ''' 
    input: 
    - path to the reconciliations file
    - species tree XML string
    - map from DeCoSTAR families ID to original families ID
    - directory where to write temporary recPhyloXML files
    output:
    dict (DeCoSTAR family ID -> path to corresponding temporary recPhyloXML file
    '''
    family_idx = 0
    out_reconciliations_files = {}
    with open(in_reconciliations_file, 'r') as in_reconciliations:
        for xml_line in in_reconciliations.readlines():
            if xml_line.lstrip().startswith('<recGeneTree'):
                family_id = families_map[str(family_idx)]
                family_idx += 1
                reconciliation_str = '<recPhylo>\n'
                reconciliation_str += in_sp_xml_str
                reconciliation_str += '\n<recGeneTree>'
            elif xml_line.lstrip().startswith('</recGeneTree'):
                reconciliation_str += '\n</recGeneTree>\n</recPhylo>'
                out_file_tmp_name = os.path.join(out_dir, f'{family_id}.xml')
                with open(out_file_tmp_name, 'w') as out_file_tmp:
                    out_file_tmp.write(reconciliation_str)
                out_reconciliations_files[str(family_idx-1)] = (family_id,out_file_tmp_name)
            elif family_idx > 0:
                reconciliation_str += f'\n{xml_line.rstrip()}'
    return out_reconciliations_files

''' Writing reconcilitions files '''
def eccetera_write_reconciliations(in_reconciliations_files, species_map, out_dir, out_xml_ext, out_reconciliations_file):
    with open(out_reconciliations_file, 'w') as out_file:
        for family_idx,(family_id,tmp_rec_file) in in_reconciliations_files.items():
         tree = ET.parse(tmp_rec_file)
         xml_rename_species(tree, species_map)
         out_reconciliation_file = os.path.join(out_dir, f'{family_id}{out_xml_ext}')
         tree.write(out_reconciliation_file)
         out_file.write(f'{family_id}\t{out_reconciliation_file}\n')
            

def main():
    in_genes_file1 = sys.argv[1] # DeCoSTAR genes file
    in_genes_file2 = sys.argv[2] # Reformatted genes file
    in_sp_xml_file = sys.argv[3] # Path to DeCoSTAR species tree XML file
    in_reconciliations_file = sys.argv[4] # Path to DeCoSTAR reconciliations file
    out_dir = sys.argv[5] # Directory where to write reconciliations files
    out_xml_ext = sys.argv[6] # Extension to recPhyloXML files
    out_reconciliations_file = sys.argv[7] # Data set reconciliations file

    species_map,families_map = eccetera_read_results(in_genes_file1, in_genes_file2)
    xml_sp_str = eccetera_read_species_tree(in_sp_xml_file)
    tmp_reconciliations_files = eccetera_read_reconciliations(
        in_reconciliations_file, xml_sp_str, families_map, out_dir
    )
    eccetera_write_reconciliations(
        tmp_reconciliations_files, species_map, out_dir, out_xml_ext, out_reconciliations_file
    )
            
if __name__ == "__main__":
    main()

