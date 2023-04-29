#!/usr/bin/env python3
# coding: utf-8

""" Create FASTA format gene orders from DeCoSTAR format adjacencies and genes """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.3"
__status__    = "Released"

import os
import sys
from collections import defaultdict
import networkx as nx

from data_utils import data_index2path
from DeCoSTAR_reformat import decostar_sep
from DeCoSTAR_statistics import decostar_sign2extremity

""" Reading input data to create CARs: DeCoSTAR-format genes and adjacencies """

''' Read DeCoSTAR genes for all species '''
def go_read_decostar_genes(in_genes_file):
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
def go_read_decostar_adjacencies_species(in_adjacencies_file):
    '''
    input: DeCoSTAR adjacencies file, for one species
    output: list((gene1,sign1,gene2,sign2,weight))
    '''
    adjacencies_list = []
    with open(in_adjacencies_file,'r') as in_file:
        for adjacency in in_file.readlines():
            adjacency_data = adjacency.rstrip().split()
            gene1,sign1 = adjacency_data[0],adjacency_data[2]
            gene2,sign2 = adjacency_data[1],adjacency_data[3]
            weight = adjacency_data[5]
            adjacencies_list.append(
                (gene1,gene2,sign1,sign2,weight)
            )
    return adjacencies_list

''' Read adjacencies for all species '''
def go_read_decostar_adjacencies(in_adjacencies_file):
    '''
    input: adjacencies file
    output: dict(species -> list((gene1,sign1,gene2,sign2,weight)))
    '''
    adjacencies_dict = {}
    species2adjacencies_file = data_index2path(in_adjacencies_file)
    for species,adjacencies_file_path in species2adjacencies_file.items():
        adjacencies_dict[species] = go_read_decostar_adjacencies_species(
            adjacencies_file_path
        )
    return adjacencies_dict

""" Graph creation and manipulation """

''' 
Create graphs from genes and adjacencies, on per species
Vertices = gene extremities
Edges = adjacencies, each with a weight
'''
def go_create_adjacencies_graph(in_genes_list, in_adjacencies):
    '''
    input:
    - dict(species -> list of genes list(family<decostar_sep>gene))
    - dict(species -> list of adjacencies list((gene1,gene2,sign1,sign2,weight)))
    output: networkx graph
    '''
    graphs = {}
    for species,in_adjacencies_list in in_adjacencies.items():
        graphs[species] = nx.Graph()
        for gene in in_genes_list[species]:
            graphs[species].add_node((gene,'h'))
            graphs[species].add_node((gene,'t'))
            graphs[species].add_edge((gene,'h'),(gene,'t'),weight=0)
        for (gene1,gene2,sign1,sign2,weight) in in_adjacencies_list:
            exts = decostar_sign2extremity[(sign1,sign2)]
            graphs[species].add_edge(
                (gene1,exts[0]),(gene2,exts[1]),
                weight=weight
            )
    return graphs

def go_check_linear(C):
    ''' Check if a component C (networkx graph) is linear '''
    return C.number_of_nodes() == C.number_of_edges()+1

def go_get_start_node(C):
    ''' Return the first node for a traversal of a component C '''
    nodes = list(C.nodes)
    if go_check_linear(C):
        return [x for x in nodes if C.degree(x)==1][0]
    else:
        return nodes[0]

def go_signed_gene(edge):
    ''' 
    Add a "-" before a the gene defined by the first gene extremity 
    of an edge if this extremity is a tail 
    '''
    if edge[0][1] == 't':
        return f'{edge[0][0]}'
    else:
        return f'-{edge[0][0]}'


''' Graph to CARs in FASTA-like format '''
    
def go_component2str(C, start_node, species, C_id):
    ''' 
    DFS traversal of a component C (assumed to be linear or circular)
    given the first node for the traversal and the ID of the 
    component.
    species is needed to remove the gene name
    Creates a FASTA-like string describing the oriented gene order
    of the traversal
    '''
    edges_list = list(nx.dfs_edges(C, source=start_node))
    nodes_list = [
        go_signed_gene(edge).replace(f'{species}|','')
        for edge in edges_list
        if edge[0][0]==edge[1][0]
    ]
    nodes_str = ' '.join(nodes_list)
    C_str = f'>{C_id}\n{nodes_str}\n'
    return C_str
    
