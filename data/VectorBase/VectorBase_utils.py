#!/usr/bin/env python3
# coding: utf-8


'''Pre-processing VectorBase data'''

import os
import sys
import pandas as pd
import argparse

'''
Expected data format.
A single tab-separated files with one line per gene and fields:
- Gene ID: gene
- Organism: species name
- Genomic Location (Gene): assembly_chromosome:start..end:strand where strand is +/-
- Chromosome: chromosome or scaffold
- Ortholog Group: family ID
- Gene Type:
- Is Pseudo:
- Predicted Protein Sequence: protein sequence
Assumption: only the longest transcript is kept per gene
'''

def rename_object(name, sep=''):
    ''' Rename an object by deleting all non alphanumeric characters '''
    return sep.join(filter(str.isalnum, name))

''' Reading original data into a DataFrame '''

def rename_columns(data_df, read_seq=False):
    data_df.rename(
        columns={
            'Gene ID': 'gene',
            'Organism': 'species',
            'Genomic Location (Gene)': 'coordinates',
            'Chromosome': 'chromosome',
            'Ortholog Group': 'family',
            'Gene Type': 'gene_type',
            'Is Pseudo': 'pseudogene'
        },
        inplace=True
    )
    if read_seq:
        data_df.rename(
            columns={'Predicted Protein Sequence': 'sequence'},
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
    return len(discarded_species)

def delete_chromosomes(data_df, target_chr):
    all_chr = data_df['chromosome'].unique()
    discarded_chr = [s for s in all_chr if s not in target_chr]
    nb_genes_before = len(data_df.index)
    data_df.drop(data_df[data_df['chromosome'].isin(discarded_chr)].index, inplace = True)
    nb_genes_after = len(data_df.index)
    return (nb_genes_before-nb_genes_after)

def delete_ambiguous_data(data_df):
    nb_rows_before = len(data_df.index)
    data_df.drop(data_df[data_df['family'] == 'NA'].index, inplace = True)
    data_df.drop(data_df[data_df['chromosome'] == 'UNKN'].index, inplace = True)
    data_df.drop(data_df[data_df['chromosome'] == 'Yunplaced'].index, inplace = True)
    nb_rows_after = len(data_df.index)
    nb_discarded_rows = nb_rows_before - nb_rows_after
    return nb_discarded_rows

def delete_missing_sequences(data_df):
    nb_rows_before = len(data_df.index)
    data_df.drop(data_df[data_df['sequence'].isna()].index, inplace = True)
    nb_rows_after = len(data_df.index)
    nb_discarded_rows = nb_rows_before - nb_rows_after
    return nb_discarded_rows

def delete_noncoding_genes(data_df):
    nb_rows_before = len(data_df.index)
    data_df.drop(data_df[~data_df['gene_type'].isin(['protein coding gene'])].index, inplace = True)
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

def read_data(tsv_file, target_species, target_chr, create_map=False, read_seq=False):
    columns = [
        'Gene ID', 'Organism', 'Genomic Location (Gene)', 'Chromosome',
        'Ortholog Group', 'Gene Type', 'Is Pseudo'
    ]
    if read_seq:
        columns.append('Predicted Protein Sequence')
    data_df = pd.read_table(tsv_file, delimiter='\t', usecols=columns)
    rename_columns(data_df, read_seq=read_seq)
    if create_map:
        names_map_file = f'{tsv_file}_map'
    else:
        names_map_file = None
    rename_data(data_df, names_map_file)
    split_location(data_df)
    data_df.sort_values(by=['species','scaffold','start'], ascending=True, inplace=True)
    stats = {}
    if target_species != ['all']:
        _ = delete_species(data_df, target_species)
    if target_chr != ['all']:
        stats['nb_off_target_genes'] = delete_chromosomes(data_df, target_chr)
    #stats['nb_included_genes'] = delete_included_genes(data_df)
    #stats['nb_missing_sequences'] = delete_missing_sequences(data_df)
    return data_df,stats

def group_by_OG(data_df):
    return data_df.groupby(['family'])

def group_by_species(data_df):
    return data_df.groupby(['species'])

def group_by_gene_type(data_df):
    return data_df.groupby(['gene_type'])

def get_gene_id(df_row, sep='|'):
    gene = df_row['gene']
    species = df_row['species']
    return f'{species}{sep}{gene}'

def build_sequences(data_df_by_key, key, out_dir, suffix):
    sequences_dir = os.path.join(out_dir,f'sequences_{suffix}')
    os.makedirs(sequences_dir, exist_ok=True)
    sequences_file = os.path.join(out_dir,f'sequences_{suffix}.txt')
    with open(sequences_file, 'w') as out_file:
        for key_id,_ in data_df_by_key:
            key_df = data_df_by_key.get_group(key_id)
            fasta_file = os.path.join(sequences_dir,f'{key_id}.fasta')
            with open(fasta_file, 'w') as out_fasta:
                for _,gene in key_df.iterrows():
                    gene_id = get_gene_id(gene)
                    sequence = gene['sequence']
                    out_fasta.write(f'>{gene_id}\n{sequence}\n')
                out_file.write(f'{key_id}\t{fasta_file}\n')

def build_sequences_families(data_df_by_family, out_dir, suffix):
    build_sequences(data_df_by_family, 'family', out_dir, suffix)

def build_sequences_species(data_df_by_species, out_dir, suffix):
    build_sequences(data_df_by_species, 'species', out_dir, suffix)


''' Computing statistics about data '''
def cmd_stats(in_file_name, out_file_name, species_list, chr_list):
    data_df,_ = read_data(in_file_name, species_list, ['all'], create_map=True, read_seq=True)
    data_df_by_species = group_by_species(data_df)
    data_stats_by_species = {}
    with open(out_file_name, 'w') as out_file:
        for species,species_data in data_df_by_species:
            data_stats_by_species[species] = {}
            species_data_df = data_df_by_species.get_group(species)
            species_data_df.sort_values(by=['species','scaffold','start'], ascending=True, inplace=True)
            data_stats_by_species[species]['nb_genes'] = len(species_data_df.index)
            data_stats_by_species[species]['nb_included_genes'] = delete_included_genes(species_data_df)
            species_data_df_by_gene_type = group_by_gene_type(species_data_df)
            gene_types = []
            for gene_type,species_data_gene_type in species_data_df_by_gene_type:
                renamed_gene_type = gene_type.replace(' ', '_')
                gene_types.append(f'nb_{renamed_gene_type}')
                data_stats_by_species[species][f'nb_{renamed_gene_type}'] = len(species_data_df_by_gene_type.get_group(gene_type).index)
            data_stats_by_species[species]['nb_noncoding_genes'] = delete_noncoding_genes(species_data_df)
            data_stats_by_species[species]['nb_missing_coding_seq'] = delete_missing_sequences(species_data_df)
            data_stats_by_species[species]['nb_off_target_genes'] = delete_chromosomes(species_data_df, chr_list)
            data_stats_by_species[species]['nb_kept_genes'] = len(species_data_df.index)
            for stats_key in ['nb_genes','nb_included_genes'] + gene_types + ['nb_noncoding_genes', 'nb_missing_coding_seq', 'nb_off_target_genes', 'nb_kept_genes']:
                stats_value = data_stats_by_species[species][stats_key]
                out_file.write(f'{species}.{stats_key}\t{stats_value}\n')

''' Creating a genomes dataset '''
def cmd_genomes(in_file_name, species_list, chr_list, suffix, out_dir):
    data_df,_ = read_data(in_file_name, species_list, ['all'], create_map=True, read_seq=True)
    stats = {}
    data_df.sort_values(by=['species','scaffold','start'], ascending=True, inplace=True)
    stats['nb_genes'] = len(data_df.index)
    stats['nb_included_genes'] = delete_included_genes(data_df)
    stats['nb_noncoding_genes'] = delete_noncoding_genes(data_df)
    stats['nb_missing_coding_seq'] = delete_missing_sequences(data_df)
    if chr_list != ['all']:
        stats['nb_off_target_genes'] = delete_chromosomes(data_df, chr_list)
    stats['nb_kept_genes'] = len(data_df.index)
    data_df_by_species = group_by_species(data_df)
    build_sequences(data_df_by_species, 'species', out_dir, suffix)
    return stats
            
''' Main '''

def main():
    parser = argparse.ArgumentParser(description='VectorBase data.')
    subparsers = parser.add_subparsers(help='sub-command help')
    # stats command arguments
    stats_parser = subparsers.add_parser('stats')
    stats_parser.set_defaults(cmd='stats')
    stats_parser.add_argument('input', type=str, help='Input TSV file')
    stats_parser.add_argument('output', type=str, help='Output TSV file')
    stats_parser.add_argument('species', type=str, help='Species list')
    stats_parser.add_argument('chr', type=str, help='Target chromosomes')
    # genomes command arguments
    genomes_parser = subparsers.add_parser('genomes')
    genomes_parser.set_defaults(cmd='genomes')
    genomes_parser.add_argument('input', type=str, help='Input TSV file')
    genomes_parser.add_argument('species', type=str, help='Species list')
    genomes_parser.add_argument('chr', type=str, help='Target chromosomes')
    genomes_parser.add_argument('suffix', type=str, help='Dataset suffix')
    genomes_parser.add_argument('out_dir', type=str, help='Output directory')
    
    args = parser.parse_args()

    if args.cmd == 'stats':
        cmd_stats(args.input, args.output, args.species.split(), args.chr.split())
    elif args.cmd == 'genomes':
        stats = cmd_genomes(args.input, args.species.split(), args.chr.split(), args.suffix, args.out_dir)
        for stats_key,stats_value in stats.items():
            print(f'{stats_key}\t{stats_value}')

if __name__ == "__main__":
    main()

