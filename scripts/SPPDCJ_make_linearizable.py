#!/usr/bin/env python3

from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter as ADHF
from itertools import chain
from os.path import join
from sys import stdout, stderr, exit
import logging

#
# third party libraries
#
import pandas as pd
import networkx as nx
import numpy as np

# logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def build_adj_graph(df, species):
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


    genes = set(df.loc[df.Species == species].Gene_1).union(
            df.loc[df.Species == species].Gene_2)
    G = nx.Graph()
    G.add_nodes_from(map(lambda x: (x, 'h'), genes))
    G.add_nodes_from(map(lambda x: (x, 't'), genes))
    G.add_edges_from(map(lambda x: ((x.Gene_1, x.Ext_1), (x.Gene_2, x.Ext_2)),
        df.loc[df.Species == species].itertuples()))
    return G


def complement_telomeres(G):
    '''
    Adds telomeric adjacencies to each degree-0 extremity
    '''

    c = 0
    for v in tuple(G.nodes()):
        if not G.degree(v):
            c += 1
            G.add_edge(v, (f't_{c}', 'o'), complement=True)
    LOG.info(f'++ added {c} telomeric adjacencies to singleton extremities')
    return c

def complement_conflicting_adjacencies(G, c):
    '''Adds conflicting adjacencies to components to ensure their
    linearizability.
    '''

    for C in tuple(nx.connected_components(G)):
        # ignore non-conflicting adjacencies
        if len(C) <= 2:
            continue
        degs = G.degree(C)
        deg_values = set(map(lambda x: x[1], degs))
        if deg_values == set((2,)):
            LOG.info(f'identified circular component of conflicting ' +\
                    f'adjacencies of size {len(C)}')
            # for even components we don't have to do anything, but for
            # odds..
            if len(C) %2:
                # grab an arbitrary node from the cycle and append a
                # telomere--that should do the trick.
                c += 1
                G.add_edge(next(iter(C)), (f't_{c}', 'o'), complement=True)
        elif deg_values == set((1, 2)):
            LOG.info(f'identified linear component of conflicting ' + \
                    f'adjacencies of size {len(C)}')
            # component is linear 
            ends = [x[0] for x in degs if x[1] == 1]
            if len(C) % 2:
                # component is of odd length; all we gotta do is add 1
                # telomeric extremity and add two telomeric adjacencies to it
                # to close the cycle 
                c += 1
                t = (f't_{c}', 'o')
                for adj in ((ends[0], t), (ends[1], t)):
                    G.add_edge(*adj, complement=True)
            elif len(ends) > 0:
                # component is of even length; all we gotta do is add 1
                # conflicting adjacency to it to close the cycle
                G.add_edge(*ends, complement=True)
        else:
            LOG.info(f'computing maximum matching in component of ' + \
                    f'size {len(C)}')
            M = nx.max_weight_matching(G.subgraph(C))
            unmatched = C.difference(chain(*M))
            while len(unmatched) >= 2:
                G.add_edge(unmatched.pop(), unmatched.pop(), complement=True)
            if unmatched:
                # component is of odd length; all we gotta do is add 1
                # telomeric extremity to connect the last extremity 
                c += 1
                G.add_edge(unmatched.pop(), (f't_{c}', 'o'), complement=True)

if __name__ == '__main__':

    description = '''
    Complements adjacencies with additional conflicting adjacencies and
    telomeric adjacencies to ensure that each degenerate genome is linearizable
    '''
    parser = ArgumentParser(formatter_class=ADHF, description=description)
    parser.add_argument('in_adjacencies', type=open,
            help='Input adjacencies file')
    parser.add_argument('out_adjacencies', type=FileType('w'),
            help='Output adjacencies file')
    parser.add_argument('log_file', type=FileType('w'),
            help='Log file')    
    
    args = parser.parse_args()

    out = stdout

    # setup logging
    ch = logging.FileHandler(args.log_file.name, mode='w')
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s'))
    LOG.addHandler(ch)


    LOG.info(f'loading adjacency set from {args.in_adjacencies.name}')
    df = pd.read_csv(args.in_adjacencies, sep='\t',  header=0)
    if 'penality' not in df.columns:
        df['penality'] = np.nan

    species = df.Species.unique()

    for s in species:
        LOG.info(f'processing species {s}')
        LOG.info(f'++ building adjacency graph')
        G = build_adj_graph(df, s)
        c = complement_telomeres(G)
        complement_conflicting_adjacencies(G, c)
        for (g1, ext1), (g2, ext2), data in G.edges(data=True):
            if 'complement' in data and data['complement']:
                i = df.index.max()+1
                df.loc[i] = [s, g1, ext1, s, g2, ext2, 0, 1]

    LOG.info(f'writing complemented adjacency set to {args.out_adjacencies.name}')
    df.to_csv(args.out_adjacencies, sep='\t', index=False)
