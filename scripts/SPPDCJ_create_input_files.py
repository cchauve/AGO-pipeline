#!/usr/bin/env python3
# coding: utf-8

""" Create SPP-DCJ input files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.5"
__status__    = "Released"

import sys
import ete3
from os.path import basename
import pandas as pd
import numpy as np

from data_utils import data_index2path
from newick_utils import (
    newick_get_children_map,
    newick_get_lca_species
)
from DeCoSTAR_reformat import (
    decostar_read_adjacencies,
    decostar_sep
)
from DeCoSTAR_statistics import decostar_sign2extremity

from recPhyloXML_statistics import xml_read_events


TEL_START_ID = 1_000_000

''' Creates SPP-DCJ species tree file '''
def sppdcj_species_trees(
        in_species_tree,
        out_species_tree,
        species_list=None
):
    '''
    input:
    - path to a Newick tree file with internal nodes named
    - path to output SPP-DCJ species tree file
    - list of species to consider (None means all)
    output: out_species_tree
    '''
    children_map = newick_get_children_map(in_species_tree)
    with open(out_species_tree, 'w') as out_tree:
        for species,children in children_map.items():
            if species_list is None or species in species_list:
                out_tree.write(f'{species}\t{children[0]}\n')
                out_tree.write(f'{species}\t{children[1]}\n')

''' Creates the SPP-DCJ adjacencies file '''
def sppdcj_adjacencies(
        in_adjacencies_file,
        in_weight_threshold,
        gene_content,
        out_adjacencies_file,
        species_list=None):
    '''
    input:
    - dataset file with paths to DeCoSTAR adjacencies file
    - gene content table
    - minimum weight threshold to keep adjacencies
    - path to output SPP-DCJ adjacencies file
    - list of species to consider (None means all)
    output: out_adjacencies_file
    '''

    tel_id = TEL_START_ID
    sppdcj_sep = '\t'
    def split_gene(gene):
        gene_split = gene.split(decostar_sep)
        return gene_split[0],decostar_sep.join(gene_split[1:])

    species2adjacencies_file = [
        (species,adj_path)
        for (species,adj_path) in data_index2path(
                in_adjacencies_file
        ).items()
        if (species_list is None or species in species_list)
    ]
    with open(out_adjacencies_file, 'w') as out_adjacencies:
        header_str = [
            "#Species","Gene_1","Ext_1",
            "Gene_2","Ext_2", "Weight"
        ]
        out_adjacencies.write(f'{sppdcj_sep.join(header_str)}')

        for species,in_adjacencies_path in species2adjacencies_file:
            in_adjacencies = [
                adj
                for adj in decostar_read_adjacencies(
                        in_adjacencies_path, species=species
                )
                if float(adj[6]) >= in_weight_threshold
            ]
            gene_content_actual = set()
            for (sp,g1,g2,sign1,sign2,w1,w2) in in_adjacencies:
                exts = decostar_sign2extremity[(sign1,sign2)]
                fam1,gene1 = split_gene(g1)
                fam2,gene2 = split_gene(g2)
                gene_content_actual.add((fam1, gene1))
                gene_content_actual.add((fam2, gene2))
                adj_str = [
                    sp,f'{fam1}_{gene1}',exts[0],
                    f'{fam2}_{gene2}',exts[1], w2
                ]
                out_adjacencies.write(
                    f'\n{sppdcj_sep.join(adj_str)}'
                )

            # add single-gene CARS for each missing gene (i.e., gene
            # that is not part of an adjacency in DeCoSTAR output)
            df = pd.DataFrame(data = gene_content_actual,
                              columns=['family', 'actual_gc'])
            df = df.groupby(['family']).count()
            for i, gc in gene_content.loc[gene_content[species] > 0,
                                          species].items():
                n = i not in df.index and gc or gc - df.loc[i, 'actual_gc']
                for x in range(n):
                    out_adjacencies.write('\n' + sppdcj_sep.join(
                        (sp,f'{i}_{x}', 't', f't_{tel_id}', 'o',
                         '0')))
                    tel_id += 1
                    out_adjacencies.write('\n' + sppdcj_sep.join(
                        (sp,f'{i}_{x}', 'h', f't_{tel_id}', 'o',
                         '0')))
                    tel_id += 1


def get_gene_content(in_reconciliations_file, species_list=None):
    ''' reads in file with list of reconciled gene trees, then loads
    the trees and infers the number of copies for each specie of the
    given list'''

    df = pd.read_csv(open(in_reconciliations_file), header=None,
                     names=['family', 'tree_file_path'], sep='\t')
    df.set_index(['family'], inplace=True)
    if species_list is not None:
        df[species_list] = 0

    for i, row in df.iterrows():
        events = xml_read_events(row.tree_file_path)
        for s, vals in events.items():
            if species_list is None or s in species_list:
                if s not in df.columns:
                    df[s] = 0
                df.loc[i, s] = vals['genes']

    df.drop(columns=['tree_file_path'], inplace=True)
    return df


def main():
    in_adjacencies_file = sys.argv[1]
    in_reconciliations_file = sys.argv[2]
    in_species_tree = sys.argv[3]
    in_extant_species = sys.argv[4]
    in_weight_threshold = float(sys.argv[5])
    out_species_tree = sys.argv[6]
    out_adjacencies_file = sys.argv[7]

    # Define species to consider
    if in_extant_species == 'all':# Consider all species
        species_list = None
    else:# Consider species covered by the LCA of in_extant_species
        species_list = newick_get_lca_species(
            in_species_tree, in_extant_species.split()
        )

    gene_content = get_gene_content(in_reconciliations_file,
                                    species_list)

    # Creates an SPP-DCJ species tree
    sppdcj_species_trees(
        in_species_tree,
        out_species_tree,
        species_list=species_list
    )
    # Creates an SPP-DCJ adjacencies file
    sppdcj_adjacencies(
        in_adjacencies_file, in_weight_threshold,
        gene_content,
        out_adjacencies_file,
        species_list=species_list
    )

if __name__ == "__main__":
    main()
