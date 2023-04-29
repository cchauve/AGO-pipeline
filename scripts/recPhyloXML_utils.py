#!/usr/bin/env python3
# coding: utf-8

""" Parsing recPhyloXML reconciled files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.3"
__status__    = "Released"

import sys
import xml.etree.ElementTree as ET

ST_TAG = 'spTree'
REC_TAG = 'recGeneTree'

def xml_get_tag(node):
    ''' Returns the tag of a node without its prefix {...} '''
    return(node.tag.rpartition('}')[2])

def xml_get_prefix(node):
    ''' Returns the prefix of tag '''
    pref = node.tag.rpartition("}")[0]
    if len(pref)>0: return(pref+'}')
    else: return(pref)

def xml_get_text(node):
    ''' Returns the text associated to a node '''
    if node.text is not None: return((node.text).strip())
    else: return('')

def xml_get_name(node, tag_pref=''):
    ''' 
    Returns the name of a clade node
    Assumption: any clade node has a name 
    '''
    return(xml_get_text(node.find(f'{tag_pref}name')))

def xml_get_rec_species(node):
    ''' Returns the species of a eventRec node '''
    return(node.get(f'speciesLocation'))

def xml_get_rec_event(node, tag_pref=''):
    return node.find(f'{tag_pref}eventsRec')

def _xml_get_tree_root(xml_tree, tree):
    root = xml_tree.getroot()
    tag_pref = xml_get_prefix(root)
    tree_root = root.find(
        f'{tag_pref}{tree}'
    ).find(f'{tag_pref}phylogeny'
    ).find(f'{tag_pref}clade')
    return tree_root,tag_pref

def xml_get_tree_root(in_file, tree):
    xml_tree = ET.parse(in_file)
    return _xml_get_tree_root(xml_tree, tree)

def xml_get_species_tree_root(in_file):
    return xml_get_tree_root(in_file, ST_TAG)

def xml_get_gene_tree_root(in_file):
    return xml_get_tree_root(in_file, REC_TAG)

def xml_get_species(in_file):
    ''' Get species list from the species tree '''
    root,_ = xml_get_species_tree_root(in_file)
    species_list = []
    for node in root.iter('name'):
        species_list.append(node.text)
    return species_list

def xml_get_extant_leaves(in_file):
    ''' Get list of extant leaves names '''
    root,tag_pref = xml_get_gene_tree_root(in_file)
    genes_list = []
    for node in root.iter('clade'):
        name = xml_get_name(node, tag_pref=tag_pref)
        children = node.findall(f'{tag_pref}clade')
        if len(children) == 0 and name != 'loss': # Extant leaf
            genes_list.append(xml_get_name(node, tag_pref=tag_pref))
    return genes_list

''' Rename all species according to a dictionary in species tree '''
def _xml_rename_species_st(tree, species_map):
    root,_ = _xml_get_tree_root(tree, ST_TAG)
    for node in root.iter('name'):
        species = node.text
        node.text = species_map[species]

''' Rename all species according to a dictionary in gene tree '''
def _xml_rename_species_rec(tree, species_map):
    root,_ = _xml_get_tree_root(tree, REC_TAG)
    for node in root.iter():
        if 'speciesLocation' in node.attrib:
            species = node.attrib['speciesLocation']
            node.attrib['speciesLocation'] = species_map[species]

''' Rename all species according to a dictionary '''
def xml_rename_species(tree, species_map):
    _xml_rename_species_st(tree, species_map)
    _xml_rename_species_rec(tree, species_map)

''' Rename loss nodes '''
def xml_rename_losses(tree, identify_loss, loss_name):
    root,_ = _xml_get_tree_root(tree, REC_TAG)
    for node in root.iter('name'):
        if identify_loss(node):
            node.text = loss_name

''' Rename all ancestral genes numerically increasingly '''
def xml_rename_ancestral_genes(tree, identify_ancestral_gene, start_id=1):
    root,_ = _xml_get_tree_root(tree, REC_TAG)
    current_id = start_id
    for node in root.iter('name'):
        if identify_ancestral_gene(node):
            node.text = str(current_id)
            current_id += 1
    return current_id

''' Check if a tree contains HGT '''
def xml_check_transfer(tree, identify_transfer):
    result = False
    root,tag_pref = _xml_get_tree_root(tree, REC_TAG)
    for node in root.iter('name'):        
        if identify_transfer(node):
            return True
    return result
        
''' 
Reformat a recphyloxml file that does not have the proper format for DeCoSTAR
Also relabel the internal nodes with no name
'''
def xml_reformat_file(in_file, out_file, start_id=0):
    ''' Should be done using the XML libray '''
    with open(in_file, 'r') as in_xml, \
         open(out_file, 'w') as out_xml:
        out_xml.write('<recPhylo>\n')
        current_id = start_id
        for line in in_xml.readlines()[1:]:
            line1 = line.strip()
            if line1.0.3]!='<': continue
            if line1 == '<name></name>':
                out_xml.write(line.replace('><', f'>{current_id}<'))
                current_id += 1
            elif line1.startswith('<speciation'):
                out_xml.write(line.replace('/>', '></speciation>'))
            elif line1.startswith('<leaf'):
                out_xml.write(line.replace('/>', '></leaf>'))
            elif line1.startswith('<duplication'):
                out_xml.write(line.replace('/>', '></duplication>'))
            elif line1.startswith('<loss'):
                out_xml.write(line.replace('/>', '></loss>'))
            elif line1.startswith('<speciationLoss'):
                out_xml.write(line.replace('/>', '></speciationLoss>'))
            elif line1.startswith('<branchingOut'):
                out_xml.write(line.replace('/>', '></branchingOut>'))
            else:
                out_xml.write(line)
    return(current_id)
