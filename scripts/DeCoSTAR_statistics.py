#!/usr/bin/env python3
# coding: utf-8

""" Compute DeCoSTAR statistics or conflicts from reformatted DeCoSTAR results """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Released"

import sys

from data_utils import (
    data_species_list,
    data_index2path
)
from DeCoSTAR_reformat import decostar_read_adjacencies

decostar_sign2extremity = {
    ('-','+'): ['t','t'],('-','-'): ['t','h'],
    ('+','-'): ['h','h'],('+','+'): ['h','t']
}

# Recorded statistics
# key_genes: number of genes with at least one extremity in at least one adjacency
# key_adj: number of adjacencies
# key_conflict: number of gene extremities in a conflict
# key_free: number of gene extremities in no adjacencies
key_genes = 'genes_in_adj'
key_adj = 'adjacencies'
key_conflict = 'ext_in_conflict'
key_free = 'free_ext'
stats_keys = [key_genes, key_adj, key_conflict, key_free]
    
''' 
Reads genes and adjacencies 
Creates dict(species -> list of genes in species)
Creates dict(species -> gene1 -> ext1 -> list((weight, gene2, ext2)))
'''
def decostar_read_results(in_genes_file, in_adjacencies_file, in_species_list):
    '''
    input:
    - reformatted genes file
    - reformatted adjacencies file
    - list of extant and ancestral species file
    output:
    - dict(species -> list of genes in species)
    - dict(species -> gene1 -> ext1 -> (weight, gene2, ext2))
    '''
    # Reading reformatted genes file to create a dict(species -> list of genes)
    genes_lists = {sp: [] for sp in in_species_list}
    with open(in_genes_file, 'r') as in_genes:
        for gene_data in in_genes.readlines():
            species,gene = gene_data.rstrip().split()[0:2]
            genes_lists[species].append(gene)
    # Nested dict(species -> gene1 -> ext1 -> list((weight, gene2, ext2)))
    species_gene = [(s,g) for s in in_species_list for g in genes_lists[s]]
    ## Initialize dictionaries
    adjacencies_dicts = {s: {} for s in in_species_list}
    for (species,gene) in species_gene:
        adjacencies_dicts[species][gene] = {'h': [], 't': []}
    ## Populate dictionaries from species to adjacency tabulated file
    species2adjacencies = data_index2path(in_adjacencies_file)
    for species,in_adjacencies_file in species2adjacencies.items():
        in_adjacencies = decostar_read_adjacencies(
            in_adjacencies_file, species=species
        )
        for (sp,g1,g2,sign1,sign2,w1,w2) in in_adjacencies:
            ext1,ext2 = decostar_sign2extremity[(sign1,sign2)]
            fw2 = float(w2)
            adjacencies_dicts[sp][g1][ext1].append([fw2, g2, ext2])
            adjacencies_dicts[sp][g2][ext2].append([fw2, g1, ext1])
    # Sorting by increasing weight for each gene extremity
    for (species,gene) in species_gene:
        adjacencies_dicts[species][gene]['h'].sort(key=lambda x: x[0])
        adjacencies_dicts[species][gene]['t'].sort(key=lambda x: x[0])            
    return genes_lists,adjacencies_dicts
    
