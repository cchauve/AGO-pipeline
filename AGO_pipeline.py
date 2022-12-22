#!/usr/bin/env python3
# coding: utf-8

''' Running the various steps of the ancestral gene order pipeline '''

import os
import sys
import shutil
import functools
import yaml
from collections import defaultdict
import xml.etree.ElementTree as ET
import subprocess

''' Reading the parameters YAML file '''
def read_parameters(in_file):
    '''
    input:
    in_file: absolute path to YAML file
    output:
    dictionary of parameters
    '''
    class StringConcatinator(yaml.YAMLObject):
        ''' Defining an operator to concatenate YAML fields '''
        yaml_loader = yaml.SafeLoader
        yaml_tag = '!join'
        @classmethod
        def from_yaml(cls, loader, node):
            return functools.reduce(lambda a, b: a.value + b.value, node.value)
    
    with open(in_file, 'r') as file:
        parameters = yaml.safe_load(file)
    # Adding parameters
    families_file = os.path.join(parameters['data_dir'], parameters['families'])
    with open(families_file, 'r') as families:
        run_name = parameters['run_name']
        # Input files and directories
        parameters['main_script_file'] = parameters['main_script']
        parameters['data_genes_dir'] = os.path.join(parameters['data_dir'], parameters['genes_dir'])
        parameters['data_orders_dir'] = os.path.join(parameters['data_dir'], parameters['gene_orders_dir'])
        parameters['data_families'] = os.path.join(parameters['data_dir'], parameters['families'])
        parameters['data_species_tree'] = os.path.join(parameters['data_dir'], parameters['species_tree'])
        parameters['data_extant_species'] = os.path.join(parameters['data_dir'], parameters['species'])
        parameters['data_genes_map'] = os.path.join(parameters['data_dir'], parameters['map'])
        # Tools-independent directories
        parameters['exp_dir'] = os.path.join(parameters['exp_dir_pref'], run_name)
        parameters['scripts_dir'] = os.path.join(parameters['exp_dir'], 'scripts')
        parameters['results_dir'] = os.path.join(parameters['exp_dir'], 'results')
        parameters['log_dir'] = os.path.join(parameters['exp_dir'], 'log')
        parameters['aux_dir'] = os.path.join(parameters['exp_dir'], 'aux')
        # File created during initialization from input
        parameters['active_genes_map'] = os.path.join(parameters['aux_dir'], parameters['map'])
        parameters['active_families'] = os.path.join(parameters['aux_dir'], parameters['families'])
        parameters['active_species_tree'] = os.path.join(parameters['aux_dir'], parameters['species_tree'])
        # Tools-specific directories
        parameters['macse_log_dir'] = os.path.join(parameters['log_dir'], parameters['macse_dir'])
        parameters['macse_results_dir'] = os.path.join(parameters['results_dir'], parameters['macse_dir'])
        parameters['generax_log_dir'] = os.path.join(parameters['log_dir'], parameters['generax_dir'])
        parameters['generax_results_dir'] = os.path.join(parameters['results_dir'], parameters['generax_dir'])
        parameters['generax_aux_dir'] = os.path.join(parameters['aux_dir'], parameters['generax_dir'])
        parameters['treerecs_log_dir'] = os.path.join(parameters['log_dir'], parameters['treerecs_dir'])
        parameters['treerecs_results_dir'] = os.path.join(parameters['results_dir'], parameters['treerecs_dir'])
        parameters['treerecs_aux_dir'] = os.path.join(parameters['aux_dir'], parameters['treerecs_dir'])
        # Tools-specific files
        parameters['macse_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['macse_template'])
        parameters['macse_script_file'] = os.path.join(parameters['scripts_dir'], parameters['macse_script'])
        parameters['macse_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_MACSE.log')
        parameters['macse_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_MACSE.err')
        parameters['generax_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['generax_template'])
        parameters['generax_script_file'] = os.path.join(parameters['scripts_dir'], parameters['generax_script'])
        parameters['generax_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_GeneRax.log')
        parameters['generax_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_GeneRax.err')
        parameters['generax_stats_file'] = os.path.join(parameters['log_dir'], f'{run_name}_GeneRax.csv')
        parameters['generax_species_tree'] = os.path.join(
            parameters['generax_results_dir'], 'species_trees', 'starting_species_tree.newick'
        )
        parameters['treerecs_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['treerecs_template'])
        parameters['treerecs_script_file'] = os.path.join(parameters['scripts_dir'], parameters['treerecs_script'])
        parameters['treerecs_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_Treerecs.log')
        parameters['treerecs_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_Treerecs.err')
        parameters['treerecs_stats_file'] = os.path.join(parameters['log_dir'], f'{run_name}_Treerecs.csv')

    return(parameters)

def init(parameters):
    '''
    output: 
    - creates run-specific directories
    - copies input files that can be modified (families, species tree, genes map) to run-specific directory aux
    '''
    os.makedirs(parameters['exp_dir'], exist_ok=True)
    os.makedirs(parameters['scripts_dir'], exist_ok=True)
    os.makedirs(parameters['results_dir'], exist_ok=True)
    os.makedirs(parameters['log_dir'], exist_ok=True)
    os.makedirs(parameters['aux_dir'], exist_ok=True)
    os.makedirs(parameters['macse_log_dir'], exist_ok=True)
    os.makedirs(parameters['macse_results_dir'], exist_ok=True)
    os.makedirs(parameters['generax_log_dir'], exist_ok=True)
    os.makedirs(parameters['generax_results_dir'], exist_ok=True)
    os.makedirs(parameters['generax_aux_dir'], exist_ok=True)
    os.makedirs(parameters['treerecs_log_dir'], exist_ok=True)
    os.makedirs(parameters['treerecs_results_dir'], exist_ok=True)
    os.makedirs(parameters['treerecs_aux_dir'], exist_ok=True)
    with open(parameters['data_families'], 'r') as f1, open(parameters['active_families'], 'w') as f2:
        for fam in f1.readlines(): f2.write(f'{fam.split()[0]}\n')
    shutil.copy(parameters['data_species_tree'], parameters['active_species_tree'])
    shutil.copy(parameters['data_genes_map'], parameters['active_genes_map'])

# log/err files suffixes
LOG_SUFF = 'log'
ERR_SUFF = 'err'
# Error files separators
SEP_ERR_FAM_ID = ':'
SEP_ERR_FIELDS = '\t'
# Stats files separators
SEP_STATS = ':'
SEP_SPECIES = ','
SEP_STATS_FIELDS = '\t'
# Statistics dictionary keys
STATS_genes = 'genes' # Number of genes
STATS_dup = 'duplications' # Number of duplications
STATS_loss = 'losses' # Number of losses
# XML tags to corresponding statistics keys
STATS_keys = {'leaf': STATS_genes, 'speciation': STATS_genes, 'duplication': STATS_dup, 'loss': STATS_loss}
# Gene maps files separators
SEP_GENE_MAP = '\t'

# Auxiliary functions ----------------------------------------------------------
        
''' List of active families '''
def get_active_families(parameters):
    '''
    output: list(str) list of active families names
    '''
    active_families = [i.rstrip() for i in open(parameters['active_families'], 'r').readlines()]
    return(active_families)

''' Update the active families file, saving a backup file '''
def update_active_families(parameters, families_to_remove, backup_suffix):
    '''
    input:
    - families_to_remove: list(str) list of families to discard from active families
    - backup_file: (str) suffix to add to the backuped active families file
    output:
    nothing done if parameters['active_active_families']_<backup_suffix> does exist
    - modifies parameters['active_families']
    - creates parameters['active_families']_<backup_suffix>
    '''
    backup_file = f'{parameters["active_families"]}_{backup_suffix}'
    if not os.path.isfile(backup_file):
        shutil.copy(active_families, backup_file)
        active_families = [i for i in get_active_families(parameters) if i not in families_to_remove]
        with open(parameters['active_families'], 'w') as f:
            for i in active_families: f.write(f'{i}\n')

''' Creates an error family id ><idx><SEP_ERR_FAM_ID><name> '''
def set_err_family_id(family_idx, family_name):
    return(f'>{family_idx}{SEP_ERR_FAM_ID}{family_name}')            
''' Extracts the family name (str) from an error family index '''
def get_err_family_name(err_family):
    return(err_family.split(SEP_ERR_FAM_ID)[1])
''' Extracts the family idx (str) from an error family index '''
def get_err_family_idx(err_family):
    return(err_family.split(SEP_ERR_FAM_ID)[0][1:])
                
''' Update active families from a step error file '''
def update_active_families_post_step(parameters, err_file, backup_suffix):
    '''
    input:
    - families_to_remove: list(str) list of families to discard from active families
    - err_file: (str) path to an error file
      format: <f1><SEP_ERR_FAM_ID><f2><SEP_ERR_FIELDS><error message> 
      f1: family index in current active families file (int)
      f2: family name (str)
    output:
    - modifies parameters['active_families']
    - creates parameters['active_families']_<backup_suffix>
    '''
    with open(err_file, 'r') as f:
        families_2_remove = [get_err_family_name(l.split(SEP_ERR_FIELDS)[0]) for l in f.readlines()[1:]]
    update_active_families(parameters, families_2_remove, backup_suffix)

''' Update the active species tree '''
def update_active_species_tree(parameters, new_tree_file, backup_suffix):
    '''
    input:
    - new_tree_file: (str) path to new species tree file (newick format)
    - backup_suffix: (str) suffix to add to the backuped active species tree file
    output:
    nothing done if parameters['active_species_tree']_<backup_suffix> does exist
    - copies parameters['active_species_tree'] to parameters['active_species_tree']_<backup_suffix>
    - replaces parameters['active_species_tree'] by new_tree_file
    '''
    backup_file = f'{parameters["active_species_tree"]}_{backup_suffix}'
    if not os.path.isfile(backup_file):
        shutil.copy(parameters['active_species_tree'], backup_file)
        shutil.copy(new_tree_file, parameters['active_species_tree'])

''' Create a list of species '''
def create_extant_species_list(parameters):
    '''
    output: list(str) list of extant species
    '''
    return([species.rstrip() for species in open(parameters['data_extant_species'], 'r').readlines()])


''' Create a dictionary indexed by gene names and mapping to pairs (family,species) '''
def create_genes_map(parameters):
    '''
    output: dict(gene_name(str) -> [family_name(str),species(str)]
    '''
    genes_map = {}
    with open(parameters['active_genes_map'], 'r') as f:
        for gene_data in f.readlines()[1:]:
            gene,family,species = gene_data.rstrip().split(SEP_GENE_MAP)
            genes_map[gene] = [family,species]
    return(genes_map)

''' Create a dictionary indexed by family and mapping to lists of pairs (gene,species) '''
def create_families_map(parameters):
    '''
    output: dict(family_name(str) -> [gene_name(str),species(str)]
    '''
    families_map = defaultdict(list)
    with open(parameters['active_genes_map'], 'r') as f:
        for gene_data in f.readlines()[1:]:
            gene,family,species = gene_data.rstrip().split(SEP_GENE_MAP)
            families_map[family].append([gene,species])
    return(families_map)

''' Generic function to create SLURM scripts from a template '''
def create_slurm_script(parameters, template_key, script_key, patterns, run_script=False):
    '''
    input:
    - template_key: (str) parameters key to path to template SLURM script file
    - script_key: (str) parameters key to path to final SLURM script file
    - patterns: dict(str->str): replacement to create final script from template script
    - run_script: (bool) if True, the script is created
    output:
    - creates file parameters[script_key]
    - jobid: (str/None) SLURM job ID if job is run
    '''
    with open(parameters[template_key], 'r') as f1, open(parameters[script_key], 'w') as f2:
        for line in f1.readlines():
            for in_pattern,out_pattern in patterns.items():
                line = line.replace(in_pattern, out_pattern)
            f2.write(line)
    if run_script:
        jobid = subprocess.check_output(f'jobid=$(sbatch {parameters[script_key]})'+' && echo ${jobid##* }', shell=True)
        return(jobid.decode().rstrip())
    else:
        return(None)

# MACSE functions ----------------------------------------------------------

''' Substitutions in MACSE template file to create MACSE SLURM script '''
def macse_script_patterns(parameters):
    return({
        'XX_slurm_account': parameters['slurm_account'],
        'XX_families_nb': str(len(get_active_families(parameters))),
        'XX_families_file': parameters['active_families'],
        'XX_tools_dir': parameters['tools_dir'],
        'XX_macse_log_dir': parameters['macse_log_dir'],
        'XX_macse_log_pref': parameters['macse_log_pref'],
        'XX_macse_results_dir': parameters['macse_results_dir'],
        'XX_genes_dir': parameters['data_genes_dir'],
        'XX_macse_memory': str(parameters['macse_memory']),
        'XX_macse_time': str(parameters['macse_time'])
    })

''' Creates MACSE SLURM script parameters['macse_script_file'] and runs it if run_script=True '''
def run_macse(parameters, run_script=False):
    '''
    input: run_script: (boolean) run created scripts if True
    output: 
    - creates parameters['macse_script_file']
    - jobid: (str/None) SLURM job ID if job is run
    '''
    return(
        create_slurm_script(
            parameters,
            'macse_template_file',
            'macse_script_file',
            macse_script_patterns(parameters),
            run_script=run_script
        )
    )
    

''' Creates MACSE rerun SLURM scripts for MACSE runs that did not succeed '''
def rerun_macse(parameters, mem, time, run_script=False):
    '''
    input:
    - mem, time: (str) new meory and time parameters for SLURM
    - run_script: (boolean) run created scripts if True
    output: 
    - for each family entry in MACSE error file, >idx<SEP_1>fam 
      creates script file parameters['macse_rerun_pref']_idx.sh
      script is run if run_script=True
    - list(str): list of SLURM job IDs
    '''
    patterns = macse_script_patterns(parameters)
    # Updated patterns replacement
    patterns['XX_macse_memory'] = mem
    patterns['XX_macse_time'] = time
    # Comment array features as each script is for one family
    patterns['FAMILY_ID='] = '#FAMILY_ID='
    patterns['#SBATCH --array'] = '#--array' 
    with open(parameters['macse_err_file'], 'r') as f1:
        # Loop over families with failed runs
        jobs_id = []
        for err_line in f1.readlines()[1:]:
            err_family = err_line.split(SEP_ERR_FIELDS)[0]
            idx,fam = get_err_family_idx(err_family),get_err_family_name(err_family)
            patterns['%a'] = idx
            patterns['${SLURM_ARRAY_TASK_ID}'] = idx
            patterns['${FAMILY_ID}'] = fam
            # Creates a temporary parameters field with script name
            _macse_script_key = '_macse_script'
            parameters[_macse_script_key] = f'{parameters["macse_rerun_pref"]}_{idx}.sh'
            jobid = (
                create_slurm_script(
                    parameters,
                    'macse_template_file',
                    _macse_script_key,
                    patterns,
                    run_script=run_script
                )
            )
            if jobid is not None: jobs_id.append(jobid)
            parameters.pop(_macse_script_key)
    return(jobs_id)

'''  Check the results of MACSE, creating a log file and an error file '''
def check_macse(parameters):
    '''
    output:
    creates parameters['macse_log_file'] and parameters['macse_err_file']
    format: one line per family
    parameters['macse_err_file'] contains only entries for failed families
    fam_id<SEP_ERR_FIELDS>error message
    parameters['macse_log_file'] contains entries for all families
    fam_id<SEP_ERR_FIELDS>ERROR/SUCCESS<SEP_ERR_FIELDS>error/success message
    '''
    active_families = get_active_families(parameters)
    with open(parameters['macse_log_file'], 'w') as log_file, open(parameters['macse_err_file'], 'w') as err_file:
        for idx in range(1,len(active_families)+1):
            fam_id = set_err_family_id(idx, active_families[idx-1])
            idx_log_pref = os.path.join(parameters['macse_log_dir'], f'{parameters["macse_log_pref"]}_{idx}')
            idx_log_file,idx_err_file = f'{idx_log_pref}.{LOG_SUFF}',f'{idx_log_pref}.{ERR_SUFF}'
            if not (os.path.exists(idx_log_file) and os.path.exists(idx_err_file)):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", "missing SLURM log"])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "missing SLURM log"])}')
                continue
            with open(idx_log_file, 'r') as idx_log_file, open(idx_err_file, 'r') as idx_err_file:
                log_last,err_last = idx_log_file.readlines()[-1].rstrip(),idx_err_file.readlines()[-1].rstrip()
            if log_last != 'PROGRAM HAS FINISHED SUCCESSFULLY':
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", log_last])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, err_last])}')
                continue
            log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "SUCCESS", log_last])}')
        return(None)

