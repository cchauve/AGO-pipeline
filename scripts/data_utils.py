#!/usr/bin/env python3
# coding: utf-8

""" Data handling utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

import sys
from operator import itemgetter
from newick_utils import (
    newick_get_species,
    newick_check_rooted,
    newick_check_internal_names,
    newick_get_gene_trees_leaves
)
from fasta_utils import fasta_get_names

# Auxiliary generic functions

''' Creates a map from a tabulated file '''
def _data_create_map(in_file, sep1='\t', sep2=None):
    '''
    input: path to dataset tabulated file with 2 fields 
    separated by  sep1; if sep2 is not None, the second field is 
    split according to it
    output: dict(index -> gene order file path)
    '''
    result_map = {}
    with open(in_file, 'r') as in_data:
        for index_data in in_data.readlines():
            index_data_split = index_data.rstrip().split(sep1)
            index = index_data_split[0]
            if len(index_data_split)==1:
                result_map[index] = []
            else:
                data = index_data_split[1]
                if sep2 is None:
                    result_map[index] = data
                else:
                    result_map[index] = data.split(sep2)
    return result_map

''' Creates an inverse map from a tabulated file '''
def _data_create_inverse_map(in_file, sep1='\t', sep2=' '):
    '''
    input:
    - tabulated indexed file
    - separator between index and data
    - separator between data list
    output:
    dict(data item -> index)
    '''
    result_map = {}
    with open(in_file, 'r') as in_data:
        for index_data in in_data.readlines():
            index,data = index_data.rstrip().split(sep1)
            if sep2 is None:
                result_map[data] = index
            else:
                data_items = data.split(sep2)
                for data_item in data_items:
                    result_map[data_item] = index
    return result_map

# Data specific functions

''' Creates a map from gene to its family '''
def data_gene2family(in_families_file):
    '''
    input: path to gene families file
    output: dict(gene name -> family ID)
    '''
    return _data_create_inverse_map(in_families_file)

''' Creates a map from family to the list of its genes '''
def data_family2genes(in_families_file):
    '''
    input: path to gene families file
    output: dict(family ID -> list(genes))
    '''
    return _data_create_map(in_families_file, sep2=' ')
    
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

''' Creates a map from family to sequences file '''
def data_family2sequences_path(in_sequences_file):
    '''
    input: path to dataset sequences file
    output: dict(family -> sequences path)
    '''
    return _data_create_map(in_reconciliations_file)

''' Creates a map from family to alignment file '''
def data_family2alignment_path(in_alignments_file, in_suffix):
    '''
    input: path to dataset alignments file
    output: dict(family -> alignment path) if path ends by in_suffix
    '''
    family2alignment_path = {}
    with open(in_alignments_file, 'r') as alignments:
        for family in alignments.readlines():
            fam_id,alignment_file = family.rstrip().split('\t')
            if alignment_file.endswith(in_suffix):
                family2alignment_path[fam_id] = alignment_file
    return family2alignment_path

''' Creates a map from family to gene tree(s) file '''
def data_family2genetree_path(in_gene_trees_file):
    '''
    input: path to dataset gene trees file
    output: dict(family -> gene tree(s) path)
    '''
    return _data_create_map(in_gene_trees_file)

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

''' Creates a dict(gene -> species from gene orders files) '''
def data_gene2species(in_gene_orders_file):
    gene2species = {}
    species2gene_order_file = _data_create_map(in_gene_orders_file)
    for species,gene_order_file in species2gene_order_file.items():
        with open(gene_order_file, 'r') as gene_order:            
            for gene_data in gene_order.readlines():
                gene = gene_data.split('\t')[0]
                gene2species[gene] = species
    return gene2species

''' Creates a map between species '''
def data_species_map(in_species_file):
    '''
    input: path to species files
    output: dict(species_name -> sorted extant descendants (weak))
    '''
    sorted_descendants_map = {
        s: sorted(l) for s,l in _data_create_map(in_species_file, sep2=' ').items()
    }
    return sorted_descendants_map


''' Create an equivalence map between keys of 2 data maps '''
def data_create_equivalence_map(in_map_1, in_map_2, direction=1):
    '''
    input: 2 maps of the form key -> data
    output: map between keys
    '''
    nodes_map_1to2,nodes_map_2to1 = {},{}
    for s1 in in_map_1.keys():
        for s2 in in_map_2.keys():
            if in_map_1[s1] == in_map_2[s2]:
                nodes_map_1to2[s1] = s2
                nodes_map_2to1[s2] = s1
    if direction==1:
        return nodes_map_1to2
    elif direction==2:
        return nodes_map_2to1

''' Read a genes order file data '''
def data_read_gene_order_file(in_gene_order_file):
    '''
    input: path to genes order file for a species
    output: list of (name,chr,start,end,sign) sorted by chromosome and increasing start coordinate
    '''    
    gene_order = []
    with open(in_gene_order_file, 'r') as in_gene_order:
        for gene in in_gene_order.readlines():
            gene_data = gene.rstrip().split()
            gene_name = gene_data[0]
            gene_start,gene_end = int(gene_data[2]),int(gene_data[3])
            gene_chr,gene_sign = gene_data[5],gene_data[1]
            gene_order.append((gene_name,gene_chr,gene_start,gene_end,gene_sign))
    gene_order.sort(key=itemgetter(1,2))
    return gene_order

''' 
Rename an object (species, family, gene) to replace all non alphanumeric characters 
by sep
'''
def data_rename_object(name, sep=''):
    return sep.join(filter(str.isalnum, name))

# Data checking functions

''' Check if an object name is only alphanumeric '''
def data_check_object_name(name):
    '''
    input: name (str)
    output: boolean
    '''
    return (name.isalnum())

''' Check if a gene name is of the format gene<SEP>species '''
def data_check_gene_name(name, species_list, sep):
    '''
    input: name (str), species list, separator character
    output: boolean
    assumption: species names are correct
    '''
    name_split = name.split(sep)
    check_format = (len(name_split) == 2)
    check_name = data_check_object_name(name_split[1])
    check_species = name_split[0] in species_list
    return (check_format and check_name and check_species)

''' Check for gene inclusion '''
def data_check_gene_inclusion(gene_order):
    '''
    input: sorted list of genes (name,chr,start,end,sign)
    output: list (gene1,gene2) where gene2 is included in gene1
    '''
    inclusions = []
    prev_gene,prev_chr,prev_end = None,'',-1
    for (gene_name,gene_chr,gene_start,gene_end,_) in gene_order:
        if prev_gene is not None and prev_chr==gene_chr and gene_end<=prev_end:
            inclusions.append((prev_gene,gene_name))
        else:
            prev_gene,prev_chr,prev_end = gene_name,gene_chr,gene_end
    return inclusions

''' Check species tree '''
def data_check_species_tree(species_tree_file):
    '''
    input: path to species tree file
    assumption: Newick format file
    output: boolean,False:error message/True:species list
    '''
    if not newick_check_rooted(species_tree_file):
        return 1,'Unrooted species tree'
    if not newick_check_internal_names(species_tree_file):
        return 2,'Unlabeled ancestral species'
    species_list = newick_get_species(species_tree_file, extant=True)
    species_errors = [s for s in species_list if not data_check_object_name(s)]
    if len(species_errors) > 0:
        return 3,species_errors
    else:
        return 0,species_list

''' Check families file '''
def data_check_families(in_families_file, species_list, sep):
    '''
    input: path to families file, species list, separator character
    output: boolean,False:family errors/True:map family to genes,False:genes errors/True:map gene to family
    '''
    g2f_map = data_gene2family(in_families_file)
    f2g_map = data_family2genes(in_families_file)
    families_errors = [f for f in f2g_map.keys() if not data_check_object_name(f)]
    genes_errors = [g for g in g2f_map.keys() if not data_check_gene_name(g,species_list,sep)]
    if len(families_errors)>0:
        return 1,families_errors
    elif len(genes_errors)>0:
        return 2,genes_errors
    else:
        return 0,[f2g_map,g2f_map]

def _data_compare_lists(list1,list2):
    errors1 = [x for x in list1 if x not in list2]
    errors2 = [x for x in list2 if x not in list1]
    if len(errors1)+len(errors2) > 0:
        return False,[errors1,errors2]
    else:
        return True,[]

''' Check gene orders files '''
def data_check_gene_orders_file(in_gene_orders_file, species_list, genes_list):
    '''
    input: path to gene orders file, list of species in species tree,list of gene names present in families
    output: 
    - no error:        0,[]
    - species errors:  1,[list of species in gene orders file not in species tree,list of species in species tree not in gene orders file]
    - gene inclusions: 2,list of genes inclusions (gene1,gene2)
    - genes errors:    3,[list of genes in gene orders files not in genes list,list of genes in genes list not in gene orders files]
    '''
    species2gene_order_path = data_species2gene_order_path(in_gene_orders_file)
    go_species_list = species2gene_order_path.keys()
    # Checking species lists
    species_check,species_errors = _data_compare_lists(go_species_list,species_list)
    if not species_check:
        return 1,species_errors
    # Checking gene inclusions
    species2genes_order,genes_inclusions = {},[]
    for species in species_list:
        species2genes_order[species] = data_read_gene_order_file(species2gene_order_path[species])
        genes_inclusions += data_check_gene_inclusion(species2genes_order[species])
    if len(genes_inclusions) > 0:
        return 2,genes_inclusions
    # Checking genes lists
    go_genes_list = [g[0]  for s in species_list for g in species2genes_order[s]]
    genes_check,genes_errors = _data_compare_lists(go_genes_list,genes_list)
    if not species_check:
        return 3,genes_errors
    # No error
    return 0,[]

''' Generic function to check a file indexed by families is correct '''
def _data_check_family_indexed_file(in_file, family2genes_map, genes2family_map, get_names):
    '''
    input: path to family indexed file, family2genes map, genes2family map, name getting function
    output:
    - no error: 0,[]
    - error:    1,[list of families with no object file,list of object files with no family]
    - error:    2,[list of genes in families not in objects,list of genes in objects not in families]
    '''
    family2objects_file = _data_create_map(in_file)
    # Checking families
    families_check,families_errors = _data_compare_lists(family2genes_map.keys(),family2objects_file.keys())
    if not families_check:
        return 1,families_errors
    # Checking genes names
    genes_names = [
        g for family in family2objects_file.keys() for g in get_names(family2objects_file[family]) 
    ]
    genes_check,genes_errors = _data_compare_lists(genes2family_map.keys(),genes_names)
    if not genes_check:
        return 2,genes_errors
    # No error
    return 0,[]
    
''' Check sequences files '''
def data_check_sequences_file(in_sequences_file, family2genes_map, genes2family_map):
    '''
    input: path to sequences file, family2genes map, genes2family map
    output:
    - no error: 0,[]
    - error:    1,[list of families with no sequence file,list of sequence file with no family]
    - error:    2,[list of genes in families not in sequences,list of genes in sequences not in families]
    '''
    return _data_check_family_indexed_file(in_sequences_file, family2genes_map, genes2family_map, fasta_get_names)

''' Check alignments file '''
def data_check_alignments_file(in_alignments_file, family2genes_map, genes2family_map):
    '''
    input: path to alignments file, family2genes map, genes2family map
    output:
    - no error: 0,[]
    - error:    1,[list of families with no alignment file,list of alignment file with no family]
    - error:    2,[list of genes in families not in alignments,list of genes in alignments not in families]
    '''
    return _data_check_family_indexed_file(in_alignments_file, family2genes_map, genes2family_map, fasta_get_names)

''' Check gene tree(s) file '''
def data_check_gene_trees_file(in_gene_trees_file, family2genes_map, genes2family_map):
    '''
    input: path to alignments file, family2genes map, genes2family map
    output:
    - no error: 0,[]
    - error:    1,[list of families with no gene trees file,list of gene trees file with no family]
    - error:    2,[list of genes in families not in gene trees,list of genes in gene trees not in families]
    '''
    return _data_check_family_indexed_file(in_gene_trees_file, family2genes_map, genes2family_map, newick_get_gene_trees_leaves)

''' Main: testing '''
def main():
    species_tree = sys.argv[1]
    families = sys.argv[2]
    gene_orders = sys.argv[3]
    data = sys.argv[4]
    data_type = sys.argv[5]

    check_st,species_out = data_check_species_tree(species_tree)
    if check_st != 0:
        print(f'ERROR\tspecies tree\t{check_st}\t{species_output}')
        exit(1)
    else:
        species_list = species_out
        print('SUCCESS\tspecies tree')

    check_fam,fam_out = data_check_families(families, species_list, '|')
    if check_fam == 1:        
        print(f'ERROR\tfamilies file\tfamilies names\t{fam_out}')
        exit(1)
    elif check_fam == 2:
        print(f'ERROR\\tfamilies file\tgenes names\t{fam_out}')
        exit(1)
    else:
        f2g_map,g2f_map = fam_out[0],fam_out[1]
        genes_list = list(g2f_map.keys())
        print('SUCCESS\tfamilies file')
        
    check_go,go_out = data_check_gene_orders_file(gene_orders, species_list, genes_list)
    if check_go == 1:
        print(f'ERROR\t\gene orders\tspecies\n\t{go_out[0]}\n\t{go_out[1]}')
        exit(1)
    elif check_go == 2:
        print(f'ERROR\tgene orders\tgene_inclusions\n\t{go_out}')
        exit(1)
    elif check_go == 3:
        print(f'ERROR\t\gene orders\tgenes\n\t{go_out[0]}\n\t{go_out[1]}')
        exit(1)
    else:
        print('SUCCESS\tgene orders file')

    if data_type == 'seq':
        check_data,data_out = data_check_sequences_file(data, f2g_map, g2f_map)
    elif data_type == 'msa':
        check_data,data_out = data_check_alignments_file(data, f2g_map, g2f_map)
    elif data_type == 'gt':
        check_data,data_out = data_check_gene_trees_file(data, f2g_map, g2f_map)
    if check_data == 1:
        print(f'ERROR\t\{data_type}\tfamilies\n\t{data_out[0]}\n\t{data_out[1]}')
        exit(1)
    elif check_data == 2:
        print(f'ERROR\t\{data_type}\tgenes\n\t{data_out[0]}\n\t{data_out[1]}')
        exit(1)
    else:
        print(f'SUCCESS\t{data_type} file')

if __name__ == "__main__":
    main()
