#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as ADHF
from sys import stdout, stderr, exit
from itertools import repeat, chain
from io import StringIO
import requests
import logging
import json

#
# third party libraries
#
import pandas as pd
import numpy as np
import re

#
# own modules
#


# logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

PAT_LOC = re.compile(r'^([^:]+):([0-9,]+)\.\.([0-9,]+)\((\+|-)\)$')

VECTORBASE_TRANSCRIPT_SEARCHES_URL = 'https://vectorbase.org/vectorbase/service/record-types/transcript/searches/GenesByInterproDomain/reports/standard'

def queryVectorBase(organism):
    '''
    Queries vectorbase to get information on protein domains
    Parameters
    ----------
    organism : str
        organism name

    Returns
    -------
    dict 
        JSON response
    '''

    params  = {
            'organism' : organism,
            'domain_database' : 'INTERPRO',
            'domain_typeahead': '["N/A"]',
            'domain_accession': '*',
            'reportConfig': json.dumps({
                'attributes': [
#                    'primary_key',
#                    'organism',
                    'gene_location_text',
                    'chromosome',
#                    'sequence_id',
                    'interpro_id',
                    'pfam_id',
                    'tigrfam_id',
#                    'superfamily_id',
                    'prositeprofiles_id',
                    'pirsf_id',
                    'smart_id',
                    'protein_sequence', 
                    ],
                'tables': [],
                'attributeFormat': 'text'
                })
            }

    response = requests.get(VECTORBASE_TRANSCRIPT_SEARCHES_URL, params=params)
    return response.json()

def _get_loc(txt):

    m = PAT_LOC.match(txt)
    if m:
        _, start, end, orient = m.groups()
        return start.replace(',',''), end.replace(',', ''), orient
    else:
        raise Exception(f'location "{txt}" does not match required pattern {PAT_LOC.pattern}')

def produceFrame(json):

    data =map(lambda x:
                (
                     
                    next(filter(lambda y: y['name'] == 'gene_source_id', x['id']))['value'],
                    x['attributes']['chromosome']
                    ) +
                _get_loc(x['attributes']['gene_location_text']) + 
                (
                    x['attributes']['interpro_id'],
                    x['attributes']['pfam_id'],
                    x['attributes']['tigrfam_id'],
                    x['attributes']['prositeprofiles_id'],
                    x['attributes']['pirsf_id'],
                    x['attributes']['smart_id'],
                    x['attributes']['protein_sequence']
                    ),
              json['records']
              )

    df = pd.DataFrame(data = data, columns=['gene_id', 'chromosome', 'start', 'end', 'orient', 'interpro_ids', 'pfam_id', 'tigrfam_id',
                                            'prositeprofiles_id', 'pirsf_id', 'smart_id', 'protein_sequence'])

    return df

if __name__ == '__main__':
    description = '''
    Query VectorBase for information on protein domains of genes of a given organism
    '''

    parser = ArgumentParser(formatter_class=ADHF, description=description)
    parser.add_argument('organism', type=str, help='Organism of interest')
    args = parser.parse_args()

    out = stdout

    # setup logging
    ch = logging.StreamHandler(stderr)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s'))
    LOG.addHandler(ch)

    df = produceFrame(queryVectorBase(args.organism))
    df[df == 'N/A'] = ''
    df.to_csv(out, sep='\t', index=False)