''' Check the results of MACSE through a SLURM script '''
def check_macse_slurm(parameters):
    ''' Same output than function check_macse plus SLURM job ID'''
    macse_check_script = os.path.join(parameters['scripts_dir'], parameters['macse_script'].replace('.sh', '_check.sh'))
    with open(macse_check_script, 'w') as check_script:
        check_script.write('#!/bin/bash')
        check_script.write('\n')
        check_script.write(f'\n#SBATCH --account={parameters["slurm_account"]}')
        check_script.write(f'\n#SBATCH --output={parameters["macse_log_file"].replace(".log","_check.log")}')
        check_script.write(f'\n#SBATCH --output={parameters["macse_err_file"].replace(".err","_check.log")}')
        check_script.write('\n')
        check_script.write(f'\npython {parameters["main_script"]} check_macse')
    jobid = subprocess.check_output(f'jobid=$(sbatch {macse_check_script})'+' && echo ${jobid##* }', shell=True)
    return(jobid.decode().rstrip())
    

# Reconciliations ----------------------------------------------------------------

def read_RecPhyloXML(in_file):
    ''' 
    Read a recPhyloXML file and returns a dictionary indexed by species
    and for each containing a dictionary recording number of genes,  of duplications
    and of losses with the keys STATS_genes, STATS_dup, STATS_loss
    '''

    def get_tag(node):
        ''' Returns the tag of a node without its prefix {...} '''
        return(node.tag.rpartition('}')[2])
    def get_prefix(node):
        ''' Returns the prefix of tag '''
        pref = node.tag.rpartition("}")[0]
        if len(pref)>0: return(pref+'}')
        else: return(pref)
    def get_text(node):
        ''' Returns the text associated to a node; assumption '''
        if node.text is not None: return((node.text).strip())
        else: return('')
    def get_name(node):
        ''' Returns the name of a clade node; assumption: any clade node has a name '''
        return(get_text(node.find(f'{tag_pref}name')))
    def get_species(node):
        ''' Returns the species of a eventRec node '''
        return(node.get(f'speciesLocation'))
        
    def parse_spTree(root):
        ''' 
        input: XML root node
        output: dict(species name(str) -> species name of sibling species (str/None))
        '''
        def parse_clade_recursive(node, siblings):
            ''' Assumption: node is tagged <clade> '''
            children = node.findall(f'{tag_pref}clade')
            # Updating siblings dictionary
            if len(children) == 2:
                siblings[get_name(children[0])] = get_name(children[1])
                siblings[get_name(children[1])] = get_name(children[0])
            # Recursive calls
            for child in children: parse_clade_recursive(child, siblings)
        siblings = {get_name(root): None}
        parse_clade_recursive(root, siblings)
        return(siblings)

    def parse_recGeneTree(root, siblings):
        ''' 
        input: XML root node
        output: dict(species name(str) -> dict(STATS_genes: int, STATS_dup: int, STATS_loss: int))
        '''
        def parse_clade_recursive(node, stats):
            # Reconciliation event (possibly more than one)
            events = node.find(f'{tag_pref}eventsRec')
            # If more than one, then speciationLoss ended by last event
            # Loop on speciationLoss events to add a loss to the sibling species
            for event in events[1:][::-1]: stats[siblings[get_species(event)]][STATS_loss] += 1
            # Last event
            last_event_tag,last_event_species = get_tag(events[-1]),get_species(events[-1])
            stats[last_event_species][STATS_keys[last_event_tag]] += 1
            # Recursive calls
            for child in node.findall(f'{tag_pref}clade'): parse_clade_recursive(child, stats)
        stats = {sp:{STATS_genes: 0, STATS_dup: 0, STATS_loss: 0} for sp in siblings.keys()}
        parse_clade_recursive(root, stats)
        return(stats)

    root = ET.parse(in_file).getroot()
    tag_pref = get_prefix(root)
    siblings = parse_spTree(
        root.find(f'{tag_pref}spTree').find(f'{tag_pref}phylogeny').find(f'{tag_pref}clade')
    )
    recStats = parse_recGeneTree(
        root.find(f'{tag_pref}recGeneTree').find(f'{tag_pref}phylogeny').find(f'{tag_pref}clade'),
        siblings
    )
    return(recStats)

