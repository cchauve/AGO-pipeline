#!/usr/bin/env python3

# import from built-in packages
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as ADHF, \
        FileType
from sys import stdout, stderr, exit
from collections import defaultdict
from itertools import combinations
from math import comb
from functools import reduce
from os.path import basename, dirname, join
import logging
import csv

# import from third-party packages
import pandas as pd
import numpy as np
import ete3

# import from own packages


#
# global variables
#

ORIENT_FORWARD = 1
ORIENT_REVERSE = 0

EXTR_HEAD = 'h'
EXTR_TAIL = 't'
EXTR_CAP  = 'o'

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

def readCounts(filename):
    header_start = 0
    with open(filename) as f:
        for line in f:
            if line.startswith('#|'):
                header_start += 1
            else:
                break
    return pd.read_csv(filename, sep='\t', index_col=0, header=[header_start], low_memory=False)


def readGF(data):
    _df = pd.read_csv(data, sep='\t', header=None, index_col=0, names=['Members'])
    _df['Count'] = _df.Members.map(lambda x: len(x.split()))
    df = pd.DataFrame(data = {'Family': reduce(lambda a, b: a + b, map(lambda x: [x[0]] * x[1]['Count'], _df.iterrows())),
                                 'Genome_gene': reduce(lambda a, b: a+b, _df.Members.map(lambda x: x.split()))
                                 })
    df['Genome'] = df.Genome_gene.map(lambda x: x.split('|', 1)[0])
    # intentially programmed to fail in case | is not part of string...
    df['Gene'] = df.Genome_gene.map(lambda x: x.split('|', 1)[1])
    del df['Genome_gene']
    df.sort_values(['Genome', 'Gene'], inplace=True)
    df.set_index(['Genome', 'Gene'], inplace=True)

    return df


def readGO(data, path_prefix):
    df = pd.DataFrame({
        'Genome_gene': pd.Series(dtype=str),
        'Orientation': pd.Series(dtype=int),
        'Start': pd.Series(dtype=int),
        'End': pd.Series(dtype=int),
        'Chromosome': pd.Series(dtype=str),
        })
    for genome, f in csv.reader(data, delimiter='\t'):
        fname = join(path_prefix, f)
        LOG.info('++ parsing gene order of {} from {}'.format(genome, fname))
        df = pd.concat([df,
                           pd.read_csv(fname, sep='\t', header=None,
                                       names=['Genome_gene', 'Orientation', 'Start', 'End', '_unused_', 'Chromosome'])],
                          join='inner', ignore_index=True)

    df['Genome'] = df.Genome_gene.map(lambda x: x.split('|', 1)[0])
    # intentially programmed to fail in case | is not part of string...
    df['Gene'] = df.Genome_gene.map(lambda x: x.split('|', 1)[1])
    df.sort_values(['Genome', 'Chromosome', 'Start', 'End'], inplace=True)
    df.set_index(['Genome', 'Gene'], inplace=True)

    # remove columns that we no longer need
    del df['Genome_gene']
    del df['Start']
    del df['End']

    return df


