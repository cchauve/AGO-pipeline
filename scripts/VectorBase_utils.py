#!/usr/bin/env python3
# coding: utf-8


'''Pre-processing VectorBase data'''

import os
import sys
import pandas as pd

'''
Expected data format.
A single tab-separated files with one line per gene and fields:
- Gene ID: gene
- Organism: species name
- Genomic Location (Gene): assembly_chromosome:start..end:strand where strand is +/-
- Chromosome: chromosome or scaffold
- Ortholog Group: family ID
- Coding Sequence: gene squence
'''

ASSEMBLED_SPECIES = [
    'Anopheles_albimanus_STECLA',
    'Anopheles_atroparvus_EBRO',
    'Anopheles_funestus_FUMOZ',
    'Anopheles_gambiae_PEST'
]

''' Reading original data into a DataFrame '''

def rename_columns(data_df, read_seq=False):
    data_df.rename(
        columns={
            'Gene ID': 'gene',
            'Organism': 'species',
            'Genomic Location (Gene)': 'coordinates',
            'Chromosome': 'chromosome',
            'Ortholog Group': 'family'
        },
        inplace=True
    )
    if read_seq:
        data_df.rename(
            columns={'Coding Sequence': 'sequence'},
            inplace=True
        )

def rename_species(data_df):
    data_df['species'] = data_df['species'].map(lambda x: x.replace(' ','_'))

def split_location(data_df):
    def split_entry(s, i):
        s1 = s.replace(',','').replace('(+)',':+').replace('(-)',':-')
        s2 = s1.split(':')
        s3 = s2[1].split('..')
        result = [s2[0],int(s3[0]),int(s3[1]), s2[2]]
        return result[i]
    data_df['scaffold'] = data_df['coordinates'].map(lambda s: split_entry(s,0))
    data_df['start'] = data_df['coordinates'].map(lambda s: split_entry(s,1))
    data_df['end'] = data_df['coordinates'].map(lambda s: split_entry(s,2))
    data_df['strand'] = data_df['coordinates'].map(lambda s: split_entry(s,3))
    data_df.drop(labels=['coordinates'], axis=1, inplace=True)  

def delete_ambiguous_data(data_df):
    nb_rows_before = len(data_df.index)
    data_df.drop(data_df[data_df['family'] == 'NA'].index, inplace = True)
    data_df.drop(data_df[data_df['chromosome'] == 'UNKN'].index, inplace = True)
    data_df.drop(data_df[data_df['chromosome'] == 'Y_unplaced'].index, inplace = True)
    nb_rows_after = len(data_df.index)
    nb_discarded_rows = nb_rows_before - nb_rows_after
    return nb_discarded_rows

def delete_included_genes(data_df):
    prev_species,prev_scaffold,prev_end = '','',-1
    idx_to_discard = []
    for idx,gene in data_df.iterrows():
        species,scaffold,end = gene['species'],gene['scaffold'],gene['end']
        if species==prev_species and scaffold==prev_scaffold and end<prev_end: 
            idx_to_discard.append(idx)
        else:
            prev_species,prev_scaffold,prev_end = species,scaffold,end
    data_df.drop(index=idx_to_discard, inplace=True)
    return len(idx_to_discard)

def read_data(tsv_file, read_seq=False):
    columns = ['Gene ID', 'Organism', 'Genomic Location (Gene)', 'Chromosome', 'Ortholog Group']
    if read_seq:
        columns.append('Coding Sequence')
    data_df = pd.read_table(tsv_file, delimiter='\t', usecols=columns)
    rename_columns(data_df, read_seq=read_seq)
    rename_species(data_df)
    split_location(data_df)
    nb_ambiguous_genes = delete_ambiguous_data(data_df)
    data_df.sort_values(by=['species','scaffold','start'], ascending=True, inplace=True)
    nb_included_genes = delete_included_genes(data_df)
    return data_df,nb_ambiguous_genes,nb_included_genes

''' Selecting data '''

def group_by_OG(data_df):
    return data_df.groupby(['family'])

def group_by_species(data_df):
    return data_df.groupby(['species'])

def check_target_chr(family_df, target_chr):
    stats = {
        species: {'on_target': 0, 'off_target': 0}
        for species in ASSEMBLED_SPECIES
    }
    for _,gene in family_df.iterrows():
        chromosome,species = gene['chromosome'],gene['species']
        if chromosome in target_chr:
            stats[species]['on_target'] +=1
        elif species in ASSEMBLED_SPECIES:
            stats[species]['off_target'] += 1
    return stats

def select_families(data_df_by_family, min_size, target_chr, min_on_target):
    selected_families = []
    nb_families = 0
    stat_small1,stat_absent,stat_off_target,stat_ambiguous,stat_small2,stat_on_target = 0,0,0,0,0,0
    for key, item in data_df_by_family:
        nb_families += 1
        family_df = data_df_by_family.get_group(key)
        family_id = family_df['family'].tolist()[0]
        family_stats = check_target_chr(family_df, target_chr)
        nb_on_target,nb_ambiguous,nb_off_target,nb_absent = 0,0,0,0        
        for species in ASSEMBLED_SPECIES:
            on_target = family_stats[species]['on_target']
            off_target = family_stats[species]['off_target']
            if on_target>0 and off_target==0: nb_on_target += 1
            elif on_target>0 and off_target>0: nb_ambiguous += 1
            elif off_target>0: nb_off_target += 1
            elif on_target==0 and off_target==0: nb_absent += 1

        test_size = len(family_df.index) >= min_size
        test_target = (
            nb_on_target>=min_on_target
            and
            nb_ambiguous+nb_off_target==0
        )

        if not test_size: stat_small1 += 1
        elif nb_absent==len(ASSEMBLED_SPECIES): stat_absent += 1
        elif nb_on_target==0: stat_off_target += 1
        elif nb_ambiguous+nb_off_target>0: stat_ambiguous += 1
        elif nb_on_target<min_on_target: stat_small2 += 1
        else:
            stat_on_target += 1
            selected_families.append(family_id)
    stats = [
        stat_small1,stat_absent,stat_off_target,stat_ambiguous,stat_small2,stat_on_target
    ]
    return selected_families,nb_families,stats

