#!/usr/bin/env python3
# coding: utf-8

""" FASTA utils """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

import sys
from Bio import SeqIO

def fasta_get_names(in_fasta_file):
    '''
    input: path to FASTA file
    output: list of names of sequences
    '''
    names = []
    with open(in_fasta_file, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            names.append(record.id)
    return names
