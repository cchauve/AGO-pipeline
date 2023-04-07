#!/usr/bin/env python3
# coding: utf-8

""" Parsing recPhyloXML reconciled files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

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