'''
Compute statistics per species for various weight thresholds
Creates for each species s and weight threshold w statistics are recorded
from adjacencies in s of weight >= w:
- 'genes': number of genes in adjacencies
- 'adj': number of adjacencies
- 'conflict': number of gene extremity in at least 2 adjacencies
- 'free': number of gene extrimity in no adjacency
Moreover for each species there key spcies -> 'genes': total number of genes 
in species
'''
def decostar_compute_statistics(
        in_species_list, in_genes_lists, in_adj_dicts, in_thresholds
):
    '''
    input:
    - species list
    - genes list and adjacencies dictionaries from function decostar_read_results
    - list of weight thresholds
    output:
    dict(species -> str(threshold) -> dictionary of statistics with keys stats_keys)
    '''
    statistics = {s: {} for s in in_species_list}
    species_thresholds = [
        (s,t) for s in in_species_list for t in in_thresholds
    ]
    for (species,threshold) in species_thresholds:
        statistics[species][key_genes] = len(in_genes_lists[species])
        statistics[species][f'{threshold}'] = {k: 0 for k in stats_keys}
        for gene in in_adj_dicts[species].keys():
            # Number of adjacencies of weight >= threshold over both extremities
            nb_adj_h = len(list(
                filter(lambda k: k[0]>=threshold, in_adj_dicts[species][gene]['h'])
            ))
            nb_adj_t = len(list(
                filter(lambda k: k[0]>=threshold, in_adj_dicts[species][gene]['t'])
            ))
            statistics[species][f'{threshold}'][key_adj] += (nb_adj_h + nb_adj_t)/2
            if nb_adj_h == 0:
                statistics[species][f'{threshold}'][key_free] += 1
            if nb_adj_t == 0:
                statistics[species][f'{threshold}'][key_free] += 1
            if nb_adj_h > 1:
                statistics[species][f'{threshold}'][key_conflict] += 1
            if nb_adj_t > 1:
                statistics[species][f'{threshold}'][key_conflict] += 1
            if nb_adj_h+nb_adj_t >= 1:
                statistics[species][f'{threshold}'][key_genes] += 1
    return statistics

''' Write conflicting adjacencies '''
def decostar_write_conflicts(
        in_species_list, in_adj_dicts, in_threshold,
        out_conflicts_file
):
    # Filtering adjacencies with a weight below in_threshold
    species_gene = [
        (s,g) for s in in_species_list for g in in_adj_dicts[s].keys()
    ]
    for (species,gene) in species_gene:
        adj_h = in_adj_dicts[species][gene]['h']
        adj_t = in_adj_dicts[species][gene]['t']
        in_adj_dicts[species][gene]['h'] = list(
            filter(lambda k: k[0]>=in_threshold, adj_h)
        )
        in_adj_dicts[species][gene]['t'] = list(
            filter(lambda k: k[0]>=in_threshold, adj_t)
        )
    # Writing conflicts adjacencies
    with open(out_conflicts_file, 'w') as out_conflicts:
        for (species,gene,ext) in [
                (s,g,e) for (s,g) in species_gene for e in ['h','t']
        ]:
            adjacencies = in_adj_dicts[species][gene][ext]
            if len(adjacencies) > 1:
                conflicts = ' '.join(
                    [f'{c[1]}_{c[2]}.{c[0]}' for c in adjacencies]
                )
                out_conflicts.write(
                    f'{species}\t{gene}_{ext}\t{conflicts}\n'
                )
                

''' Write statistics for a set of thresholds '''
def decostar_write_statistics(
        in_statistics, in_thresholds,
        out_statistics_file,
        out_sep=':'
):
    with open(out_statistics_file, 'w') as out_stats:
        header_pref = f'#species{out_sep}nb_{key_genes}:min_weight'
        header_stats = out_sep.join([f'nb_{k}' for k in stats_keys])
        header = f'{header_pref}\t{header_stats}'
        out_stats.write(header)    
        for species in in_statistics.keys():
            out_stats.write(f'\n#{species}')
            nb_genes = in_statistics[species][key_genes]
            for threshold in in_thresholds:
                stats = in_statistics[species][f'{threshold}']
                pref_str = f'\n{species}:{nb_genes}:{threshold}'
                stats_str = out_sep.join(
                    [str(int(stats[k])) for k in stats_keys]
                )                        
                out_stats.write(f'{pref_str}\t{stats_str}')
        out_stats.write('\n')

def main():
    in_species_file = sys.argv[1]
    in_genes_file = sys.argv[2]
    in_adjacencies_file = sys.argv[3]
    in_thresholds = [float(t) for t in sys.argv[4].split()]
    out_file = sys.argv[5]

    species_list = data_species_list(in_species_file)
    genes_lists,adj_dicts = decostar_read_results(
        in_genes_file, in_adjacencies_file, species_list
    )
    if len(in_thresholds) > 1:
        # Computing statistics for several weight thresholds
        statistics = decostar_compute_statistics(
            species_list, genes_lists, adj_dicts, in_thresholds
        )
        decostar_write_statistics(statistics, in_thresholds, out_file)
    else:
        # Computing conflicts for one weight threshold
       decostar_write_conflicts(
           species_list, adj_dicts, in_thresholds[0], out_file
       ) 
    
if __name__ == "__main__":
    main()

