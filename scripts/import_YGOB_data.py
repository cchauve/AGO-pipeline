#!/usr/bin/env python3
# coding: utf-8


'''Importing data from the directory of Evan'''

import os
import sys
import shutil

# Evan data directory
IN_DATA_DIR = '/home/chauvec/projects/ctb-chauvec/ecribbie/USRA_2022/YGOB/DATA/'
# Data directory
OUT_DATA_DIR = '/home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/YGOB'
os.makedirs(OUT_DATA_DIR, exist_ok=True)

# Step 1. Importing species tree
IN_SPECIES_TREE_FILE = os.path.join(IN_DATA_DIR, 'species_tree.tree')
OUT_SPECIES_TREE_FILE = os.path.join(OUT_DATA_DIR, 'species_tree.newick')
print(f'# Importing species tree\t{OUT_SPECIES_TREE_FILE}')
shutil.copy(IN_SPECIES_TREE_FILE, OUT_SPECIES_TREE_FILE)

# Step 2. Extracting species
SPECIES_LIST = open(OUT_SPECIES_TREE_FILE, 'r').readlines()[0].replace('(','').replace(')','').replace(';','').rstrip().split(',')
SPECIES_NB = len(SPECIES_LIST)
print(f'# Number of species\t{SPECIES_NB}')
OUT_SPECIES_FILE = os.path.join(OUT_DATA_DIR, 'species.txt')
print(f'# Extracting species\t{OUT_SPECIES_FILE}')
OUT_SPECIES = open(OUT_SPECIES_FILE, 'w')
with open(OUT_SPECIES_FILE, 'w') as f:
    for idx in range(SPECIES_NB):
        species = SPECIES_LIST[idx]
        if idx < SPECIES_NB-1: f.write(f'{species}\n')
        else: f.write(f'{species}')

def f_idx(f):
    if f == 351: return('10352')
    elif f == 352: return('353a')
    else: return(f'{f+1}')


# Step 3. Creating gene families dictionary, with a label, increasing from 1
IN_FAMILIES_FILE = os.path.join(IN_DATA_DIR, 'desired_pillar.txt')
print(f'# Creating families')
IN_FAMILIES = open(IN_FAMILIES_FILE, 'r').readlines()
FAMILIES_NB = len(IN_FAMILIES)
print(f'# Number of families\t{FAMILIES_NB}')
FAMILIES_DICT = {}
for idx in range(FAMILIES_NB):
    family_idx = f_idx(idx)
    family_str = IN_FAMILIES[idx]
    family = family_str.rstrip().split()
    FAMILIES_DICT[family_idx] = family



# Step 4. Importing gene orders, filtering out genes that are not in families
GENES_LIST_ALL = []
GENES_FAMILY_SPECIES = {}
for family_idx,family in FAMILIES_DICT.items():
    for gene in family:
        GENES_LIST_ALL.append(gene)
        GENES_FAMILY_SPECIES[gene] = {'family': family_idx}
IN_GENE_ORDERS_DIR = os.path.join(IN_DATA_DIR, 'species_genome_tabs')
OUT_GENE_ORDERS_DIR = os.path.join(OUT_DATA_DIR, 'gene_orders')
os.makedirs(OUT_GENE_ORDERS_DIR, exist_ok=True)
GENES_LISTS = {species: [] for species in SPECIES_LIST}
print(f'# Importing gene orders\t{OUT_GENE_ORDERS_DIR}')
for species in SPECIES_LIST:
    IN_GENE_ORDER_FILE = os.path.join(IN_GENE_ORDERS_DIR, f'{species}_genome.txt')
    OUT_GENE_ORDER_FILE = os.path.join(OUT_GENE_ORDERS_DIR, f'{species}.txt')
    with open(OUT_GENE_ORDER_FILE, 'w') as out_f:
        for gene_data in open(IN_GENE_ORDER_FILE, 'r').readlines():
            gene_name = gene_data.split('\t')[0]
            if gene_name in GENES_LIST_ALL:
                new_gene_name = '@'.join([species,gene_name])
                remaining_info = '\t'.join(gene_data.split('\t')[1:])
                out_f.write('\t'.join([new_gene_name,remaining_info]))
                GENES_LISTS[species].append(gene_name)
                GENES_FAMILY_SPECIES[gene_name]['species']=species
    print(f'# {species}\t{len(GENES_LISTS[species])}')


# Step 5. Importing gene families, adding a label first, increasing from 1
OUT_FAMILIES_FILE = os.path.join(OUT_DATA_DIR, 'families.txt')
print(f'# Importing families\t{OUT_FAMILIES_FILE}')
with open(OUT_FAMILIES_FILE, 'w') as f:
    for idx in range(FAMILIES_NB):
        family_idx = f_idx(idx)
        family = FAMILIES_DICT[family_idx]
        fam_str=''
        for gene in family:
            specie = GENES_FAMILY_SPECIES[gene]['species']
            new_gene_name = '@'.join([specie,gene])
            fam_str = ' '.join([fam_str,new_gene_name])
        f.write('\t'.join([family_idx,fam_str.lstrip()]))
        if idx<FAMILIES_NB-1:
            f.write("\n")

# Step 6. Importing gene (DNA) sequences for each family
IN_DNA_DIR = os.path.join(IN_DATA_DIR, 'PILLAR_NT_FILES')
OUT_DNA_DIR = os.path.join(OUT_DATA_DIR, 'genes')
print(f'# Importing genes DNA sequences\t{OUT_DNA_DIR}')
os.makedirs(OUT_DNA_DIR, exist_ok=True)
for idx in range(FAMILIES_NB):
    family_idx = f_idx(idx)
    in_DNA_file = os.path.join(IN_DNA_DIR, f'NT_{idx}.fsa')
    out_DNA_file = os.path.join(OUT_DNA_DIR, f'{family_idx}.fasta')
    with open(in_DNA_file, 'r') as f1, open(out_DNA_file, 'w') as f2:
        for line in f1.readlines():
            if line[0] == '>':
                gene = line.split()[0].lstrip(">")
                specie = GENES_FAMILY_SPECIES[gene]['species']
                new_gene_name = '@'.join([specie,gene])
                f2.write(''.join(['>',new_gene_name,'\n']))
            else: f2.write(line)

# Step 7. Creating a gene,family,species mapping file
OUT_MAP_FILE = os.path.join(OUT_DATA_DIR, 'map.txt')
with open(OUT_MAP_FILE, 'w') as map_file:
    map_file.write('#gene\tfamily\tspecies')
    for gene,data in GENES_FAMILY_SPECIES.items():
        family_idx = data['family']
        species = data['species']
        new_gene_name = '@'.join([species,gene])
        map_file.write(f'\n{new_gene_name}\t{family_idx}\t{species}')


