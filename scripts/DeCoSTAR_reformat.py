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
import ete3
from DeCoSTAR_create_input_files import read_families as decostar_genes_map
from recPhyloXML_utils import xml_get_gene_tree_root, xml_parse_tree

''' Creates a map from node names to list of descendant extant species '''
def newick_get_leaves(species_tree_file):
    '''
    input: paths to a Newick species tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    tree = ete3.Tree(species_tree_file, format=1)
    leaves = defaultdict(list)
    for node in tree.traverse():
        for leaf in node:
            leaves[node.name].append(leaf.name)
        leaves[node.name].sort()
    return(leaves)

''' Reads the map from nodes to descendant leaves from DeCoSTAR output '''
def decostar_get_leaves(in_species_file):
    '''
    input:
    - DeCoSTAR species file
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    leaves = {}
    with open(in_species_file, 'r') as in_species:
        for node in in_species.readlines():
            node_data = node.rstrip().split()
            leaves[node_data[0]] = node_data[1:]
            leaves[node_data[0]].sort()
    return(leaves)

''' Returns a map of correspondance between species names of species tree and DeCoSTAR species '''
def decostar_species_map(in_species_tree_file, in_species_file):
    '''
    input:
    - original species tree file
    - DeCoSTAR species file
    output: dict(str->str) indexd by DeCoSTAR species labels
    '''
    newick_leaves_map = newick_get_leaves(in_species_tree_file)
    decostar_leaves_map = decostar_get_leaves(in_species_file)
    map_aux = defaultdict(list)
    for species,leaves in newick_leaves_map.items():
        map_aux[''.join(leaves)].append(species)
    for species,leaves in decostar_leaves_map.items():
        map_aux[''.join(leaves)].append(species)
    species_map = {}
    for species_pair in map_aux.values():
        species_map[species_pair[1]] = species_pair[0]
    return(species_map)

''' Returns a dictionary from reconciliation path to family '''
def decostar_reconciliation2family(in_reconciliations_file):
    '''
    input: reconciliations access file
    output: dict(reconciliation path -> family ID)
    '''
    reconciliation2family = {}
    with open(in_reconciliations_file, 'r') as reconciliations:
        for reconciliation in reconciliations.readlines():
            fam_id = reconciliation.split()[0]
            rec_path = reconciliation.split()[1].rstrip()
            reconciliation2family[rec_path] = fam_id
    return reconciliation2family

''' Read DeCoSTAR genes file to compute a map from gene name to list of descendant extant leaves '''
def decostar_genes2leaves(in_genes_file, char_sep='|'):
    gene2leaves = {}
    with open(in_genes_file, 'r') as in_genes:
        for gene_data in in_genes.readlines():
            data = gene_data.rstrip().split()
            gene = data[1]
            gene2leaves[gene] = []
            if len(data) == 2:
                gene2leaves[gene] = [gene]
            else:
                for child in data[2:]:
                    if char_sep in child:
                        gene2leaves[gene] += gene2leaves[child]
                    else:
                        gene2leaves[gene] += [child]
            gene2leaves[gene].sort()
    return gene2leaves

