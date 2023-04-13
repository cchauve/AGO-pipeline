#!/usr/bin/env python3
# coding: utf-8

""" Create FASTA format gene orders from DeCoSTAR format adjacencies """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

import os
import sys
from collections import defaultdict
import networkx as nx

from data_utils import data_species2adjacencies_path
from DeCoSTAR_reformat import decostar_sep
from DeCoSTAR_statistics import decostar_sign2extremity

''' Read DeCoSTAR genes for all species '''
def read_DeCoSTAR_genes(in_genes_file):
    '''
    input: DeCoSTAR genes file, for all species
    output: dict(species -> list of genes in format family<decostar_sep>gene)
    '''
    genes_dict = defaultdict(list)
    with open(in_genes_file,'r') as in_file:
        for gene in in_file.readlines():
            gene_data = gene.rstrip().split()
            species,gene_name = gene_data[0],gene_data[1]
            genes_dict[species].append(gene_name)
    return genes_dict

''' Read adjacencies for a given species '''
def read_DeCoSTAR_adjacencies_species(in_adjacencies_file):
    '''
    input: DeCoSTAR adjacencies file, for one species
    output: list((gene1,sign1,gene2,sign2,weight))
    '''
    adjacencies_list = []
    with open(in_adjacencies_file,'r') as in_file:
        for adjacency in in_file.readlines():
            adjacency_data = adjacency.rstrip().split()
            gene1,sign1 = adjacency_data[0],adjacency_data[1]
            gene2,sign2 = adjacency_data[2],adjacency_data[3]
            weight = adjacency_data[5]
            adjacencies_list.append((gene1,sign1,gene2,sign2,weight))
    return adjacencies_list

''' Read adjacencies for all species '''
def read_DeCoSTAR_adjacencies(in_adjacencies_file):
    '''
    input: adjacencies file
    output: dict(species -> list((gene1,sign1,gene2,sign2,weight)))
    '''
    adjacencies_dict = {}
    species2adjacencies_file = data_species2adjacencies_path(in_adjacencies_file)
    for species,adjacencies_file_path in species2adjacencies_file.items():
        adjacencies_dict[species] = read_DeCoSTAR_adjacencies_species(adjacencies_file_path)
    return adjacencies_dict

''' Create a graph from genes and adjacencies '''
def create_adjacencies_graph(in_genes_list, in_adjacencies):
    '''
    input:
    - dict(species -> list of genes list(family<decostar_sep>gene))
    - dict(species -> list of adjacencies list((gene_1,sign_1,gene_2,sign_2,weight)))
    output: networkx graph
    '''
    graphs = {}
    for species,in_adjacencies_list in in_adjacencies.items():
        graphs[species] = nx.Graph()
        for gene in in_genes_list[species]:
            graphs[species].add_node((gene,'h'))
            graphs[species].add_node((gene,'t'))
            graphs[species].add_edge((gene,'h'),(gene,'t'),weight=0)
        for (gene1,sign1,gene2,sign2,weight) in in_adjacencies_list:
            exts = decostar_sign2extremity[(sign1,sign2)]
            graphs[species].add_edge((gene1,exts[0]),(gene2,exts[1]), weight=weight)
    return graphs

''' Graph to FASTA string '''

def check_linear(C):
    ''' Check if a component is linear '''
    return C.number_of_nodes() == C.number_of_edges()+1

def get_start_node(C):
    ''' Return the first node for a traversal of a component '''
    nodes = list(C.nodes)
    if check_linear(C):
        return [x for x in nodes if C.degree(x)==1][0]
    else:
        return nodes[0]

def signed_gene(edge):
    if edge[0][1] == 't':
        return f'{edge[0][0]}'
    else:
        return f'-{edge[0][0]}'
    
def traversal2FASTA(C, start_node, species, C_id):
    ''' DFS traversal of a component '''
    edges_list = list(nx.dfs_edges(C, source=start_node))
    nodes_list = [signed_gene(edge).replace(f'{species}|','') for edge in edges_list if edge[0][0]==edge[1][0]]
    nodes_str = ' '.join(nodes_list)
    C_str = f'>{C_id}\n{nodes_str}\n'
    return C_str
    
    

def graph2FASTA(in_graph, species):
    '''
    input: graph, specis
    output: FASTA str
    '''
    components = list(nx.connected_components(in_graph))
    component_id = 1
    FASTA_str = ''
    for component in components:
        subgraph = nx.induced_subgraph(in_graph, component)
        start_node = get_start_node(subgraph)
        FASTA_str += traversal2FASTA(subgraph, start_node, species, component_id)
        component_id += 1
    return FASTA_str

''' Read graphs components '''
def read_adjacencies_graph(in_graph):
    print(list(nx.connected_components(in_graph)))

def main():
    in_genes_file = sys.argv[1]
    in_data_adjacencies_file = sys.argv[2]
    out_dir = sys.argv[3]
    out_data_gene_orders_file = sys.argv[4]    
    # Reading genes
    genes = read_DeCoSTAR_genes(in_genes_file)
    # Reading DeCoSTAR adjacencies
    adjacencies = read_DeCoSTAR_adjacencies(in_data_adjacencies_file)
    # Create graphs
    graphs = create_adjacencies_graph(genes, adjacencies)
    # Read graphs
    with open(out_data_gene_orders_file,'w') as out_data_file:
        for species,graph in graphs.items():
            species_str = graph2FASTA(graph,species)
            species_out_file = os.path.join(out_dir,f'{species}_gene_order.txt')
            out_data_file.write(f'{species}\t{species_out_file}\n')
            with open(species_out_file,'w') as out_file:
                out_file.write(species_str)

if __name__ == "__main__":
    main()