def get_gene_id(df_row, sep='|'):
    gene = df_row['gene']
    species = df_row['species']
    return f'{species}{sep}{gene}'

def build_families(data_df_by_family, selected_families, out_dir, suffix):
    families_file = os.path.join(out_dir,f'families_{suffix}.txt')
    with open(families_file, 'w') as out_file:
        for key, item in data_df_by_family:
            family_df = data_df_by_family.get_group(key)
            family_id = family_df['family'].tolist()[0]
            if family_id in selected_families:
                out_file.write(family_id)
                first_gene = True
                for _,gene in family_df.iterrows():
                    gene_id = get_gene_id(gene)
                    if first_gene:
                        out_file.write(f'\t{gene_id}')
                        first_gene = False
                    else:
                        out_file.write(f' {gene_id}')
                out_file.write('\n')

def build_sequences(data_df_by_family, selected_families, out_dir, suffix):
    sequences_dir = os.path.join(out_dir,f'sequences_{suffix}')
    os.makedirs(sequences_dir, exist_ok=True)
    sequences_file = os.path.join(out_dir,f'sequences_{suffix}.txt')
    with open(sequences_file, 'w') as out_file:
        for key, item in data_df_by_family:
            family_df = data_df_by_family.get_group(key)
            family_id = family_df['family'].tolist()[0]
            if family_id in selected_families:
                fasta_file = os.path.join(sequences_dir,f'{family_id}.fasta')
                with open(fasta_file, 'w') as out_fasta:
                    for _,gene in family_df.iterrows():
                        gene_id = get_gene_id(gene)
                        sequence = gene['sequence']
                        out_fasta.write(f'>{gene_id}\n{sequence}\n')
                out_file.write(f'{family_id}\t{fasta_file}\n')

def build_gene_orders(data_df_by_species, selected_families, out_dir, suffix):
    strand_2_sign = {'+': 1, '-': 0}
    gene_orders_dir = os.path.join(out_dir,f'gene_orders_{suffix}')
    os.makedirs(gene_orders_dir, exist_ok=True)
    gene_orders_file = os.path.join(out_dir,f'gene_orders_{suffix}.txt')
    with open(gene_orders_file, 'w') as out_file:
        for key, item in data_df_by_species:
            species_df = data_df_by_species.get_group(key)
            species = species_df['species'].tolist()[0]
            genes = []
            for _,gene in species_df.iterrows():                
                if gene['family'] in selected_families:
                    gene_data = [
                        get_gene_id(gene),
                        strand_2_sign[gene['strand']],
                        gene['start'], gene['end'],
                        '_', gene['scaffold']
                    ]
                    genes.append(gene_data)
            genes.sort(key=lambda x: (x[5],x[2]))
            gene_order_file = os.path.join(gene_orders_dir,f'{species}.txt')
            with open(gene_order_file, 'w') as out_gene_order:
                for gene in genes:
                    out_gene_order.write('\t'.join([str(x) for x in gene]))
                    out_gene_order.write('\n')
            out_file.write(f'{species}\t{gene_order_file}\n')
                        
# Main                  
                    
command = sys.argv[1]
read_seq = {'stats': False, 'build': True, 'test': False}
genes_file = sys.argv[2]
target_chr = sys.argv[3].split()
min_on_target = int(sys.argv[4])
min_size = int(sys.argv[5])

data_df,nb_ambiguous_genes,nb_included_genes = read_data(genes_file, read_seq=read_seq[command])
data_df_by_family = group_by_OG(data_df)
selected_families,nb_families,stats = select_families(data_df_by_family, min_size, target_chr, min_on_target)

if command == 'stats':
    print(f'#Target {target_chr} Min size {min_size} Min size on target {min_on_target}')
    print(f'Filter    \tambiguous:{nb_ambiguous_genes}\tincluded:{nb_included_genes}')
    print(f'All       \t{nb_families}')
    print(f'Small1    \t{stats[0]}')
    print(f'Absent    \t{stats[1]}')
    print(f'Off target\t{stats[2]}')
    print(f'Ambiguous \t{stats[3]}')
    print(f'Small2    \t{stats[4]}')
    print(f'On target \t{stats[5]}\t{len(selected_families)}')
elif command == 'build':
    out_dir = sys.argv[6]
    out_suffix = '_'.join(target_chr)
    build_families(data_df_by_family, selected_families, out_dir, out_suffix)
    build_sequences(data_df_by_family, selected_families, out_dir, out_suffix)
    data_df_by_species = group_by_species(data_df)
    build_gene_orders(data_df_by_species, selected_families, out_dir, out_suffix)

    
    
