#!/usr/bin/env python3
# coding: utf-8

""" Computes and writes statistics about adjacencies discarded by SPP_DCJ """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Released"

import sys
import os

from SPPDCJ_reformat import (
    sppdcj_read_sppdcj_adjacencies,
    sppdcj_read_decostar_adjacencies,
    sppdcj_filter_adjacencies
)

def sppdcj_statistics(decostar_adjacencies, filtered_adjacencies):
    statistics = {}
    for species,adjacencies in decostar_adjacencies.items():
        statistics[species] = {}
        nb_adj = len(adjacencies.keys())
        sum_weights = sum([float(adj[5]) for adj in adjacencies.values()])
        statistics[species]['nb1'] = nb_adj
        statistics[species]['weight1'] = sum_weights
    for species,adjacencies in filtered_adjacencies.items():
        nb_adj = len(adjacencies.keys())
        sum_weights = sum([float(adj[5]) for adj in adjacencies.values()])
        statistics[species]['nb2'] = nb_adj
        statistics[species]['weight2'] = sum_weights
    return statistics

def sppdcj_write_statistics(statistics, out_statistics_file):
    with open(out_statistics_file,'w') as out_file:
        out_file.write('#species\tnumber of adjacencies:total weight:kept adjacencies:kept weight')
        for species,stats in statistics.items():
            stats_str = ':'.join([str(round(stats[k],2)) for k in ['nb1','weight1','nb2','weight2']])
            out_file.write(f'\n{species}\t{stats_str}')
        out_file.write('\n')

def main():
    in_data_adjacencies_file = sys.argv[1]
    in_sppdcj_adjacencies_file = sys.argv[2]
    out_statistics_file = sys.argv[3]
    # Reading SPPDCJ adjacencies
    sppdcj_adjacencies = sppdcj_read_sppdcj_adjacencies(in_sppdcj_adjacencies_file)    
    # Reading DeCoSTAR adjacencies
    decostar_adjacencies = sppdcj_read_decostar_adjacencies(in_data_adjacencies_file)
    # Filter DeCoSTAR adjacencies
    filtered_adjacencies = sppdcj_filter_adjacencies(decostar_adjacencies,sppdcj_adjacencies)
    # Statistics
    statistics = sppdcj_statistics(decostar_adjacencies, filtered_adjacencies)
    sppdcj_write_statistics(statistics, out_statistics_file)

if __name__ == "__main__":
    main()
