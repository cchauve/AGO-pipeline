#!/usr/bin/env python3
# coding: utf-8

""" Parsing recPhyloXML reconciled files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import xml.etree.ElementTree as ET

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

def xml_get_tree_root(in_file, tree):
    root = ET.parse(in_file).getroot()
    tag_pref = xml_get_prefix(root)
    tree_root = root.find(
        f'{tag_pref}{tree}'
    ).find(f'{tag_pref}phylogeny'
    ).find(f'{tag_pref}clade')
    return tree_root,tag_pref
def xml_get_species_tree_root(in_file):
    return xml_get_tree_root(in_file, 'spTree')
def xml_get_gene_tree_root(in_file):
    return xml_get_tree_root(in_file, 'recGeneTree')

def xml_parse_tree(root, tag_pref, output_type=1):
    ''' 
    input: XML root node
    output: 
    - 1: dict(node name(str) -> name of siblings (str/None))
    - 2: dict(node name(str) -> name of descendant leaves (str/None))
    '''
    def parse_clade_recursive(node, result, output_type):
        ''' Assumption: node is tagged <clade> '''
        name = xml_get_name(node, tag_pref=tag_pref)
        # Updating result dictionary
        children = node.findall(f'{tag_pref}clade')
        # Recursive calls
        leaves = []
        for child in children:
            leaves += parse_clade_recursive(child, result, output_type)
        if len(children) == 0 and name != 'loss': # Extant leaf
            leaves += [name]
        # Update output
        if output_type == 1 and len(children) == 2:
            child1 = xml_get_name(children[0], tag_pref=tag_pref)
            child2 = xml_get_name(children[1], tag_pref=tag_pref)
            result[child1] = child2
            result[child2] = child1
        elif output_type == 2 and name != 'loss':
            result[name] = leaves.copy()
        return leaves
    if output_type == 1:
        result = {xml_get_name(root, tag_pref=tag_pref): None}
    elif output_type == 2:
        result = {}
    parse_clade_recursive(root, result, output_type)
    return(result)


def xml_reformat_file(in_file, out_file, start_id=0):
    ''' Should be done using the XML libray '''
    with open(in_file, 'r') as in_xml, \
         open(out_file, 'w') as out_xml:
        out_xml.write('<recPhylo>\n')
        current_id = start_id
        for line in in_xml.readlines()[1:]:
            line1 = line.strip()
            if line1[0]!='<': continue
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
            else:
                out_xml.write(line)
    return(current_id)

def xml_map_leaves(in_file, tree=1, fam_id=None):
    '''
    input:
    in_file: recPhyloXML reconciliation
    tree: 1 is for species tree, 2 for gene tree
    fam_id: ID of the family
    output:
    map gene or (gene,fam_id) -> list of subtree leaves names
    '''
    root = ET.parse(in_file).getroot()
    tag_pref = xml_get_prefix(root)
    if tree == 1:
        tree_root = root.find(
            f'{tag_pref}spTree'
        ).find(f'{tag_pref}phylogeny'
        ).find(f'{tag_pref}clade')
    else:
         tree_root = root.find(
            f'{tag_pref}recGeneTree'
        ).find(f'{tag_pref}phylogeny'
        ).find(f'{tag_pref}clade')
         
    leaves_map = xml_parse_tree(tree_root, tag_pref, output_type=2)
    if fam_id is None:
        result = leaves_map
    else:
        result = {
            (gene,fam_ID): leaves_map[gene]
            for gene in leaves_map.keys()
        }
    return result
