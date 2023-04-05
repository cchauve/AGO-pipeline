#!/usr/bin/env python3
# coding: utf-8

""" Reformat DeCoSTAR genes and adjacencies """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os
from collections import defaultdict

from data_utils import (
    data_create_equivalence_map,
    data_species_map,
    data_gene2family,
    data_reconciliation_path2family
)
from recPhyloXML_utils import (
    xml_get_gene_tree_root,
    xml_parse_tree
)

''' Separator family/gene in DeCoStar ancestral genes '''
decostar_sep = '|'

''' Reads the DeCoSTAR map from nodes to descendant extant species '''
def decostar_read_species_file(in_species_file):
    '''
    input: DeCoSTAR species file
    output: dictionary dict(str->list(str)) indexed by names of 
      nodes in  in_species_file to list of extant descendants 
      species each list is sorted in alphabetical order
    '''
    leaves = {}
    with open(in_species_file, 'r') as in_species:
        for species_data in in_species.readlines():
            species = species_data.rstrip().split()[0]
            descendants = species_data.rstrip().split()[1:]
            leaves[species] = descendants
            leaves[species].sort()
    return leaves

''' Returns a map from DeCoSTAR species name to original species name '''
def decostar_species_map(in_species_file, in_decostar_species_file):
    '''
    input:
    - original species file
    - DeCoSTAR species file
    output: dict(str->str) Decostar species name -> original species name
    '''
    in_species_map = data_species_map(in_species_file)
    in_decostar_species_map = decostar_read_species_file(in_decostar_species_file)
    species_map_from_decostar = data_create_equivalence_map(in_species_map, in_decostar_species_map, direction=2)
    return(species_map_from_decostar)

''' Returns a map from DeCoSTAR family ID to original family ID '''
def decostar_family_map(
        in_gene_trees_file, in_reconciliations_file, add_path=False
):
    '''
    input: 
    - in_gene_trees_file: DeCoSTAR input gene trees distribution file
    - in_reconciliations_file: map to original family ID to rec. path
    - if add_path is True, adds the reconciliation path
    output:
    dict(str->str) from DeCoSTAR family ID to original family ID
    '''
    reconciliation2family = data_reconciliation_path2family(
        in_reconciliations_file
    )
    family_map = {}
    with open(in_gene_trees_file, 'r') as in_gene_trees:
        decostar_fam_idx = 0
        for reconciliation in in_gene_trees.readlines():
            rec_path = reconciliation.rstrip()
            decostar_fam_id = str(decostar_fam_idx)
            original_fam_id = reconciliation2family[rec_path]
            if add_path:
                family_map[decostar_fam_id] = (original_fam_id,rec_path)
            else:
                family_map[decostar_fam_id] = original_fam_id
            decostar_fam_idx += 1
    return family_map

'''=
Test if a string is the name of an ancestral gene
An ancestral gene is of the form <integer>|<integer>
'''
def decostar_test_ancestral(gene):
    gene1 = gene.split(decostar_sep)
    return len(gene1)==2 and gene1[0].isdigit() and gene1[1].isdigit()

''' 
Read DeCoSTAR genes file to compute a map from gene name 
to list of descendant (gene) leaves 
'''
def decostar_genes2leaves(in_genes_file):
    '''
    input: DeCoSTAR genes file, separator family/gene
    output: dict(gene name -> list of descendant (gene) leaves)
    '''
    gene2leaves = {}
    with open(in_genes_file, 'r') as in_genes:
        for gene_data in in_genes.readlines():
            data = gene_data.rstrip().split()
            gene = data[1]
            gene2leaves[gene] = []
            if len(data) == 2: # Extant leaf
                gene2leaves[gene] = [gene]
            for child in data[2:]:
                if decostar_test_ancestral(child): # Ancestral gene
                    gene2leaves[gene] += gene2leaves[child]
                else: # Extant leaf, no descendant
                    gene2leaves[gene] += [child]
            gene2leaves[gene].sort()
    return gene2leaves

''' Returns a map from DeCoSTAR gene names to original gene names '''
def decostar_gene_map(in_family_map, in_genes_file):
    '''
    input:
    - dict(DeCoSTAR family ID -> (original family ID, reconciliation path))
    - DeCoSTAR genes file
    output:
    dict(DeCoSTAR gene name -> original gene name)
    '''
    # Dictionary (list of extant descendants genes -> original gene name)
    leaves2gene_map = {}
    for (fam_id,rec_path) in in_family_map.values():
        rec_root,tag_pref = xml_get_gene_tree_root(rec_path)
        _gene2leaves_map = xml_parse_tree(rec_root, tag_pref, output_type=2)
        for gene,leaves in _gene2leaves_map.items():
            if len(leaves) > 0:
                leaves.sort()
                leaves2gene_map[decostar_sep.join(leaves)] = gene
    # Dictionary DeCoSTAR gene name -> list of descendant extant genes
    gene2leaves_map = decostar_genes2leaves(in_genes_file)
    # Mapping DeCoSTAR gene names to original names by identifying leaves sets
    genes_map = {}
    for decostar_gene,decostar_leaves in gene2leaves_map.items():
        decostar_leaves_str = decostar_sep.join(decostar_leaves)
        original_gene = leaves2gene_map[decostar_leaves_str]
        genes_map[decostar_gene] = original_gene
    return genes_map