''' Computes statistics of reconciliations from a log file and writes them in a csv file '''
def stats_reconciliation(parameters, log_file_key, stats_file_key):
    '''
    output:
    creates parameters[stats_file_key] 
    Format: csv with separator SEP_STATS_FIELDS and a header line
    '''
    with open(parameters[log_file_key], 'r') as log_file:
        statistics = {}
        for family_log in log_file.readlines()[1:]:
            family_data = family_log.rstrip().split(SEP_ERR_FIELDS)
            if family_data[1] != 'ERROR': family_stats = family_data[2].split(SEP_SPECIES)
            for stat in family_stats:
                species,genes,dup,loss = stat.split(SEP_STATS)
                if species not in statistics.keys():
                    statistics[species] = {STATS_genes: 0, STATS_dup: 0, STATS_loss: 0}
                statistics[species][STATS_genes] += int(genes)
                statistics[species][STATS_dup] += int(dup)
                statistics[species][STATS_loss] += int(loss)
    with open(parameters[stats_file_key], 'w') as stats_file:
        stats_file.write(SEP_STATS_FIELDS.join(['species', STATS_genes, STATS_dup, STATS_loss]))
        for species,stats in statistics.items():
            stats_str = [str(species), str(stats[STATS_genes]), str(stats[STATS_dup]), str(stats[STATS_loss])]
            stats_file.write(f'\n{SEP_STATS_FIELDS.join(stats_str)}')
    return(None)

