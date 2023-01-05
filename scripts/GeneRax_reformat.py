#!/usr/bin/env python3
# coding: utf-8

""" Reformat recPhyloXML files to be read by DeCoSTAR """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os
from recPhyloXML_utils import xml_reformat_file

def main():
    families_file = sys.argv[1]
    results_dir = sys.argv[2]
    suffix = sys.argv[3]
    with open(families_file, 'r') as families:
        current_id = 0
        for line in families.readlines():
            if line.startswith('- '):
                fam_id = line.rstrip()[2:]
                in_file = os.path.join(results_dir, 'reconciliations', f'{fam_id}_reconciliated.xml')
                out_file = os.path.join(results_dir, 'reconciliations', f'{fam_id}{suffix}')
                if os.path.isfile(in_file):
                    current_id = xml_reformat_file(in_file, out_file, start_id=current_id)

if __name__ == "__main__":
    main()

