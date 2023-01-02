#!/usr/bin/env python3
# coding: utf-8

""" Compute DeCoSTAR statistics """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
from DeCoSTAR_reformat import decostar_species_map


decostar_sign2extremity = {
    ('-','+'): ['t','t'],('-','-'): ['t','h'],
    ('+','-'): ['h','h'],('+','+'): ['h','t']
}


def decostar_read_results(in_genes_file, in_adjacencies_file, in_species_tree_file, in_species_file):
    species_list = [
        sp for sp in decostar_species_map(in_species_tree_file, in_species_file).values()
    ]
    genes_lists = {sp: [] for sp in species_list}
    adj_dicts = {sp: {} for sp in species_list}    
    with open(in_genes_file, 'r') as in_genes:
        for gene in in_genes.readlines():
            species,gene_name = gene.rstrip().split()[0:2]
            genes_lists[species].append(gene_name)
            adj_dicts[species][gene_name] = {'h': {'w': []}, 't': {'w': []}}
    with open(in_adjacencies_file, 'r') as in_adjacencies:
        for adj in in_adjacencies.readlines():
            species,gene1,gene2,sign1,sign2,_,weight = adj.rstrip().split()
            ext1,ext2 = decostar_sign2extremity[(sign1,sign2)]
            adj_dicts[species][gene1][ext1]['w'].append(float(weight))
            adj_dicts[species][gene2][ext2]['w'].append(float(weight))
    # Sorting weights for each gene extremity
    for species in species_list:
        for gene in adj_dicts[species].keys():
            adj_dicts[species][gene]['h']['w'].sort()
            adj_dicts[species][gene]['t']['w'].sort()            
    return species_list,genes_lists,adj_dicts
    
stats_keys = ['genes', 'adj', 'conflict', 'free']

def decostar_compute_statistics(in_species_list, in_genes_lists, in_adj_dicts, in_thresholds):
    # Genes: number of genes per species
    # Adjacencies: number, number of genes in ana djacency, number conflicting, number free
    # for adjacencies of weight >= thresholds
    statistics = {}
    for species in in_species_list:
        statistics[species] = {}
        for threshold in in_thresholds:
            statistics[species]['genes'] = len(in_genes_lists[species])
            statistics[species][f'{threshold}'] = {k: 0 for k in stats_keys}
            for gene in in_adj_dicts[species].keys():
                # Number of adjacencies of weight >= threshold over both extremities
                nb_adj_h = len(list(filter(lambda k: k>=threshold, in_adj_dicts[species][gene]['h']['w'])))
                nb_adj_t = len(list(filter(lambda k: k>=threshold, in_adj_dicts[species][gene]['t']['w'])))
                statistics[species][f'{threshold}']['adj'] += (nb_adj_h + nb_adj_t)/2
                if nb_adj_h == 0: statistics[species][f'{threshold}']['free'] += 1
                if nb_adj_t == 0: statistics[species][f'{threshold}']['free'] += 1
                if nb_adj_h > 1: statistics[species][f'{threshold}']['conflict'] += 1
                if nb_adj_t > 1: statistics[species][f'{threshold}']['conflict'] += 1
                if nb_adj_h + nb_adj_t >= 1: statistics[species][f'{threshold}']['genes'] += 1
    return statistics

def decostar_write_statistics(in_statistics, in_thresholds, out_statistics_file):
    with open(out_statistics_file, 'w') as out_stats:
        out_stats.write(f'#species:nb_genes:min_weight')        
        out_stats.write(f'\tnb_adjacencies:nb_genes_in_adjacencies:nb_extremities_in_conflict:nb_free_extremities')                        
        for species in in_statistics.keys():
            out_stats.write(f'\n#{species}')
            nb_genes = in_statistics[species]['genes']
            for threshold in in_thresholds:
                stats = in_statistics[species][f'{threshold}']
                header = f'\n{species}:{nb_genes}:{threshold}'
                stats_str = ':'.join([str(int(stats[k])) for k in stats_keys])                        
                out_stats.write(f'{header}\t{stats_str}')

def main():
    in_species_tree_file = sys.argv[1]
    in_species_file = sys.argv[2]
    in_genes_file = sys.argv[3]
    in_adjacencies_file = sys.argv[4]
    in_thresholds = [float(t) for t in sys.argv[5].split()]
    out_statistics_file = sys.argv[6]

    species_list,genes_lists,adj_dicts = decostar_read_results(
        in_genes_file, in_adjacencies_file, in_species_tree_file, in_species_file
    )
    statistics = decostar_compute_statistics(
        species_list, genes_lists, adj_dicts, in_thresholds
    )
    decostar_write_statistics(statistics, in_thresholds, out_statistics_file)
    
if __name__ == "__main__":
    main()