def go_graph2str(in_graph, species):
    '''
    input: graph, species
    output: string in FASTA-like format for all components of the graph
    '''
    components = list(nx.connected_components(in_graph))
    component_id = 1
    result = ''
    for component in components:
        C = nx.induced_subgraph(in_graph, component)
        start_node = go_get_start_node(C)
        result += go_component2str(
            C, start_node, species, component_id
        )
        component_id += 1
    return result

def go_write_CARs(in_graphs, out_dir, out_file_path):
    '''
    Write CARs
    '''
    with open(out_file_path,'w') as out_data_file:
        for species,graph in in_graphs.items():
            species_str = go_graph2str(graph,species)
            species_out_file = os.path.join(out_dir,f'{species}_CARs.txt')
            out_data_file.write(f'{species}\t{species_out_file}\n')
            with open(species_out_file,'w') as out_file:
                out_file.write(species_str)

''' Statistics about a graph '''

def go_graph2stats(in_graph):
    '''
    input: graph
    output:  dict(nb_nodes -> dict(nb_edges -> number of components))    
    '''
    components = list(nx.connected_components(in_graph))
    components_stats = defaultdict(lambda: defaultdict(int))
    for component in components:
        subgraph = nx.induced_subgraph(in_graph, component)
        nb_nodes = subgraph.number_of_nodes()
        nb_edges = subgraph.number_of_edges()
        nb_genes = int(nb_nodes / 2)
        nb_adjacencies = nb_edges - nb_genes
        components_stats[nb_genes][nb_adjacencies] += 1
    return components_stats

def go_write_stats(in_stats, out_file_path):
    '''
    input: dict(species -> dict(nb_nodes -> dict(nb_edges -> number of components)), stats file
    '''
    with open(out_file_path,'w') as out_stats_file:
        out_stats_file.write('#species\tnb_comp:nb_lin_comp:nb_circ_comp:list(nb_genes.nb_adj.nb_comp)')
        for species,sp_stats in in_stats.items():
            nb_comp = sum({x: sum(sp_stats[x].values()) for x in sp_stats.keys()}.values())
            nb_lin,nb_circ,list_stats = 0,0,[]
            nbg_keys = sorted(list(sp_stats.keys()),reverse=True)
            for nbg in nbg_keys:
                nba_keys = sorted(list(sp_stats[nbg].keys()),reverse=True)
                for nba in nba_keys:
                    nbc = sp_stats[nbg][nba]
                    if nba==nbg-1: nb_lin += nbc
                    elif nba==nbg: nb_circ += nbc
                    list_stats.append(f'{nbg}.{nba}.{nbc}')
            stats_str = f'\n{species}\t{nb_comp}:{nb_lin}:{nb_circ}:{",".join(list_stats)}'
            out_stats_file.write(stats_str)

        
def main():
    command = sys.argv[1]
    in_genes_file = sys.argv[2]
    in_data_adjacencies_file = sys.argv[3]
    out_dir = sys.argv[4]
    out_file = sys.argv[5]
    
    # Reading DeCoSTAR genes
    genes = go_read_decostar_genes(in_genes_file)
    # Reading DeCoSTAR adjacencies
    adjacencies = go_read_decostar_adjacencies(in_data_adjacencies_file)
    # Create graphs
    graphs = go_create_adjacencies_graph(genes, adjacencies)
    if command == 'build':
        # Read graphs and write CARs
        go_write_CARs(graphs, out_dir, out_file)
    elif command == 'stats':
        # Compute and write statistics
        species_stats = {}
        for species,graph in graphs.items():
            species_stats[species] = go_graph2stats(graphs[species])
        go_write_stats(species_stats, out_file)
            
if __name__ == "__main__":
    main()
