#!/usr/bin/env python3
# coding: utf-8

""" Compute DeCoSTAR statistics or conflicts """

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
            adj_dicts[species][gene_name] = {'h': [], 't': []}
    with open(in_adjacencies_file, 'r') as in_species_adjacencies:
        for species_data in in_species_adjacencies.readlines():
            species,in_adjacencies_file = species_data.rstrip().split()
            with open(in_adjacencies_file, 'r') as in_adjacencies:
                for adj in in_adjacencies.readlines():
                    gene1,gene2,sign1,sign2,_,weight = adj.rstrip().split()
                    ext1,ext2 = decostar_sign2extremity[(sign1,sign2)]
                    adj_dicts[species][gene1][ext1].append([float(weight), gene2, ext2])
                    adj_dicts[species][gene2][ext2].append([float(weight), gene1, ext1])
    # Sorting weights for each gene extremity
    for species in species_list:
        for gene in adj_dicts[species].keys():
            adj_dicts[species][gene]['h'].sort(key=lambda x: x[0])
            adj_dicts[species][gene]['t'].sort(key=lambda x: x[0])            
    return species_list,genes_lists,adj_dicts
    
stats_keys = ['genes', 'adj', 'conflict', 'free']

def decostar_compute_statistics(in_species_list, in_genes_lists, in_adj_dicts, in_thresholds):
    # Genes: number of genes per species
    # Adjacencies: number, number of genes in an adjacency, number conflicting, number free
    # for adjacencies of weight >= thresholds
    statistics = {}
    for species in in_species_list:
        statistics[species] = {}
        for threshold in in_thresholds:
            statistics[species]['genes'] = len(in_genes_lists[species])
            statistics[species][f'{threshold}'] = {k: 0 for k in stats_keys}
            for gene in in_adj_dicts[species].keys():
                # Number of adjacencies of weight >= threshold over both extremities
                nb_adj_h = len(list(filter(lambda k: k[0]>=threshold, in_adj_dicts[species][gene]['h'])))
                nb_adj_t = len(list(filter(lambda k: k[0]>=threshold, in_adj_dicts[species][gene]['t'])))
                statistics[species][f'{threshold}']['adj'] += (nb_adj_h + nb_adj_t)/2
                if nb_adj_h == 0: statistics[species][f'{threshold}']['free'] += 1
                if nb_adj_t == 0: statistics[species][f'{threshold}']['free'] += 1
                if nb_adj_h > 1: statistics[species][f'{threshold}']['conflict'] += 1
                if nb_adj_t > 1: statistics[species][f'{threshold}']['conflict'] += 1
                if nb_adj_h + nb_adj_t >= 1: statistics[species][f'{threshold}']['genes'] += 1
    return statistics

def decostar_write_conflicts(in_species_list, in_adj_dicts, in_threshold, out_conflicts_file):
    # Filtering adjacencies with a weight below in_threshold
    for species in in_species_list:
        for gene in in_adj_dicts[species].keys():
            adj_h = in_adj_dicts[species][gene]['h']
            adj_t = in_adj_dicts[species][gene]['t']
            in_adj_dicts[species][gene]['h'] = list(filter(lambda k: k[0]>=in_threshold, adj_h))
            in_adj_dicts[species][gene]['t'] = list(filter(lambda k: k[0]>=in_threshold, adj_t))
    # Writing conflicts adjacencies
    with open(out_conflicts_file, 'w') as out_conflicts:
        for species in in_species_list:
            for gene in in_adj_dicts[species].keys():
                for ext in ['h','t']:
                    adjacencies = in_adj_dicts[species][gene][ext]
                    if len(adjacencies) > 1:
                        conflicts = ' '.join([f'{c[1]}_{c[2]}.{c[0]}' for c in adjacencies])
                        out_conflicts.write(f'{species}\t{gene}_{ext}\t{conflicts}\n')
                

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
    out_file = sys.argv[6]

    species_list,genes_lists,adj_dicts = decostar_read_results(
        in_genes_file, in_adjacencies_file, in_species_tree_file, in_species_file
    )
    if len(in_thresholds) > 1: # Computing statistics
        statistics = decostar_compute_statistics(
            species_list, genes_lists, adj_dicts, in_thresholds
        )
        decostar_write_statistics(statistics, in_thresholds, out_file)
    else: # Computing conflicts
       decostar_write_conflicts(species_list, adj_dicts, in_thresholds[0], out_file) 
    
if __name__ == "__main__":
    main()