''' Computes statistics of reconciliations through a SLURM script '''
def stats_reconciliation_slurm(parameters, log_file_key, err_file_key, script_key, command):
    ''' Same output than function stats_reconciliation '''
    stats_script = os.path.join(parameters['scripts_dir'], parameters[script_key].replace('.sh', '_stats.sh'))
    with open(generax_stats_script, 'w') as stats_script:
        stats_script.write('#!/bin/bash')
        stats_script.write('\n')
        stats_script.write(f'\n#SBATCH --account={parameters["slurm_account"]}')
        stats_script.write(f'\n#SBATCH --output={parameters[log_file_key].replace(".log","_stats.log")}')
        stats_script.write(f'\n#SBATCH --output={parameters[err_file_key].replace(".err","_stats.log")}')
        stats_script.write('\n')
        stats_script.write(f'\npython {parameters["main_script"]} {command}')
    jobid = subprocess.check_output(f'jobid=$(sbatch {stats_script})'+' && echo ${jobid##* }', shell=True)
    return(jobid.decode().rstrip())
    
# GeneRax functions ----------------------------------------------------------
                        
'''  Create GeneRax input files: one families file, one map file per family '''
def aux_generax(parameters):
    '''
    output:
    - creates file parameters['generax_aux_dir']/parameters['generax_families']
    - creates files parameters['generax_aux_dir']/parameters['generax_families']_<familyname> for 
      each active family
    File formats are the ones required by GeneRax
    '''
    generax_family_file = os.path.join(parameters['generax_aux_dir'], parameters['generax_families'])
    families_map = create_families_map(parameters)
    active_families = get_active_families(parameters)
    with open(generax_family_file, 'w') as f1:
        f1.write('[FAMILIES]')
        for idx in active_families:
            alignment_file = os.path.join(parameters['macse_results_dir'], f'{idx}_{parameters["generax_seq"]}.fasta')
            map_file = f'{generax_family_file}_{idx}'
            f1.write(f'\n- {idx}')
            f1.write(f'\nalignment = {alignment_file}')
            f1.write(f'\nmapping = {map_file}')
            f1.write(f'\nsubst_model = {parameters["generax_subst"]}')
            with open(map_file, 'w') as f2:
                f2.write('\n'.join([f'{gene}\t{species}' for [gene,species] in families_map[idx]]))
            
