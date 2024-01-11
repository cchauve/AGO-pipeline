#!/usr/bin/env python3

from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter as ADHF
from sys import stdout, stderr, exit
from os.path import join, isfile, exists, isdir
import logging

#
# third party libraries
#
import pandas as pd
import networkx as nx

# logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def build_adj_graph(df, genes, species):
    '''
    Constructs a species-specific undirected NetworkX graph where marker
    extremities correspond to nodes and adjacencies to edges.

    Parameters
    ---------
    df : pd.DataFrame
        Input adjacencies table with columns
            #Species	Gene_1	Ext_1	Species	Gene_2	Ext_2	Weight

    Returns
    -------
    nx.Graph
        Graph where each component corresponds to a set of adjacencies
    '''


    G = nx.Graph()
    G.add_nodes_from(map(lambda x: (x, 'h'), genes))
    G.add_nodes_from(map(lambda x: (x, 't'), genes))
    G.add_edges_from(map(lambda x: ((x.Gene_1, x.Ext_1), (x.Gene_2, x.Ext_2)),
        df.loc[df.Species == species].itertuples()))
    return G


if __name__ == '__main__':

    description = '''
    Decomposes the adjacency set from the input file into components and
    outputs these into genome-specific tab-separated (TSV) files.
    '''
    parser = ArgumentParser(formatter_class=ADHF, description=description)
    parser.add_argument('adjacencies', type=open,
            help='Adjacencies file')
    parser.add_argument('log_file', type=FileType('w'),
            help='Log file')
    parser.add_argument('-c', '--contig', default=False, action='store_true', \
            help='Decompose into contigs, rather than components corresponding to conflicting adjacencies')
    parser.add_argument('-p', '--plots', default=False, action='store_true', \
            help='Draw summary plots on component statistics')
    parser.add_argument('-o', '--out_dir', default='.', \
            help='Path to output directory')

    args = parser.parse_args()

    # setup logging
    ch = logging.FileHandler(args.log_file.name, mode='w')
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s'))
    LOG.addHandler(ch)

    LOG.info(f'loading adjacency set from {args.adjacencies.name}')
    df = pd.read_csv(args.adjacencies, sep='\t',  header=0)
    df.columns = map(lambda x: x.title(), df.columns)
    df['Species'] = df['#Species']
    species = df.Species.unique()

    for s in species:
        LOG.info(f'building adjacency graph for {s}')
        genes = set(df.loc[(df.Species == s) & (df.Ext_1 != 'o')].Gene_1).union(df.loc[(df.Species == s) & (df.Ext_2 != 'o')].Gene_2)
        G = build_adj_graph(df, genes, s)

        if args.contig:
            f = join(args.out_dir, f'contig-components.{s}.tsv')
            LOG.info(f'writing contig components to {f}')
            G.add_edges_from(map(lambda x: ((x, 'h'), (x, 't')), genes))
            C = sorted(nx.components.connected_components(G), key=len, reverse=True)
            with open(f, 'w') as out:
                print('\n'.join(map(lambda x: '\t'.join(map(str, sorted(set(map(lambda
                    y: y[0], x))))), C)), file=out)

            if args.plots:
                import matplotlib.pyplot as plt

                fp = join(args.out_dir, f'contig-components.{s}.pdf')
                LOG.info(f'plotting summary statistic to {fp}')
                clen = list(map(len, nx.connected_components(G)))
                (pd.Series(clen).value_counts()/2).sort_index().plot.bar(
                        title=f'contig components of {s}',
                        ylabel='count', xlabel='component size')
                plt.tight_layout()
                plt.savefig(fp, format='pdf')

        else:
            f = join(args.out_dir, f'adj-components.{s}.tsv')
            LOG.info(f'writing adjacency components to {f}')
            # produce output in sorted order, with largest components on top
            C = sorted(nx.components.connected_components(G), key=len, reverse=True)
            with open(f, 'w') as out:
                print('\n'.join(map(lambda x: '\t'.join(map(lambda y:
                    '%s::%s'%y, sorted(x))), C)), file=out)

            if args.plots:
                import matplotlib.pyplot as plt

                fp = join(args.out_dir, f'adj-components.{s}.pdf')
                LOG.info(f'plotting summary statistic to {fp}')
                clen = list(map(len, nx.connected_components(G)))
                (pd.Series(clen).value_counts()/2).sort_index().plot.bar(
                        title=f'adjacency components of {s}',
                        ylabel='count', xlabel='component size')
                plt.tight_layout()
                plt.savefig(fp, format='pdf')