def recruitAdjacencies(tree, df_go, name2node):
    """
    Assumes that genes in df_go are already ordered by their genomic position.

    This function performs a bottom-up swipe to construct a weighted adjacency set for each internal node of the given phylogeny. The result will be
    such that all internal nodes will have different adjacencies and weights depending on how many times the corresponding adjacency has been seen on
    any path through the corresponding node.

    """
    ids = pd.IndexSlice
    tc = 0
    df_up = pd.DataFrame({
        'Species': pd.Series(dtype=str),
        'Family_1': pd.Series(dtype=str),
        'Gene_1': pd.Series(dtype=str),
        'Ext_1': pd.Series(dtype=str),
        'Family_2': pd.Series(dtype=str),
        'Gene_2': pd.Series(dtype=str),
        'Ext_2': pd.Series(dtype=str),
        'Weight': pd.Series(dtype=int)
        })

    map_orient1 = {0: EXTR_TAIL, 1: EXTR_HEAD, 2: EXTR_CAP}
    map_orient2 = {0: EXTR_HEAD, 1: EXTR_TAIL, 2: EXTR_CAP}
    # bottom-up traversal
    for v in tree.traverse('postorder'):
        if v.is_leaf(): 
            df_go_v = df_go.loc[ids[v.name,:,:]].reset_index()
            # at this point, we assume that each extant chromosome is linear
            for chrom in df_go_v.Chromosome.unique():
                # the following code creates an "adjacency table" from df_go joining it with a copy of itself that is shifted by one; then telomeres
                # are added and the table is prepared so that columns match that of the resulting df table
                df_c = df_go_v.loc[df_go_v.Chromosome == chrom]
                df_c1 = df_c.shift(1) 
                df_c1.loc[0, ['Gene', 'Orientation', 'Family']] = [str(tc), 2, 't']
                tc += 1
                df_c12 = df_c1.join(df_c, lsuffix='_1', rsuffix='_2')
                df_c12['Ext_1'] = df_c12.Orientation_1.map(map_orient1.get)
                df_c12['Ext_2'] = df_c12.Orientation_2.map(map_orient2.get)
                last = df_c12.tail(1)
                cols = ['Gene_1', 'Family_1', 'Ext_1', 'Gene_2', 'Family_2', 'Ext_2']
                df_c12.loc[last.index.item() + 1, cols] = [last.Gene_2.item(), last.Family_2.item(), map_orient1[last.Orientation_2.item()], str(tc),
                                                           't', EXTR_CAP]
                tc += 1
                df_c12['Species'] = v.name
                df_c12['Weight'] = 1

                # make sure adjacencies are represented in canonical form 
                sel_unsrtd = list(map(lambda y: y[0] > y[1], zip(map(lambda x: tuple(x[1]), df_c12[['Family_1', 'Ext_1', 'Gene_1']].iterrows()),
                                      map(lambda x: tuple(x[1]), df_c12[['Family_2', 'Ext_2', 'Gene_2']].iterrows()))))
                df_tmp1 = df_c12.loc[sel_unsrtd, ['Family_1', 'Ext_1', 'Gene_1']]
                df_tmp1.columns = ['Family_2', 'Ext_2', 'Gene_2']
                df_tmp2 = df_c12.loc[sel_unsrtd, ['Family_2', 'Ext_2', 'Gene_2']]
                df_tmp2.columns = ['Family_1', 'Ext_1', 'Gene_1']
                df_c12.loc[sel_unsrtd, ['Family_1', 'Ext_1', 'Gene_1']] = df_tmp2
                df_c12.loc[sel_unsrtd, ['Family_2', 'Ext_2', 'Gene_2']] = df_tmp1
                df_up = pd.concat([df_up, df_c12], join='inner', ignore_index=True)

        else:
            # lists genes (not accounting for multiplicity yet) of ancestral genome 
            df_v = pd.DataFrame({
                'Family_1': pd.Series(dtype=str),
                'Ext_1': pd.Series(dtype=str),
                'Family_2': pd.Series(dtype=str),
                'Ext_2': pd.Series(dtype=str),
                'Weight': pd.Series(dtype=int)
                })

            for u in v.get_children():
                df_u = df_up.loc[df_up.Species==u.name, ['Family_1', 'Ext_1', 'Family_2', 'Ext_2', 'Weight']]
                # remove duplicates within extant genomes (ancestral genomes don't have duplicates--by construction)
                if u.is_leaf():
                    df_u.drop_duplicates(inplace=True)
                df_v = pd.concat([df_v, df_u], ignore_index=True)
            # merge duplicate adjacencies between children and sum up their weights
            df_v = df_v.groupby(['Family_1', 'Ext_1', 'Family_2', 'Ext_2'], group_keys=True).sum().reset_index()
            df_v['Species'] = v.name
            df_up = pd.concat([df_up, df_v], ignore_index=True)

    sel_up_leaf = df_up.Species.map(lambda x: name2node.get(x).is_leaf())

    # first merge non-leaf adjacencies and merge them
    df = df_up.loc[~sel_up_leaf].groupby(['Species', 'Family_1', 'Ext_1', 'Family_2', 'Ext_2'], group_keys=True).sum().reset_index()
    # adjust weights
    df_norm = pd.DataFrame(index=df.Species.unique(), data={'nleaves': pd.Index(df.Species.unique()).map(lambda x: len(name2node[x].get_leaves()))})
    df_norm['pathcombs'] = df_norm.nleaves.map(lambda x: comb(x, 2))
    df.Weight = df.index.map(lambda x: df.Weight.loc[x]/df_norm.pathcombs.loc[df.Species.loc[x]])

    df[['Gene_1', 'Gene_2']]= np.nan
    df = pd.concat([df, df_up.loc[sel_up_leaf]], ignore_index=True)

    return df