''' Read DeCoSTAR genes file '''
def decostar_reformat_genes(
        in_species_map,
        in_families_file,
        in_reconciliations_file,
        in_gene_trees_file,
        in_genes_file,
        out_genes_file,
        char_sep='|'
):
    '''
    input:
    - dict(str->str): mapping from DeCoSTAR species names to species names
    - original families file
    - reconciliations access file
    - DeCoSTAR gene trees distribution file
    - DeCoSTAR genes file
    - reformated genes file
    - [optional] separator family<char_sep>gene
    output:
    dict(str->str): mapping from DeCoSTAR gene names to reformated gene names
    of format family_name<char_sep>gene_name for ancestral genes
    '''
    # Dictionary original extant gene name -> <name><char_sep><original family>
    genes_name = {
        gene: f'{fam_id}{char_sep}{gene}'
        for gene,fam_id in decostar_genes_map(in_families_file).items()
    }
    # Dictionary reconciliation path -> family ID
    reconciliation2family = decostar_reconciliation2family(in_reconciliations_file)
    # Mapping from DeCoSTAR family (integer) ID to original family ID
    family_idx2id = {}
    with open(in_gene_trees_file, 'r') as in_gene_trees:
        fam_idx = 0
        for reconciliation in in_gene_trees.readlines():
            family_idx2id[str(fam_idx)] = reconciliation2family[reconciliation.rstrip()]
            fam_idx += 1
    # Dictionary list of extant descendants -> GeneRax gene name
    leaves2gene_map = {}
    for rec_path,fam_id in reconciliation2family.items():
        rec_root,tag_pref = xml_get_gene_tree_root(rec_path)
        _gene2leaves_map = xml_parse_tree(rec_root, tag_pref, output_type=2)
        for gene,leaves in _gene2leaves_map.items():
            if len(leaves) > 0:
                leaves.sort()
                leaves2gene_map[char_sep.join(leaves)] = gene
    # Dictionary DeCoSTAR gene name -> list of descendant extant descendants
    gene2leaves_map = decostar_genes2leaves(in_genes_file, char_sep=char_sep)
    # Mapping DeCoSTAR gene names to original names by identifying leaves sets
    gene_name_mapping = {}
    for gene,leaves in gene2leaves_map.items():
        leaves_str = char_sep.join(leaves)
        gene_name = leaves2gene_map[leaves_str]
        gene_name_mapping[gene] = gene_name
    # Reformatting genes
    with open(in_genes_file, 'r') as in_genes, \
         open(out_genes_file, 'w') as out_genes:
        for line in in_genes.readlines():
            line_split = line.rstrip().split()
            in_species,in_gene = line_split[0:2]
            out_species = in_species_map[in_species]
            if char_sep in in_gene:
                # Ancestral gene: replace DeCoSTAR family name by original family name 
                family,gene_id = in_gene.split(char_sep)
                out_gene = f'{family_idx2id[family]}{char_sep}{gene_id}'
                genes_name[in_gene] = out_gene
            else:
                # Extant gene: name expandd with original family name
                out_gene = genes_name[in_gene]
            out_gene_str = ' '.join(
                [out_species, out_gene] +
                [genes_name[gene] for gene in line_split[2:]]
            )
            out_genes.write(f'{out_gene_str}\n')
    # Issue: the gene names do not match with the GeneRax gene names
    # For every GeneRax pre-speciation gene we should have the list of its extant descendants
    # Do the same for DeCoSTAR genes.
    # Then use these lists + species to match gene names
    return(genes_name)

''' Reformat DeCoSTAR adjacencies file '''
def decostar_reformat_adjacencies_file(
        in_species_map,
        in_genes_name,
        in_adjacencies_file,
        out_adjacencies_dir
):
    '''
    input:
    - dict(str->str): mapping from DeCoSTAR species names to species names
    - dict(str->str): mapping from DeCoSTAR gene names to reformated gene names
      of format family_name|gene_name for ancestral genes
    - DeCoSTAR adjacencies file
    - file with paths to adjacencies for every species
    - directory where to write species adjacencies files
    '''
    adjacencies = {
        species: [] for species in in_species_map.values()
    }
    with open(in_adjacencies_file, 'r') as in_adjacencies:
        for line in in_adjacencies.readlines():
            line_split = line.rstrip().split()
            in_species,in_gene1,in_gene2 = line_split[0],line_split[1],line_split[2]
            out_species = in_species_map[in_species]
            out_gene1,out_gene2 = in_genes_name[in_gene1],in_genes_name[in_gene2]
            out_adjacency_str = ' '.join(
                [out_gene1, out_gene2] + line_split[3:]
            )
            adjacencies[out_species].append(out_adjacency_str)
    for species,species_adjacencies in adjacencies.items():
        out_species_adjacencies_file = os.path.join(
            out_adjacencies_dir, f'{species}_adjacencies.txt'
        )
        with open(out_species_adjacencies_file, 'w') as out_species_adjacencies:
            for out_adjacency in species_adjacencies:
                out_species_adjacencies.write(f'{out_adjacency}\n')


def main():
    in_species_tree_file = sys.argv[1]
    in_species_file = sys.argv[2]
    in_families_file = sys.argv[3]
    in_reconciliations_file = sys.argv[4]
    in_gene_trees_file = sys.argv[5]
    in_genes_file = sys.argv[6]
    in_adjacencies_file = sys.argv[7]
    out_genes_file = sys.argv[8]
    out_adjacencies_dir = sys.argv[9]    

    species_map = decostar_species_map(in_species_tree_file, in_species_file)
    genes_map = decostar_reformat_genes(
        species_map, in_families_file,
        in_reconciliations_file, in_gene_trees_file,
        in_genes_file, out_genes_file
    )
    decostar_reformat_adjacencies_file(
        species_map, genes_map, in_adjacencies_file, out_adjacencies_dir
    )
    
if __name__ == "__main__":
    main()