''' Reformat DeCoSTAR genes file '''
def decostar_reformat_genes(
        in_species_map,
        in_families_file,
        in_reconciliations_file,
        in_gene_trees_file,
        in_genes_file,
        out_genes_file
):
    '''
    input:
    - dict(str->str): mapping from DeCoSTAR species names to species names
    - original families file
    - reconciliations access file
    - DeCoSTAR gene trees distribution file
    - DeCoSTAR genes file
    - reformated genes file
    output:
    dict(str->str): mapping from DeCoSTAR gene names to reformated gene names
    of format family_name<decostar_sep>gene_name for ancestral genes
    '''
    # Dictionary (original extant gene name) -> <name><decostar_sep><original family>
    original_fam_gene = {
        gene: f'{fam_id}{decostar_sep}{gene}'
        for gene,fam_id in data_gene2family(in_families_file).items()
    }
    # Mapping from DeCoSTAR family (integer) ID to original family ID
    # and reconciliation path
    family_map = decostar_family_map(
        in_gene_trees_file, in_reconciliations_file, add_path=True
    )
    # Mapping DeCoSTAR gene names to original names
    gene_map = decostar_gene_map(family_map, in_genes_file)
    # Reformatting genes
    with open(in_genes_file, 'r') as in_genes, \
         open(out_genes_file, 'w') as out_genes:
        for line in in_genes.readlines():
            line_split = line.rstrip().split()
            in_species,in_fam_gene = line_split[0:2]
            out_species = in_species_map[in_species]
            if decostar_test_ancestral(in_fam_gene):
                # Ancestral gene: replace DeCoSTAR family name by original 
                # family name and DeCoSTAR gene name by original gene name
                in_fam,in_gene = in_fam_gene.split(decostar_sep)
                out_fam = family_map[in_fam][0]
                out_gene = gene_map[in_fam_gene]
                out_fam_gene = f'{out_fam}{decostar_sep}{out_gene}'
                original_fam_gene[in_fam_gene] = out_fam_gene
            else:
                # Extant gene: no change
                out_fam_gene = original_fam_gene[in_fam_gene]
            # Assumption: non-leaf genes appear in in_genes_file in a
            # bottom-up order: descendants appear before ancestors
            out_gene_str = ' '.join(
                [out_species, out_fam_gene] +
                [original_fam_gene[gene] for gene in line_split[2:]]
            )
            out_genes.write(f'{out_gene_str}\n')
    return original_fam_gene

''' 
Reads a DeCoSTAR adjacencies fiel and returns a list of
adjacencies in form (species,gene1,gene2,extremity1,extremity2,weight1,weight2)
'''
def decostar_read_adjacencies(in_adjacencies_file, species=None):
    adjacencies = []
    with open(in_adjacencies_file, 'r') as in_adjacencies:
        for line in in_adjacencies.readlines():
            if species is None:
                sp,g1,g2,sign1,sign2,w1,w2 = line.rstrip().split()
                adjacencies.append([sp,g1,g2,sign1,sign2,w1,w2])
            else:
                g1,g2,sign1,sign2,w1,w2 = line.rstrip().split()
                adjacencies.append([species,g1,g2,sign1,sign2,w1,w2])
    return adjacencies
            
''' Reformat DeCoSTAR adjacencies file '''
def decostar_reformat_adjacencies_file(
        in_species_map,
        in_genes_name,
        in_adjacencies_file,
        out_adjacencies_dir,
        suffix = '_adjacencies.txt'
):
    '''
    input:
    - dict(str->str): mapping from DeCoSTAR species names to species names
    - dict(str->str): mapping from DeCoSTAR gene names to reformated gene names
      of format family_name<decostar_sep>gene_name for ancestral genes
    - DeCoSTAR adjacencies file
    - file with paths to adjacencies for every species
    - directory where to write species adjacencies files
    '''
    species_adjacencies = {
        species: [] for species in in_species_map.values()
    }
    adjacencies_list = decostar_read_adjacencies(
        in_adjacencies_file, species=None
    )
    for (in_sp,in_g1,in_g2,in_sign1,in_sign2,w1,w2) in adjacencies_list:
        out_sp = in_species_map[in_sp]
        out_g1,out_g2 = in_genes_name[in_g1],in_genes_name[in_g2]
        out_adjacency_str = ' '.join(
            [out_g1, out_g2] + [in_sign1,in_sign2,w1,w2]
        )
        species_adjacencies[out_sp].append(out_adjacency_str)
    for species,adjacencies in species_adjacencies.items():
        out_sp_adjacencies_file = os.path.join(
            out_adjacencies_dir, f'{species}{suffix}'
        )
        with open(out_sp_adjacencies_file, 'w') as out_sp_adjacencies:
            for out_adjacency in adjacencies:
                out_sp_adjacencies.write(f'{out_adjacency}\n')


def main():
    in_species_file = sys.argv[1]
    in_decostar_species_file = sys.argv[2]
    in_families_file = sys.argv[3]
    in_reconciliations_file = sys.argv[4]
    in_gene_trees_file = sys.argv[5]
    in_genes_file = sys.argv[6]
    in_adjacencies_file = sys.argv[7]
    out_genes_file = sys.argv[8]
    out_adjacencies_dir = sys.argv[9]    

    species_map = decostar_species_map(
        in_species_file, in_decostar_species_file
    )
    genes_map = decostar_reformat_genes(
        species_map,
        in_families_file, in_reconciliations_file,
        in_gene_trees_file, in_genes_file,
        out_genes_file
    )
    decostar_reformat_adjacencies_file(
        species_map, genes_map, in_adjacencies_file,
        out_adjacencies_dir
    )
    
if __name__ == "__main__":
    main()

