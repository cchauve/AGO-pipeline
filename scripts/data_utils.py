#!/usr/bin/env python3
# coding: utf-8

""" Create DeCoSTAR input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys

# Auxiliary generic functions

''' Creates a map from a 2-fields tabulate file '''
def _data_create_map(in_file, sep='\t'):
    '''
    input: path to dataset tabulated file with 2 fields separated by  separator
    output: dict(index -> gene order file path)
    '''
    result_map = {}
    with open(in_file, 'r') as in_data:
        for index_data in in_data.readlines():
            index,data = index_data.rstrip().split(sep)
            result_map[index] = data
    return result_map

''' Creates an inverse map from a tabulated file '''
def _data_create_inverse_map(in_file, sep1='\t', sep2=' '):
    '''
    input:
    - tabulated indexed file
    - separator between idex and data
    - separator between data list
    output:
    dict(data item -> index)
    '''
    result_map = {}
    with open(in_file, 'r') as in_data:
        for index_data in in_data.readlines():
            index,data = index_data.rstrip().split(sep1)
            data_items = data.split(sep2)
            for data_item in data_items:
                result_map[data_item] = index
    return result_map

# Data specific fucntions

''' Creates a map from gene to its family '''
def data_gene2family(in_families_file):
    '''
    input: path to gene families file
    output: dict(gene name -> family ID)
    '''
    return _data_create_inverse_map(in_families_file):

''' Creates a map from species to gene order file '''
def data_species2gene_order_path(in_gene_orders_file):
    '''
    input: path to dataset gene orders file
    output: dict(species -> gene order file path)
    '''
    return _data_create_map(in_gene_orders_file)

''' Creates a map from species to adjacencies file '''
def data_species2adjacencies_path(in_adjacencies_file):
    '''
    input: path to dataset gene orders file
    output: dict(species -> adjacencies file path)
    '''
    return _data_create_map(in_adjacencies_file)

''' Creates a map from family to reconciliation file '''
def data_family2reconciliation_path(in_reconciliations_file):
    '''
    input: path to dataset reconciliations file
    output: dict(family -> reconciliation path)
    '''
    return _data_create_map(in_reconciliations_file)

''' Creates a map from reconciliation file to family '''
def data_reconciliation_path2family(in_reconciliations_file):
    '''
    input: path to dataset reconciliations file
    output: dict(family -> reconciliation path)
    '''
    return _data_create_inverse_map(in_reconciliations_file)


''' Creates a list of species '''
def data_species_list(in_file):
    '''
    input: path to file indexed by species
    output: list of species in file
    '''
    return list(_data_create_map(in_file).keys())
    
