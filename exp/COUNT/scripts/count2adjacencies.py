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

ids = pd.IndexSlice


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


def constructExtantAdjacenciesTable(df_go, tc=0):
    """ Constructs adjacency table from given gene order table. Continuous enumeration of telomeres is ensured by tc counter. """

    map_orient1 = {0: EXTR_TAIL, 1: EXTR_HEAD, 2: EXTR_CAP}
    map_orient2 = {0: EXTR_HEAD, 1: EXTR_TAIL, 2: EXTR_CAP}

    df = pd.DataFrame({
        'Family_1': pd.Series(dtype=str),
        'Gene_1': pd.Series(dtype=str),
        'Ext_1': pd.Series(dtype=str),
        'Family_2': pd.Series(dtype=str),
        'Gene_2': pd.Series(dtype=str),
        'Ext_2': pd.Series(dtype=str),
        })
    # at this point, we assume that each extant chromosome is linear
    for chrom in df_go.Chromosome.unique():
        # the following code creates an "adjacency table" from df_go joining it with a copy of itself that is shifted by one; then telomeres are
        # added and the table is prepared so that columns match that of the resulting df table
        df_c = df_go.loc[df_go.Chromosome == chrom]
        df_c1 = df_c.shift(1) 
        df_c1.loc[0, ['Gene', 'Orientation', 'Family']] = [str(tc), 2, 't']
        tc += 1
        df_c12 = df_c1.join(df_c, lsuffix='_1', rsuffix='_2')
        df_c12['Ext_1'] = df_c12.Orientation_1.map(map_orient1.get)
        df_c12['Ext_2'] = df_c12.Orientation_2.map(map_orient2.get)
        last = df_c12.tail(1)
        cols = ['Gene_1', 'Family_1', 'Ext_1', 'Gene_2', 'Family_2', 'Ext_2']
        df_c12.loc[last.index.item() + 1, cols] = [last.Gene_2.item(), last.Family_2.item(), map_orient1[last.Orientation_2.item()], str(tc), 't',
                                                   EXTR_CAP]
        tc += 1

        # make sure adjacencies are represented in canonical form 
        sel_unsrtd = list(map(lambda y: y[0] > y[1], zip(map(lambda x: tuple(x[1]), df_c12[['Family_1', 'Ext_1', 'Gene_1']].iterrows()),
                              map(lambda x: tuple(x[1]), df_c12[['Family_2', 'Ext_2', 'Gene_2']].iterrows()))))
        df_tmp1 = df_c12.loc[sel_unsrtd, ['Family_1', 'Ext_1', 'Gene_1']]
        df_tmp1.columns = ['Family_2', 'Ext_2', 'Gene_2']
        df_tmp2 = df_c12.loc[sel_unsrtd, ['Family_2', 'Ext_2', 'Gene_2']]
        df_tmp2.columns = ['Family_1', 'Ext_1', 'Gene_1']
        df_c12.loc[sel_unsrtd, ['Family_1', 'Ext_1', 'Gene_1']] = df_tmp2
        df_c12.loc[sel_unsrtd, ['Family_2', 'Ext_2', 'Gene_2']] = df_tmp1
        df = pd.concat([df , df_c12], join='inner', ignore_index=True)

    return df, tc


def constructExtantAdjacenciesTableAll(tree, df_go):
    tc = 0
    df = pd.DataFrame({
        'Species': pd.Series(dtype=str),
        'Family_1': pd.Series(dtype=str),
        'Gene_1': pd.Series(dtype=str),
        'Ext_1': pd.Series(dtype=str),
        'Family_2': pd.Series(dtype=str),
        'Gene_2': pd.Series(dtype=str),
        'Ext_2': pd.Series(dtype=str),
        })
    # construct table of all observed adjacencies in extant genomes
    for v in tree.get_leaves():
        df_v, tc = constructExtantAdjacenciesTable(df_go.loc[ids[v.name,:,:]].reset_index(), tc)
        df_v['Species'] = v.name
        df = pd.concat([df, df_v], ignore_index=True)
    # initialize weight of extant adjacencies with 1
    df['Weight'] = 1
    return df


