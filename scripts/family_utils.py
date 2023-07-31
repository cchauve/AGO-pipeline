#!/usr/bin/env python3
# coding: utf-8

""" Manipulation of gene families """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Development"

import sys
from collections import defaultdict
import networkx as nx

''' Reading a gene families file '''
def family_read(family_file, gene_list=None):
    '''
    input: 
    - path to a gene families file
    - list of genes or None
    output:
    - dictionary fam_id -> list gene_id
    - dictionary gene_id -> fam_id
    If genes_list is not None, the families are filtered to keep only genes in the list
    '''
    fam2genes,gene2fam = {}, {}
    with open(family_file) as in_file:
        for fam_data in in_file.readlines():
            fam_split = fam_data.rstrip().split('\t')
            fam_id = fam_split[0]
            fam_genes = [
                x
                for x in fam_split[1].split()
                if (gene_list is None) or (x in gene_list)
            ]
            if len(fam_genes) > 0:
                fam2genes[fam_id] = fam_genes
                for gene_id in fam_genes: gene2fam[gene_id] = fam_id    
    return fam2genes,gene2fam

''' Distribution of size of gene families '''
def family_size_distribution(fam2genes):
    '''
    Computes the size distribution of gene families
    input: dictionary fam_id -> list gene_id
    output: dictionary fam_size -> number of families
    '''
    dist_size = defaultdict(int)
    for fam_id,gene_list in fam2genes.items():
        dist_size[len(gene_list)] += 1
    return dist_size

def family_size_distribution2str(dist_size):
    max_size = max(dist_size.keys())
    return ' '.join([
        f'{size}:{dist_size[size]}'
        for size in range(1,max_size+1)
        if dist_size[size] > 0
    ])

''' Measuring agreement between two sets of families '''
def family_combine_graph(gene2fam1, gene2fam2, fam2genes1, fam2genes2):
    genes2fam = defaultdict(list)
    for gene_id,fam_id in gene2fam1.items(): genes2fam[gene_id].append(f'{fam_id}_0')
    for gene_id,fam_id in gene2fam2.items(): genes2fam[gene_id].append(f'{fam_id}_1')
    G = nx.Graph()
    for fam_id,genes_list in fam2genes1.items(): G.add_node(f'{fam_id}_0', bipartite=0, size=len(genes_list))
    for fam_id,genes_list in fam2genes2.items(): G.add_node(f'{fam_id}_1', bipartite=1, size=len(genes_list))
    edges = [x for x in genes2fam.values() if len(x)==2]
    G.add_edges_from(edges)
    return G

def _component_type(G, C):
    GC = G.subgraph(C).copy()
    nb_fam = {0:0, 1:0}
    size1 = sum([x[1]['size'] for x in GC.nodes(data=True) if x[1]['bipartite'] == 0])
    size2 = sum([x[1]['size'] for x in GC.nodes(data=True) if x[1]['bipartite'] == 1])    
    for fam_id in GC.nodes(data=True): nb_fam[fam_id[1]['bipartite']] += 1
    if nb_fam[0]==1 and nb_fam[1]==0: return size1,size2,'o2z'
    elif nb_fam[0]==0 and nb_fam[1]==1: return size1,size2,'z2o'
    elif nb_fam[0]==1 and nb_fam[1]==1: return size1,size2,'o2o'
    elif nb_fam[0]==1 and nb_fam[1]>1: return size1,size2,'o2m'
    elif nb_fam[0]>1 and nb_fam[1]==1: return size1,size2,'m2o'
    else: return size1,size2,'m2m'
    

def cmd_compare(fam2genes1, fam2genes2, gene2fam1, gene2fam2):
    dist_size1 = family_size_distribution(fam2genes1)
    dist_size2 = family_size_distribution(fam2genes2)
    print(f'Size distribution 1:\t{family_size_distribution2str(dist_size1)}')
    print(f'Size distribution 1:\t{family_size_distribution2str(dist_size2)}')
    
    G = family_combine_graph(gene2fam1,gene2fam2,fam2genes1,fam2genes2)
    GCC = nx.connected_components(G)
    comp_type_nb = defaultdict(int)
    comp_type_size1 = defaultdict(int)
    comp_type_size2 = defaultdict(int)    
    for C in GCC:
        size1,size2,comp_type = _component_type(G, C)
        comp_type_nb[comp_type] += 1
        comp_type_size1[comp_type] += size1
        comp_type_size2[comp_type] += size2
    comp_type_str = ' '.join([
        f'{x}:{comp_type_nb[x]}:{comp_type_size1[x]}:{comp_type_size2[x]}'
        for x in ['o2o', 'z2o', 'o2z', 'o2m', 'm2o', 'm2m']
    ])
    print(f'Component types:\t{comp_type_str}')

    
def main():
    command = sys.argv[1]
    
    if command == 'compare':
        family_file1 = sys.argv[2]
        family_file2 = sys.argv[3]
        filter_family1 = sys.argv[4]
        # Assumption: if filter_family== '1', family_file1 genes include all genes of family_file2
        fam2genes2,gene2fam2 = family_read(family_file2)
        if filter_family1 == '1':
            gene_list2 = list(gene2fam2.keys())
            fam2genes1,gene2fam1 = family_read(family_file1, gene_list=gene_list2)
        else:
            fam2genes1,gene2fam1 = family_read(family_file1)
        cmd_compare(fam2genes1, fam2genes2, gene2fam1, gene2fam2)


if __name__ == "__main__":
    main()