''' Substitutions in GeneRax template file to create GeneRax SLURM script '''
def generax_script_patterns(parameters):
    return(
        {
            'XX_slurm_account': parameters['slurm_account'],
            'XX_families_nb': str(len(get_active_families(parameters))),
            'XX_families_file': parameters['active_families'],
            'XX_species_tree': parameters['active_species_tree'],
            'XX_tools_dir': parameters['tools_dir'],
            'XX_generax_ntasks': parameters['generax_ntasks'],
            'XX_generax_ncores': parameters['generax_ncores'],
            'XX_generax_memory': parameters['generax_memory'],
            'XX_generax_time': str(parameters['generax_time']),
            'XX_generax_seq': parameters['generax_seq'],
            'XX_generax_families': parameters['generax_families'],
            'XX_generax_options': parameters['generax_options'],
            'XX_generax_seed': str(parameters['generax_seed']),
            'XX_generax_model': parameters['generax_model'],
            'XX_generax_strategy': parameters['generax_strategy'],
            'XX_generax_aux_dir': parameters['generax_aux_dir'],
            'XX_generax_log_dir': parameters['generax_log_dir'],
            'XX_generax_log_pref': parameters['generax_log_pref'],
            'XX_generax_results_dir': parameters['generax_results_dir']
        }
    )