def recruitAncestralAdjacencies(tree, df_extant, name2node):
    """
    Assumes that genes in df_go are already ordered by their genomic position.

    This function performs a bottom-up/top-down swipe to construct a weighted adjacency set for each internal node of the given phylogeny. The result
    will be such that all internal nodes will have the same adjacencies, but their counts will be different, depending on how many times the
    corresponding adjacency has been seen on any path through the corresponding node.

    Note that the code may sometimes look weird, because it works on general trees, but typically we expect the tree to be binary.
    """
    # ignore gene associations of extant genes for bottom-up traversal and ignore duplicate adjacencies
    df = df_extant[['Species', 'Family_1', 'Ext_1', 'Family_2', 'Ext_2', 'Weight']].drop_duplicates()

    # introduce temporary columns "UpCount" and "DownCount"
    df['UpCount'] = df['Weight']
    df['DownCount'] = 0

    #
    # initialize table for all ancestral genomes 
    #
    df_template = df[['Family_1', 'Ext_1', 'Family_2', 'Ext_2']].drop_duplicates().set_index(['Family_1', 'Ext_1', 'Family_2', 'Ext_2'])
    df_template['Weight'] = 0
    df_template['UpCount'] = 0
    df_template['DownCount'] = 0
    df.set_index(['Species', 'Family_1', 'Ext_1', 'Family_2', 'Ext_2'], inplace=True)
    for v in tree.traverse():
        df = pd.concat([df, pd.concat({v.name: df_template}, names=['Species'])])
    # we created some duplicates for leaves, so we have to drop those
    df = df[~df.index.duplicated(keep='first')]
    df.sort_index(inplace=True)

    #
    # bottom-up traversal
    #
    for v in tree.traverse('postorder'):
        for u, w in combinations(v.get_children(), 2):
            df_u = pd.concat({v.name: df.loc[ids[u.name,:, :, :, :]]}, names=['Species'])
            df_w = pd.concat({v.name: df.loc[ids[w.name,:, :, :, :]]}, names=['Species'])
            # set weight, which is the product of the children's counts
            # by construction, df_u and df_w have same index
            df.loc[ids[v.name, :, :, :], 'Weight'] += df_u.UpCount * df_w.UpCount

        # update count of v to the sum of the children's counts
        for u in v.get_children():
            df_u = pd.concat({v.name: df.loc[ids[u.name,:, :, :, :]]}, names=['Species'])
            df.loc[df_u.index, 'UpCount'] += df_u.UpCount
    #
    # top-down traversal
    # 
    for v in tree.traverse('preorder'):
        df.loc[ids[v.name, :, :, :], 'Weight'] += df.loc[ids[v.name, :, :, :], 'UpCount'] * df.loc[ids[v.name, :, :, :], 'DownCount']
        # update count for siblings
        df_children = df.loc[ids[[u.name for u in v.get_children()], :, :, :]].groupby(['Family_1', 'Ext_1', 'Family_2', 'Ext_2']).sum()
        for u in v.get_children():
            s = pd.concat({u.name: df_children.DownCount + df.loc[v.name, 'UpCount']}, names=['Species'])
            df.loc[ids[u.name, :, :, :], 'DownCount'] = s - df.loc[ids[u.name, :, :, :], 'UpCount']

    # we report *only* the weights of ancestral adjacencies
    return df.loc[ids[[x.name for x in tree.traverse() if not x.is_leaf()], :, :, :], ['Weight']].reset_index()


def countPaths(tree):
    """ reports the number of leaf-to-leaf path that go through each node of the tree """

    df = pd.DataFrame(index=map(lambda x: x.name, tree.traverse()), data=0, columns=['Paths', 'UpLeaves', 'DownLeaves'])

    # bottom-up traversal
    for v in tree.traverse('postorder'):
        if v.is_leaf():
            df.loc[v.name, 'UpLeaves'] = 1
        else:
            for u, w in combinations(v.get_children(), 2):
                df.loc[v.name, 'Paths'] += df.loc[[u.name, w.name], 'UpLeaves'].product()
            # update leaf counter
            df.loc[v.name, 'UpLeaves'] = df.loc[[u.name for u in v.get_children()], 'UpLeaves'].sum()

    # top-down traversal
    for v in tree.traverse('preorder'):
        df.loc[v.name, 'Paths'] += df.loc[v.name, 'UpLeaves'] * df.loc[v.name, 'DownLeaves']

        # update leaf count for children
        c = df.loc[[u.name for u in v.get_children()], 'UpLeaves'].sum()
        for u in v.get_children():
            df.loc[u.name, 'DownLeaves'] = df.loc[v.name, 'DownLeaves'] + c - df.loc[u.name, 'UpLeaves']

    return df[['Paths']]

def normalizeWeights(df_paths, df_adjs):
    """ normalizes ancestral adjacencies """

    for s in df_adjs['Species'].unique():
        df_adjs.loc[df_adjs.Species == s, 'Weight'] /= df_paths.loc[s, 'Paths']

    return df_adjs


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

    df_extant = constructExtantAdjacenciesTableAll(speciesTree, df_go)
    df_paths = countPaths(speciesTree)
    df_anc = normalizeWeights(df_paths, recruitAncestralAdjacencies(speciesTree, df_extant, name2node))

    # ignore ancestral adjacencies with 0 weight for now... (might come back to that at some point)
    df_anc = df_anc[df_anc.Weight > 0]
    # join extant and ancestral adjacency sets
    df = pd.concat([instantiateGenes(df_anc, df_counts[df_anc.Species.unique()]), df_extant], ignore_index=True)

    df.Gene_1 = df.apply(lambda x: '_'.join((x.Family_1, x.Gene_1)), axis=1)
    df.Gene_2 = df.apply(lambda x: '_'.join((x.Family_2, x.Gene_2)), axis=1)
    del df['Family_1']
    del df['Family_2']

    # output final adjacency set
    df.to_csv(stdout, sep='\t', index=False)

    LOG.info('DONE')

