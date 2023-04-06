#!/usr/bin/env python3
# coding: utf-8

""" Reformat SPPDCJ adjacencies to be in DeCoSTAR format per sepcies """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os

from data_utils import data_species2adjacencies_path

from DeCoSTAR_reformat import (
    decostar_sep,
    decostar_read_adjacencies
)

from DeCoSTAR_statistics import decostar_sign2extremity

''' Read the SPPDCJ adajcencies file and create a species-indexed dictionary '''
def read_sppdcj_adjacencies(in_adjacencies_file):
    '''
    input: SPPDCJ adjacencies file
    output: dict(species -> dict((gene1,ext1,gene2,ext2)->weight)
    '''
    adjacencies_dict = {}
    species_list = []
    with open(in_adjacencies_file,'r') as in_file:
        for adjacency_data in in_file.readlines()[1:]:
            adjacency = adjacency_data.rstrip().split('\t')
            species = adjacency[0]
            gene1 = adjacency[1].replace('_',decostar_sep)
            ext1 = adjacency[2]
            gene2 = adjacency[4].replace('_',decostar_sep)
            ext2 = adjacency[5]
            weight = adjacency[6]
            if (gene1,ext1)>(gene2,ext2):
                key = (gene2,ext2,gene1,ext1)
            else:
                key = (gene1,ext1,gene2,ext2)                
            if species not in species_list:
                adjacencies_dict[species] = {}
                species_list.append(species)
            adjacencies_dict[species][key] = weight
    return adjacencies_dict

''' Read the DeCoSTAR adajcencies file and create a species-indexed dictionary '''
def read_decostar_adjacencies(in_data_adjacencies_file):
    '''
    input: data adjacencies file (species<TAB>DeCoSTAR adjacencies file
    output: dict(species -> dict((gene1,ext1,gene2,ext2)->(gene1,sign1,gene2,sign2,weight1,weight2))
    '''
    species2adjacencies_files = data_species2adjacencies_path(in_data_adjacencies_file)
    species2adjacencies_aux = {}
    for species,adjacencies_file in species2adjacencies_files.items():
        species2adjacencies_aux[species] = decostar_read_adjacencies(adjacencies_file, species=species)
    # Reformating to replace signs by extremities
    adjacencies_dict = {}
    for species,adjacencies in species2adjacencies_aux.items():
        adjacencies_dict[species] = {}
        for (sp,g1,g2,sign1,sign2,w1,w2) in adjacencies:
            exts = decostar_sign2extremity[(sign1,sign2)]
            ext1,ext2 = exts[0],exts[1]
            if (g1,ext1) > (g2,ext2):
                key = (g2,ext2,g1,ext1)
            else:
                key = (g1,ext1,g2,ext2)
            adjacencies_dict[species][key] = [g1,sign1,g2,sign2,w1,w2]
    return adjacencies_dict

''' Filter DeCoSTAR adjacencies discarded by SPPDCJ '''
def filter_adjacencies(in_decostar_adjacencies, in_sppdcj_adjacencies):
    '''
    input: dictionaries
    dict(species -> dict((gene1,ext1,gene2,ext2)->weight)
    dict(species -> dict((gene1,ext1,gene2,ext2)->(gene1,sign1,gene2,sign2,weight1,weight2))
    output:
    subdictionary of DeCoSTAR adjcencies dictionary
    '''
    out_adjacencies = {}
    for species,adjacencies_dict in in_decostar_adjacencies.items():
        out_adjacencies[species] = {}
        sppdcj_adjacencies_keys = list(in_sppdcj_adjacencies[species].keys())
        for adjacency,adj_data in adjacencies_dict.items():
            if adjacency in sppdcj_adjacencies_keys:
                out_adjacencies[species][adjacency] = adj_data
    return out_adjacencies

''' Write the filtered adjacncies '''
def write_adjacencies(adjacencies_dict,out_dir):
    for species,adjacencies_dict in adjacencies_dict.items():
        out_adjacencies_path = os.path.join(out_dir, f'{species}_adjacencies.txt')
        with open(out_adjacencies_path,'w') as out_adjacencies_file:
            for (g1,ext1,g2,ext2),adj_data in adjacencies_dict.items():
                adj_str = ' '.join(adj_data)
                out_adjacencies_file.write(f'{adj_str}\n')

def main():
    in_data_adjacencies_file = sys.argv[1]
    in_sppdcj_adjacencies_file = sys.argv[2]
    out_dir = sys.argv[3]
    # Reading SPPDCJ adjacencies
    sppdcj_adjacencies = read_sppdcj_adjacencies(in_sppdcj_adjacencies_file)    
    # Reading DeCoSTAR adjacencies
    decostar_adjacencies = read_decostar_adjacencies(in_data_adjacencies_file)
    # Filter DeCoSTAR adjacencies
    filtered_adjacencies = filter_adjacencies(decostar_adjacencies,sppdcj_adjacencies)
    write_adjacencies(filtered_adjacencies,out_dir)

if __name__ == "__main__":
    main()