''' Create a GeneRax SLURM script '''
def run_generax(parameters, run_script=False):
    '''
    input: run_script: (boolean) run created scripts if True
    output: 
    - creates parameters['generax_script_file']
    - jobid: (str/None) SLURM job ID if job is run
    '''
    return(
        create_slurm_script(
            parameters,
            'generax_template_file',
            'generax_script_file',
            generax_script_patterns(parameters),
            run_script=run_script
        )
    )

'''  Check the results of GeneRax, creating a log file and an error file '''
def check_generax(parameters):
    '''
    output:
    creates parameters['generax_log_file'] and parameters['generax_err_file']
    format: one line per family
    parameters['generax_err_file'] contains only entries for failed families
    fam_id<SEP_ERR_FIELDS>error message
    parameters['generax_log_file'] contains entries for all families
    fam_id<SEP_ERR_FIELDS>ERROR/SUCCESS<SEP_ERR_FIELDS>error/success message
    '''
    in_generax_log_file = os.path.join(parameters['generax_log_dir'], f'{parameters["generax_log_pref"]}.{LOG_SUFF}')
    active_families,error_families = get_active_families(parameters),{}
    with open(in_generax_log_file, 'r') as log_file:
        err_lines = [l.rstrip().split(':') for l in log_file.readlines() if l.startswith('Error in family')]
        for err_line_header,err_line_msg in err_lines:
            error_families[err_line_header.split()[3]] = err_line_error.rstrip()
    with open(parameters['generax_log_file'], 'w') as log_file, open(parameters['generax_err_file'], 'w') as err_file:
        log_file.write('#species:genes:duplications:losses')
        for idx in range(1,len(active_families)+1):            
            family = active_families[idx-1]
            fam_id = set_err_family_id(idx, family)
            if family in error_families.keys():
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", error_families[family]])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, error_families[family]])}')
                continue
            gene_tree = os.path.join(parameters['generax_results_dir'], 'results', family, 'geneTree.newick')
            rec_tree = os.path.join(parameters['generax_results_dir'], 'reconciliations', f'{family}_reconciliated.xml')
            if not (os.path.isfile(gene_tree) and os.path.isfile(rec_tree)):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", "missing tree"])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "missing tree"])}')
                continue
            stats_str = SEP_SPECIES.join([
                SEP_STATS.join([sp]+[str(stat) for stat in stats.values()])
                for sp,stats in read_RecPhyloXML(rec_tree).items()
            ])
            log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "SUCCESS", stats_str])}')
    return(None)

''' Check the results of GeneRax through a SLURM script '''
def check_generax_slurm(parameters):
    ''' Same output than function check_generax plus SLURM job ID '''
    generax_check_script = os.path.join(parameters['scripts_dir'], parameters['generax_script'].replace('.sh', '_check.sh'))
    with open(generax_check_script, 'w') as check_script:
        check_script.write('#!/bin/bash')
        check_script.write('\n')
        check_script.write(f'\n#SBATCH --account={parameters["slurm_account"]}')
        check_script.write(f'\n#SBATCH --output={parameters["generax_log_file"].replace(".log","_check.log")}')
        check_script.write(f'\n#SBATCH --output={parameters["generax_err_file"].replace(".err","_check.log")}')
        check_script.write('\n')
        check_script.write(f'\npython {parameters["main_script"]} check_generax')
    jobid = subprocess.check_output(f'jobid=$(sbatch {generax_check_script})'+' && echo ${jobid##* }', shell=True)
    return(jobid.decode().rstrip())

''' Computes statistics post GeneRax '''
def stats_generax(parameters):
    ''' output: creates parameters['generax_stats_file'] '''
    return(stats_reconciliation(parameters, 'generax_log_file', 'generax_stats_file'))

