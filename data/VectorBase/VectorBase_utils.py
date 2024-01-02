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

_ASSEMBLED_SPECIES = [
    'Anopheles albimanus STECLA',
    'Anopheles atroparvus EBRO',
    'Anopheles funestus FUMOZ',
    'Anopheles gambiae PEST'
]

def rename_object(name, sep=''):
    ''' Rename an object by deleting all non alphanumeric characters '''
    return sep.join(filter(str.isalnum, name))

ASSEMBLED_SPECIES = [
    rename_object(species) for species in _ASSEMBLED_SPECIES
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

def delete_species(data_df, target_species):
    all_species = data_df['species'].unique()
    discarded_species = [s for s in all_species if s not in target_species]
    data_df.drop(data_df[data_df['species'].isin(discarded_species)].index, inplace = True)
    for species in discarded_species:
        if species in ASSEMBLED_SPECIES:
            ASSEMBLED_SPECIES.remove(species)
    return len(discarded_species)

def delete_ambiguous_data(data_df):
    nb_rows_before = len(data_df.index)
    data_df.drop(data_df[data_df['family'].str.startswith('NA')].index, inplace = True)
    data_df.drop(data_df[data_df['chromosome'] == 'UNKN'].index, inplace = True)
    data_df.drop(data_df[data_df['chromosome'] == 'Yunplaced'].index, inplace = True)
    nb_rows_after = len(data_df.index)
    nb_discarded_rows = nb_rows_before - nb_rows_after
    return nb_discarded_rows

def delete_included_genes(data_df):
    prev_species,prev_scaffold,prev_end = '','',-1
    idx_to_discard = []
    for idx,gene in data_df.iterrows():
        species,scaffold,end = gene['species'],gene['scaffold'],gene['end']
        if species==prev_species and scaffold==prev_scaffold and end<=prev_end: 
            idx_to_discard.append(idx)
        else:
            prev_species,prev_scaffold,prev_end = species,scaffold,end
    data_df.drop(index=idx_to_discard, inplace=True)
    return len(idx_to_discard)

def rename_data(data_df, out_map_file):
    if out_map_file is not None:
        with open(out_map_file, 'w') as map_file:
            map_file.write('#original object:(species)(gene)(chromosome)(family)\t')
            map_file.write('renamed_object:(species)(gene)(chromosome)(family)')
            for idx,gene in data_df.iterrows():
                data = [gene['species'], gene['gene'], gene['chromosome'], gene['family']]
                original_object = ''.join([f'({x})' for x in data])
                renamed_object = ''.join([f'({rename_object(x)})' for x in data])
                map_file.write(f'\n{original_object}\t{renamed_object}')        
    for column in ['gene', 'species', 'chromosome', 'family']:
        data_df[column] = data_df[column].map(lambda x: rename_object(x))

def read_data(tsv_file, target_species, out_dir, read_seq=False):
    columns = ['Gene ID', 'Organism', 'Genomic Location (Gene)', 'Chromosome', 'Ortholog Group']
    if read_seq:
        columns.append('Coding Sequence')
    data_df = pd.read_table(tsv_file, delimiter='\t', usecols=columns)
    rename_columns(data_df, read_seq=read_seq)
    if out_dir is None:
        names_map_file = None
    else:
        names_map_file = os.path.join(out_dir, f'{tsv_file}_map')
    rename_data(data_df, names_map_file)
    if target_species != ['all']:
        nb_discarded_species = delete_species(data_df, target_species)
    else:
        nb_discarded_species = 0
    split_location(data_df)
    nb_ambiguous_genes = delete_ambiguous_data(data_df)
    data_df.sort_values(by=['species','scaffold','start'], ascending=True, inplace=True)
    nb_included_genes = delete_included_genes(data_df)
    return data_df,nb_discarded_species,nb_ambiguous_genes,nb_included_genes

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
    for key, family_df in data_df_by_family:
        nb_families += 1
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
        for key, family_df in data_df_by_family:
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
        for key, family_df in data_df_by_family:
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
        for key, species_df in data_df_by_species:
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
target_chr = [rename_object(x) for x in sys.argv[3].split()]
# if 'all', all species are considered
target_species = [rename_object(x) for x in sys.argv[4].split()]
min_on_target = int(sys.argv[5])
min_size = int(sys.argv[6])
if len(sys.argv) >= 8:
    out_dir = sys.argv[7]
else:
    out_dir = None

data_df,nb_ambiguous_genes,nb_included_genes,nb_discarded_species = read_data(
    genes_file, target_species, out_dir, read_seq=read_seq[command]
)
data_df_by_family = group_by_OG(data_df)
selected_families,nb_families,stats = select_families(
    data_df_by_family, min_size, target_chr, min_on_target
)

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
    if len(sys.argv) == 8:
        out_suffix = f'{"_".join(target_chr)}.{"__".join(target_species)}.{min_size}.{min_on_target}.txt'
    else:
        out_suffix = sys.argv[8]
    build_families(data_df_by_family, selected_families, out_dir, out_suffix)
    build_sequences(data_df_by_family, selected_families, out_dir, out_suffix)
    data_df_by_species = group_by_species(data_df)
    build_gene_orders(data_df_by_species, selected_families, out_dir, out_suffix)

    
    
