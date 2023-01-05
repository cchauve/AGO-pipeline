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


def xml_parse_tree(root, tag_pref, output_type=1):
    ''' 
    input: XML root node
    output: 
    - 1: dict(species name(str) -> name of siblings (str/None))
    - 2: dict(species name(str) -> name of descendant leaves (str/None))
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
        if len(children) == 0: # Leaf
            leaves += [name]
        # Update output
        if output_type == 1 and len(children) == 2:
            child1 = xml_get_name(children[0], tag_pref=tag_pref)
            child2 = xml_get_name(children[1], tag_pref=tag_pref)
            result[child1] = child2
            result[child2] = child1
        elif output_type == 2:
            result[name] = leaves.copy()
        return leaves
    result = {xml_get_name(root, tag_pref=tag_pref): None}
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