''' Computes statistics post GeneRax through a SLURM script '''
def stats_generax_slurm(parameters):
    ''' Same output than function stats_generax '''
    return(stats_reconciliation_slurm(parameters, "generax_log_file", "generax_err_file", 'generax_script', 'stats_generax'))

# Treerecs functions ----------------------------------------------------------

'''  Create Treerecs alignment files, one per family '''
def aux_treerecs(parameters):
    '''
    output:
    - creates file parameters['treerecs_aux_dir']/parameters['generax_families']_<familyname>
      for each active family
    File formats are the ones required by Treerecs: sequence substitution model\nalignment file path
    '''
    active_families = get_active_families(parameters)
    for idx in active_families:
        treerecs_family_file = os.path.join(
            parameters['treerecs_aux_dir'], f'{parameters["generax_families"]}_{idx}'
        )
        alignment_file = os.path.join(
            parameters['macse_results_dir'], f'{idx}_{parameters["generax_seq"]}.fasta'
        )
        with open(treerecs_family_file, 'w') as f:
            f.write(f'# {idx}\n{parameters["treerecs_subst"]}\n{alignment_file}')

''' Substitutions in Treerecs template file to create GeneRax SLURM script '''
def treerecs_script_patterns(parameters):
    return(
        {
            'XX_slurm_account': parameters['slurm_account'],
            'XX_families_nb': str(len(get_active_families(parameters))),
            'XX_families_file': parameters['active_families'],
            'XX_species_tree': parameters['active_species_tree'],
            'XX_tools_dir': parameters['tools_dir'],
            'XX_generax_results_dir': parameters['generax_results_dir'],
            'XX_treerecs_memory': parameters['treerecs_memory'],
            'XX_treerecs_time': str(parameters['treerecs_time']),
            'XX_treerecs_options': parameters['treerecs_options'],
            'XX_treerecs_map_file_prefix': os.path.join(parameters['generax_aux_dir'], parameters['generax_families']),
            'XX_treerecs_alg_file_prefix': os.path.join(parameters['treerecs_aux_dir'], parameters['generax_families']),
            'XX_treerecs_log_dir': parameters['treerecs_log_dir'],
            'XX_treerecs_log_pref': parameters['treerecs_log_pref'],
            'XX_treerecs_results_dir': parameters['treerecs_results_dir']
        }
    )

''' Create a GeneRax SLURM script '''
def run_treerecs(parameters, run_script=False):
    '''
    input: run_script: (boolean) run created scripts if True
    output: 
    - creates parameters['treerecs_script_file']
    - jobid: (str/None) SLURM job ID if job is run
    '''
    return(
        create_slurm_script(
            parameters,
            'treerecs_template_file',
            'treerecs_script_file',
            treerecs_script_patterns(parameters),
            run_script=run_script
        )
    )

'''  Check the results of Treerecs, creating a log file and an error file '''
def check_treerecs(parameters):
    '''
    output:
    creates parameters['treerecs_log_file'] and parameters['treerecs_err_file']
    format: one line per family
    parameters['treerecs_err_file'] contains only entries for failed families
    fam_id<SEP_ERR_FIELDS>error message
    parameters['treerecs_log_file'] contains entries for all families
    fam_id<SEP_ERR_FIELDS>ERROR/SUCCESS<SEP_ERR_FIELDS>error message/reconciliation stats
    '''
    active_families = get_active_families(parameters)
    with open(parameters['treerecs_log_file'], 'w') as log_file, open(parameters['treerecs__err_file'], 'w') as err_file:
        for idx in range(1,len(active_families)+1):
            fam_id = set_err_family_id(idx, active_families[idx-1])
            idx_log_pref = os.path.join(parameters['treerecs_log_dir'], f'{parameters["treerecs_log_pref"]}_{idx}')
            idx_log_file,idx_err_file = f'{idx_log_pref}.{LOG_SUFF}',f'{idx_log_pref}.{ERR_SUFF}'
            if not (os.path.exists(idx_log_file) and os.path.exists(idx_err_file)):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", "missing SLURM log"])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "missing SLURM log"])}')
                continue
            with open(idx_log_file, 'r') as idx_log_file, open(idx_err_file, 'r') as idx_err_file:
                log_last,err_last = idx_log_file.readlines()[-1].rstrip(),idx_err_file.readlines()[-1].rstrip()
            if not log_last.startswith('Total elapsed time'):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", log_last])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, err_last])}')
                continue
            rec_tree = os.path.join(parameters['treerecs_results_dir'], f'{family}_reconciliated.nhx_recs.recphylo.xml')
            if not os.path.isfile(rec_tree):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "ERROR", "missing tree"])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "missing tree"])}')
                continue
            stats_str = SEP_SPECIES.join([
                SEP_STATS.join([sp]+[str(stat) for stat in stats.values()])
                for sp,stats in read_RecPhyloXML(rec_tree).items()
            ])
            log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "SUCCESS", stats_str])}')
        return(None)