def instantiateGenes(df_adjs, df_counts):

    df = pd.DataFrame({
        'Species': pd.Series(dtype=str),
        'Family_1': pd.Series(dtype=str),
        'Gene_1': pd.Series(dtype=str),
        'Ext_1': pd.Series(dtype=str),
        'Family_2': pd.Series(dtype=str),
        'Gene_2': pd.Series(dtype=str),
        'Ext_2': pd.Series(dtype=str),
        'Weight': pd.Series(dtype=int)
        })

    for anc in df_counts.columns:
        df_genes = pd.DataFrame(data = {'Family': reduce(lambda a,b: a+b, map(lambda x: [x[0]] * x[1], df_counts[anc].items()))})
        df_genes.index.name = 'Gene'
        df_genes.reset_index(inplace=True)
        df_genes.Gene = df_genes.Gene.astype(str)

        df_anc = df_adjs.loc[df_adjs.Species==anc].set_index('Family_1').join(df_genes.set_index('Family'), how='inner').reset_index()
        df_anc = df_anc.set_index('Family_2').join(df_genes.set_index('Family'), how='inner', lsuffix='_1', rsuffix='_2').reset_index()
        df = pd.concat([df, df_anc], ignore_index=True)

    return df

if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=ADHF)
    parser.add_argument('tree', type=str,
            help='phylogenetic tree in newick format')
    parser.add_argument('gf_counts', type=open,
            help='gene family count table from Miklós Csűrös\' Count software')
    parser.add_argument('gene_families', type=open,
            help='gene-to-family assignment table')
    parser.add_argument('gene_orders', type=open,
            help='file pointing to gene order tables of extant species')
    args = parser.parse_args()

    # setup logging
    ch = logging.StreamHandler(stderr)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s'))
    LOG.addHandler(ch)

    # load & process input data
    LOG.info('loading species tree from {}'.format(args.tree))
    speciesTree = ete3.Tree(args.tree, format=1)

    LOG.info('loading gene family counts from {}'.format(args.gf_counts.name))
    df_counts = readCounts(args.gf_counts.name)
    LOG.info('loading gene family assignments from {}'.format(args.gene_families.name))
    df_gf = readGF(args.gene_families)

    LOG.info('loading extant gene orders from {}'.format(args.gene_orders.name))
    # read gene order table and join with df_gf table
    df_go = readGO(args.gene_orders, dirname(args.gene_orders.name)).join(df_gf)

    # let's do it!
    name2node = dict(map(lambda x: (x.name, x), speciesTree.traverse()))
    df_adjs = recruitAdjacencies(speciesTree, df_go, name2node)
    sel_leaf = df_adjs.Species.map(lambda x: name2node.get(x).is_leaf())
    df_adjs_leaves = df_adjs.loc[sel_leaf]
    df_adjs_anc = df_adjs.loc[~sel_leaf, ['Species', 'Family_1', 'Ext_1', 'Family_2', 'Ext_2', 'Weight']]
    df = pd.concat([instantiateGenes(df_adjs_anc, df_counts[df_adjs_anc.Species.unique()]), df_adjs_leaves], ignore_index=True)
    df.Gene_1 = df.apply(lambda x: '_'.join((x.Family_1, x.Gene_1)), axis=1)
    df.Gene_2 = df.apply(lambda x: '_'.join((x.Family_2, x.Gene_2)), axis=1)
    del df['Family_1']
    del df['Family_2']

    # output final adjacency set
    df.to_csv(stdout, sep='\t', index=False)

    LOG.info('DONE')

