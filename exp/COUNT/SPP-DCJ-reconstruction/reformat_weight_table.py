#!/usr/bin/env python3

# import from built-in packages
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as ADHF, \
        FileType
from sys import stdout, stderr, exit
from itertools import repeat, chain

# import from third-party packages
import pandas as pd
import numpy as np
import ete3

TAXA = [
        'AnophelesgambiaePEST',
        'AnophelesfunestusFUMOZ',
        'AnophelesatroparvusEBRO',
        'AnophelesalbimanusSTECLA',
        'node0',
        'node1',
        'node2'
        ]

if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=ADHF)
    parser.add_argument('weights', type=open, help='Cedir\'s weight table')
    args = parser.parse_args()

    t = ete3.Tree(next(args.weights).strip().split('\t')[1] + ';', format=1)
    df_in = pd.read_csv(args.weights, sep='\t', skiprows=4, dtype=str, header=None)

    df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(chain(zip(repeat('configuration'), TAXA[:4]), zip(repeat('weight'), TAXA[4:]))),
                      index=df_in.index, data=0)
    # cast weights to float
    df['weight'] = 0.0
    for i, (config, weight_str) in df_in.iterrows():
        df.iloc[i, :4] = list(map(int, config))
        for s in weight_str.split():
            taxon, presence, weight = s.split(':')
            if int(presence):
                df.loc[i, ('weight', TAXA[int(taxon)])] = float(weight)

    df.to_csv(stdout, sep='\t', index=False)
