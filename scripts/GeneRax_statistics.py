#!/usr/bin/env python3
# coding: utf-8

""" Compute statistics for a set of recPhyloXML reconciled files """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import xml.etree.ElementTree as ET
from recPhyloXML_utils import (
    xml_get_tag,
    xml_get_prefix,
    xml_get_text,
    xml_get_name,
    xml_get_rec_species,
    xml_parse_tree
)

# Statistics dictionary keys
STATS_genes = 'genes' # Number of genes
STATS_dup = 'duplications' # Number of duplications
STATS_loss = 'losses' # Number of losses
# XML tags to corresponding statistics keys
STATS_xmlkeys = {
    'leaf': STATS_genes,
    'speciation': STATS_genes,
    'duplication': STATS_dup,
    'loss': STATS_loss
}
STATS_keys = [STATS_genes, STATS_dup, STATS_loss]

def recPhyloXML_read_events(in_file):
    ''' 
    Read a recPhyloXML file and returns a dictionary indexed by species
    and for each containing a dictionary recording number of genes, 
    of duplications and of losses with the keys STATS_genes, STATS_dup, 
    STATS_loss
    '''

    def parse_spTree(root, tag_pref):
        ''' 
        input: XML root node
        output: 
        dict(species name(str) -> 
        species name of sibling species (str/None))
        '''
        return xml_parse_tree(root, tag_pref, output_type=1)

    def parse_recGeneTree(root, tag_pref, siblings):
        ''' 
        input: XML root node
        output: 
        dict(species name(str) -> 
        dict(STATS_genes: int, STATS_dup: int, STATS_loss: int))
        '''
        def parse_clade_recursive(node, tag_pref, stats):
            # Reconciliation event (possibly more than one)
            events = node.find(f'{tag_pref}eventsRec')
            # If more than one, then speciationLoss ended by last event
            # Loop on speciationLoss events to add a loss to the sibling species
            for event in events[1:][::-1]:
                stats[siblings[xml_get_rec_species(event)]][STATS_loss] += 1
            # Last event
            last_event_tag = xml_get_tag(events[-1])
            last_event_species = xml_get_rec_species(events[-1])
            stats[last_event_species][STATS_xmlkeys[last_event_tag]] += 1
            # Recursive calls
            for child in node.findall(f'{tag_pref}clade'):
                parse_clade_recursive(child, tag_pref, stats)
        stats = {
            sp:{STATS_genes: 0, STATS_dup: 0, STATS_loss: 0}
            for sp in siblings.keys()
        }
        parse_clade_recursive(root, tag_pref, stats)
        return(stats)

    root = ET.parse(in_file).getroot()
    tag_pref = xml_get_prefix(root)
    siblings = parse_spTree(
        root.find(f'{tag_pref}spTree').find(f'{tag_pref}phylogeny').find(f'{tag_pref}clade'),
        tag_pref
    )
    recStats = parse_recGeneTree(
        root.find(f'{tag_pref}recGeneTree').find(f'{tag_pref}phylogeny').find(f'{tag_pref}clade'),
        tag_pref,
        siblings
    )
    return(recStats)


def collect_statistics(in_reconciliations_file):
    statistics_species = {}
    statistics_families = {}
    with open(in_reconciliations_file, 'r') as reconciliations:
        for line in reconciliations.readlines():
            reconciliation = line.rstrip().split()
            fam_id = reconciliation[0]
            reconciliation_path = reconciliation[1]
            print(reconciliation_path)
            events = recPhyloXML_read_events(reconciliation_path)
            statistics_families[fam_id] = events
            for species,stats in statistics_families[fam_id].items():
                if species not in statistics_species.keys():
                    statistics_species[species] = {
                        STATS_genes: 0, STATS_dup: 0, STATS_loss: 0
                    }
                for stats_key in STATS_keys:
                    statistics_species[species][stats_key] += stats[stats_key]
    return (statistics_families,statistics_species)

def _stats_str(stats, sp, sep=':'):
    return sep.join(
        [
            str(sp),
            str(stats[STATS_genes]),
            str(stats[STATS_dup]),
            str(stats[STATS_loss])]
    )

def write_statistics_species(
        statistics_species,
        out_stats_file_species,
        sep1=':', sep2='\t', sep3=' '
):
    with open(out_stats_file_species, 'w') as stats_file:
        header1 = sep1.join(
            ['#species', STATS_genes, STATS_dup, STATS_loss]
        )
        stats_file.write(header1)
        for species,stats in statistics_species.items():
            stats_file.write(
                f'\n{_stats_str(stats, species, sep=sep1)}'
            )

def write_statistics_families(
        statistics_families,
        out_stats_file_families,
        sep1=':', sep2='\t', sep3=' '
):
    with open(out_stats_file_families, 'w') as stats_file:
        header1 = sep1.join(
            ['nb_species', STATS_genes, STATS_dup, STATS_loss]
        )
        header2 = sep1.join(
            ['species', STATS_genes, STATS_dup, STATS_loss]
        )
        header3 = f'#family{sep2}{header1}{sep2}{header2}'
        stats_file.write(header3)
        for fam_id,stats_all in statistics_families.items():
            stats_file.write(f'\n{fam_id}{sep2}')
            stats_fam = {
                STATS_genes: 0, STATS_dup: 0, STATS_loss: 0
            }
            stats_str = []
            nb_species = 0
            for species,stats in stats_all.items():
                if stats[STATS_genes] > 0:
                    nb_species += 1
                for stats_key in STATS_keys:
                    stats_fam[stats_key] += stats[stats_key]
                stats_str.append(
                    _stats_str(stats, species, sep=sep1)
                )
            stats_file.write(
                f'{_stats_str(stats_fam, nb_species, sep=sep1)}{sep2}'
            )
            stats_file.write(f'{sep3.join(stats_str)}')

def main():
    in_reconciliations_file = sys.argv[1]
    out_stats_file_species = sys.argv[2]
    out_stats_file_families = sys.argv[3]

    # Reading reconciliations and collecting statistics
    (statistics_families,statistics_species) = collect_statistics(in_reconciliations_file)
    # Writting species statistics
    write_statistics_species(statistics_species, out_stats_file_species)
    # Writting families statistics
    write_statistics_families(statistics_families, out_stats_file_families)

if __name__ == "__main__":
    main()