''' Check the results of Treerecs through a SLURM script '''
def check_treerecs_slurm(parameters):
    ''' Same output than function check_treerecs plus SLURM job ID'''
    treerecs_check_script = os.path.join(parameters['scripts_dir'], parameters['treerecs_script'].replace('.sh', '_check.sh'))
    with open(treerecs_check_script, 'w') as check_script:
        check_script.write('#!/bin/bash')
        check_script.write('\n')
        check_script.write(f'\n#SBATCH --account={parameters["slurm_account"]}')
        check_script.write(f'\n#SBATCH --output={parameters["treerecs_log_file"].replace(".log","_check.log")}')
        check_script.write(f'\n#SBATCH --output={parameters["treerecs_err_file"].replace(".err","_check.log")}')
        check_script.write('\n')
        check_script.write(f'\npython {parameters["main_script"]} check_macse')
    jobid = subprocess.check_output(f'jobid=$(sbatch {treerecs_check_script})'+' && echo ${jobid##* }', shell=True)
    return(jobid.decode().rstrip())

''' Computes statistics post Treerecs '''
def stats_treerecs(parameters):
    ''' output: creates parameters['treerecs_stats_file'] '''
    return(stats_reconciliation(parameters, 'treerecs_log_file', 'treerecs_stats_file'))

''' Computes statistics post GeneRax through a SLURM script '''
def stats_treerecs_slurm(parameters):
    ''' Same output than function stats_treerecs '''
    return(stats_reconciliation_slurm(parameters, "treerecs_log_file", "treerecs_err_file", 'treerecs_script', 'stats_treerecs'))


# MAIN --------------------------------------------------------------------------

def main():
    parameters_file = sys.argv[1]
    parameters = read_parameters(parameters_file)
    command = sys.argv[2]

    TRUE_LIST = ['y', 'yes', 'Y', 'Yes', 'YES', '1', 'true', 'True', 'TRUE']

    if command == 'init':
        init(parameters)
    elif command == 'run_macse':
        if len(sys.argv) == 4: run_val = (sys.argv[3] in TRUE_LIST)
        else: run_val = False
        run_macse_jobid = run_macse(parameters, run_script=run_val)
    elif command == 'check_macse':
        if len(sys.argv) == 4: run_slurm = (sys.argv[3] in TRUE_LIST)
        if run_slurm: check_macse_jobid = check_macse_slurm(parameters)
        else: check_macse_jobid = check_macse(parameters)
    elif command == 'rerun_macse':
        mem = sys.argv[3]
        time = sys.argv[4]
        if len(sys.argv) == 6: run_val = (sys.argv[5] in TRUE_LIST)
        else: run_val = False
        rerun_macse_jobsid = rerun_macse(parameters, mem, time, run_script=run_val)
    elif command == 'update_post_macse':
        backup_suffix = sys.argv[3]
        update_active_families_post_step(parameters, parameters['macse_err_file'], backup_suffix)
    elif command == 'aux_generax':
        aux_generax(parameters)
    elif command == 'run_generax':
        if len(sys.argv) == 4: run_val = (sys.argv[3] in TRUE_LIST)
        else: run_val = False
        run_generax_jobid = run_generax(parameters, run_script=run_val)
    elif command == 'check_generax':
        if len(sys.argv) == 4: run_slurm = (sys.argv[3] in TRUE_LIST)
        if run_slurm: check_generax_jobid = check_generax_slurm(parameters)
        else: check_generax_jobid = check_generax(parameters)
    elif command == 'stats_generax':
        if len(sys.argv) == 4: run_slurm = (sys.argv[3] in TRUE_LIST)
        if run_slurm: stats_generax_jobid = stats_generax_slurm(parameters)
        else: stats_generax_jobid = stats_generax(parameters)
    elif command == 'update_post_generax':
        backup_suffix = sys.argv[3]
        update_active_families_post_step(parameters, parameters['generax_err_file'], backup_suffix)
        update_active_species_tree(parameters, parameters['generax_species_tree'], backup_suffix)
    elif command == 'aux_treerecs':
        aux_treerecs(parameters)
    elif command == 'run_treerecs':
        if len(sys.argv) == 4: run_val = (sys.argv[3] in TRUE_LIST)
        else: run_val = False
        run_treerecs_jobid = run_treerecs(parameters, run_script=run_val)
    elif command == 'check_treerecs':
        if len(sys.argv) == 4: run_slurm = (sys.argv[3] in TRUE_LIST)
        if run_slurm: check_treerecs_jobid = check_treerecs_slurm(parameters)
        else: check_treerecs_jobid = check_treerecs(parameters)
    elif command == 'stats_treerecs':
        if len(sys.argv) == 4: run_slurm = (sys.argv[3] in TRUE_LIST)
        if run_slurm: stats_treerecs_jobid = stats_treerecs_slurm(parameters)
        else: stats_treerecs_jobid = stats_treerecs(parameters)

           
if __name__ == "__main__":
    main()
