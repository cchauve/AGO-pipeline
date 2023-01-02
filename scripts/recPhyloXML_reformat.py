#!/usr/bin/env python3
# coding: utf-8

""" Reformat recPhyloXML files to be read by DeCoSTAR """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os

def recPhyloXML_format(in_file, out_file, start_id=0):
    ''' Should be done using the XML libray '''
    with open(in_file, 'r') as in_xml, \
         open(out_file, 'w') as out_xml:
        out_xml.write('<recPhylo>\n')
        current_id = start_id
        for line in in_xml.readlines()[1:]:
            line1 = line.strip()
            if line1[0]!='<': continue
            if line1 == '<name></name>':
                out_xml.write(line.replace('><', f'>{current_id}<'))
                current_id += 1
            elif line1.startswith('<speciation'):
                out_xml.write(line.replace('/>', '></speciation>'))
            elif line1.startswith('<leaf'):
                out_xml.write(line.replace('/>', '></leaf>'))
            elif line1.startswith('<duplication'):
                out_xml.write(line.replace('/>', '></duplication>'))
            elif line1.startswith('<loss'):
                out_xml.write(line.replace('/>', '></loss>'))
            elif line1.startswith('<speciationLoss'):
                out_xml.write(line.replace('/>', '></speciationLoss>'))
            else:
                out_xml.write(line)
    return(current_id)

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
                    current_id = recPhyloXML_format(in_file, out_file, start_id=current_id)

if __name__ == "__main__":
    main()

