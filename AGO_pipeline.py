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
import ete3
import subprocess

''' Constants: should be in the yaml file with default values '''

# log/err files suffixes
LOG_SUFF = 'log'
ERR_SUFF = 'err'
CSV_SUFF = 'csv'
XML_SUFF = 'xml'
REC_SUFF = 'recphyloxml.xml'
NHX_SUFF = 'nhx'
# log messages
SUCCESS_MSG = 'SUCCESS'
ERROR_MSG = 'ERROR'
# Error files separators
SEP_ERR_FAM_ID = ':'
SEP_ERR_FIELDS = '\t'
# Gene order/adjacency separator
SEP_ORDER = '\t'
SEP_ADJ = ' '
# Stats files separators
SEP_STATS = ':'
SEP_SPECIES = ','
SEP_STATS_FIELDS = '\t'
# Statistics dictionary keys
STATS_genes = 'genes' # Number of genes
STATS_dup = 'duplications' # Number of duplications
STATS_loss = 'losses' # Number of losses
# XML tags to corresponding statistics keys
STATS_xmlkeys = {'leaf': STATS_genes, 'speciation': STATS_genes, 'duplication': STATS_dup, 'loss': STATS_loss}
STATS_keys = [STATS_genes, STATS_dup, STATS_loss]
# Gene maps files separators
SEP_GENE_MAP = '\t'
# DeCoSTAR separator
SEP_DECOSTAR = '|'
# SPP-DCJ separator
SEP_SPPDCJ_FIELDS = '\t'
SEP_SPPDCJ = '_'
# Empty file string
EMPTY_FILE = 'EMPTY FILE'

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
        parameters['data_gene_orders_dir'] = os.path.join(parameters['data_dir'], parameters['gene_orders_dir'])
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
        parameters['active_gene_orders_dir'] = os.path.join(parameters['aux_dir'], parameters['gene_orders_dir'])
        # Tools-specific directories
        parameters['macse_log_dir'] = os.path.join(parameters['log_dir'], parameters['macse_dir'])
        parameters['macse_results_dir'] = os.path.join(parameters['results_dir'], parameters['macse_dir'])
        parameters['generax_log_dir'] = os.path.join(parameters['log_dir'], parameters['generax_dir'])
        parameters['generax_results_dir'] = os.path.join(parameters['results_dir'], parameters['generax_dir'])
        parameters['generax_aux_dir'] = os.path.join(parameters['aux_dir'], parameters['generax_dir'])
        parameters['decostar_log_dir'] = os.path.join(parameters['log_dir'], parameters['decostar_dir'])
        parameters['decostar_results_dir'] = os.path.join(parameters['results_dir'], parameters['decostar_dir'])
        parameters['decostar_aux_dir'] = os.path.join(parameters['aux_dir'], parameters['decostar_dir'])
        parameters['sppdcj_log_dir'] = os.path.join(parameters['log_dir'], parameters['sppdcj_dir'])
        parameters['sppdcj_results_dir'] = os.path.join(parameters['results_dir'], parameters['sppdcj_dir'])
        parameters['sppdcj_aux_dir'] = os.path.join(parameters['aux_dir'], parameters['sppdcj_dir'])
        # Tools-specific files
        MACSE = parameters['macse_pref']
        GENERAX = parameters['generax_pref']
        DECOSTAR = parameters['decostar_pref']
        SPPDCJ = parameters['sppdcj_pref']
        parameters['macse_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['macse_template'])
        parameters['macse_script_file'] = os.path.join(parameters['scripts_dir'], parameters['macse_script'])
        parameters['macse_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{MACSE}.{LOG_SUFF}')
        parameters['macse_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{MACSE}.{ERR_SUFF}')
        parameters['generax_families'] = parameters['families']
        parameters['generax_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['generax_template'])
        parameters['generax_script_file'] = os.path.join(parameters['scripts_dir'], parameters['generax_script'])
        parameters['generax_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{GENERAX}.{LOG_SUFF}')
        parameters['generax_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{GENERAX}.{ERR_SUFF}')
        parameters['generax_stats_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{GENERAX}.{CSV_SUFF}')
        parameters['generax_species_tree'] = os.path.join(
            parameters['generax_results_dir'], 'species_trees', 'starting_species_tree.newick'
        )
        parameters['decostar_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['decostar_template'])
        parameters['decostar_script_file'] = os.path.join(parameters['scripts_dir'], parameters['decostar_script'])
        parameters['decostar_parameters_file'] = os.path.join(parameters['decostar_aux_dir'], parameters['decostar_parameters'])
        parameters['decostar_in_adjacencies_file'] = os.path.join(parameters['decostar_aux_dir'], parameters['decostar_adjacencies'])
        parameters['decostar_in_gene_trees_file'] = os.path.join(parameters['decostar_aux_dir'], parameters['decostar_gene_trees'])
        parameters['decostar_out_adjacencies_file'] = os.path.join(
            parameters['decostar_results_dir'], f'{run_name}_{parameters["decostar_adjacencies"]}'
        )
        parameters['decostar_out_genes_file'] = os.path.join(
            parameters['decostar_results_dir'], f'{run_name}_{parameters["decostar_genes"]}'
        )
        parameters['decostar_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{DECOSTAR}.{LOG_SUFF}')
        parameters['decostar_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{DECOSTAR}.{ERR_SUFF}')
        parameters['decostar_stats_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{DECOSTAR}.{CSV_SUFF}')
        if 'decostar_sep' not in parameters.keys(): parameters['decostar_sep'] = SEP_DECOSTAR
        parameters['sppdcj_ilp_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['sppdcj_ilp_template'])
        parameters['sppdcj_gurobi_template_file'] = os.path.join(parameters['in_scripts_dir'], parameters['sppdcj_gurobi_template'])
        parameters['sppdcj_ilp_script_file'] = os.path.join(parameters['scripts_dir'], parameters['sppdcj_ilp_script'])
        parameters['sppdcj_gurobi_script_file'] = os.path.join(parameters['scripts_dir'], parameters['sppdcj_gurobi_script'])        
        parameters['sppdcj_in_adjacencies_file'] = os.path.join(parameters['sppdcj_aux_dir'], parameters['sppdcj_adjacencies'])
        parameters['sppdcj_in_species_tree_file'] = os.path.join(parameters['sppdcj_aux_dir'], parameters['sppdcj_species_tree'])
        parameters['sppdcj_out_adjacencies_file'] = os.path.join(
            parameters['sppdcj_results_dir'], f'{run_name}_{parameters["sppdcj_adjacencies"]}'
        )
        parameters['sppdcj_out_idmap_file'] = os.path.join(
            parameters['sppdcj_results_dir'], f'{run_name}_{parameters["sppdcj_idmap"]}'
        )
        parameters['sppdcj_log_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{SPPDCJ}.{LOG_SUFF}')
        parameters['sppdcj_err_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{SPPDCJ}.{ERR_SUFF}')
        parameters['sppdcj_stats_file'] = os.path.join(parameters['log_dir'], f'{run_name}_{SPPDCJ}.{CSV_SUFF}')
        if 'sppdcj_sep' not in parameters.keys(): parameters['sppdcj_sep'] = SEP_SPPDCJ
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
    os.makedirs(parameters['decostar_log_dir'], exist_ok=True)
    os.makedirs(parameters['decostar_results_dir'], exist_ok=True)
    os.makedirs(parameters['decostar_aux_dir'], exist_ok=True)
    os.makedirs(parameters['sppdcj_log_dir'], exist_ok=True)
    os.makedirs(parameters['sppdcj_results_dir'], exist_ok=True)
    os.makedirs(parameters['sppdcj_aux_dir'], exist_ok=True)
    with open(parameters['data_families'], 'r') as f1, open(parameters['active_families'], 'w') as f2:
        for fam in f1.readlines(): f2.write(f'{fam.split()[0]}\n')
    shutil.copy(parameters['data_species_tree'], parameters['active_species_tree'])
    shutil.copy(parameters['data_genes_map'], parameters['active_genes_map'])
    os.makedirs(parameters['active_gene_orders_dir'], exist_ok=True)
    for species in get_extant_species(parameters):
        data_order = os.path.join(parameters['data_gene_orders_dir'], f'{species}.txt')
        active_order = os.path.join(parameters['active_gene_orders_dir'], f'{species}.txt')
        shutil.copy(data_order, active_order)

# Auxiliary functions: data access --------------------------------------------------------
        
''' Create a list of species '''
def get_extant_species(parameters):
    '''
    output: list(str) list of extant species
    '''
    return([species.rstrip() for species in open(parameters['data_extant_species'], 'r').readlines()])

''' List of active families '''
def get_active_families(parameters):
    '''
    output: list(str) list of active families names
    '''
    active_families = [i.rstrip() for i in open(parameters['active_families'], 'r').readlines()]
    return(active_families)

''' Creates an error family id ><idx><SEP_ERR_FAM_ID><name> '''
def set_family_id(family_idx, family_name):
    return(f'>{family_idx}{SEP_ERR_FAM_ID}{family_name}')            
''' Extracts the family name (str) from an error family index '''
def get_family_name(family):
    return(family.split(SEP_ERR_FAM_ID)[1])
''' Extracts the family idx (str) from an error family index '''
def get_family_idx(family):
    return(family.split(SEP_ERR_FAM_ID)[0][1:])

''' Create a dictionary indexed by gene names and mapping to pairs (family,species) '''
def get_genes_map(parameters):
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
def get_families_map(parameters):
    '''
    output: dict(family_name(str) -> [gene_name(str),species(str)]
    '''
    families_map = defaultdict(list)
    with open(parameters['active_genes_map'], 'r') as f:
        for gene_data in f.readlines()[1:]:
            gene,family,species = gene_data.rstrip().split(SEP_GENE_MAP)
            families_map[family].append([gene,species])
    return(families_map)

''' Returns the path to active gene order for species '''
def get_active_gene_order_file(parameters, species):
    '''
    output: (str) path
    '''
    return(os.path.join(parameters['active_gene_orders_dir'], f'{species}.txt'))
    

# Auxiliary functions: update data --------------------------------------------------------

''' Update the active species tree '''
def update_active_species_tree(parameters, new_tree_file, backup_suffix):
    '''
    input:
    - new_tree_file: (str) path to new species tree file (newick format)
    - backup_suffix: (str) suffix to add to the backuped active species tree file
    output:
    - copies parameters['active_species_tree'] to parameters['active_species_tree']_<backup_suffix>
    - replaces parameters['active_species_tree'] by new_tree_file
    '''
    backup_file = f'{parameters["active_species_tree"]}_{backup_suffix}'
    shutil.copy(parameters['active_species_tree'], backup_file)
    shutil.copy(new_tree_file, parameters['active_species_tree'])

''' Update the active families file, saving a backup file '''
def update_active_families(parameters, families_to_remove, backup_suffix):
    '''
    input:
    - families_to_remove: list(str) list of families to discard from active families
    - backup_file: (str) suffix to add to the backuped active families file
    output:
    - modifies parameters['active_families']
    - creates parameters['active_families']_<backup_suffix>
    '''
    active_file = parameters['active_families']
    backup_file = f'{active_file}_{backup_suffix}'
    shutil.copy(active_file, backup_file)
    active_families = [i for i in get_active_families(parameters) if i not in families_to_remove]
    with open(parameters['active_families'], 'w') as f:
        for i in active_families: f.write(f'{i}\n')
                
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
        families_2_remove = [get_family_name(l.split(SEP_ERR_FIELDS)[0]) for l in f.readlines()[1:]]
    update_active_families(parameters, families_2_remove, backup_suffix)

''' Update the active gene orders based on the active families file, saving a backup file '''
def update_active_gene_orders(parameters, backup_suffix):
    '''
    input:
    - backup_file: (str) suffix to add to the backuped active families file
    output:
    - modifies files parameters['active_gene_orders_dir']/<species>.txt
    - creates parameters['active_gene_orders_dir']/<species>.txt_<backup_suffix>
    '''
    active_families = get_active_families(parameters)
    extant_species = get_extant_species(parameters)
    genes_map = get_genes_map(parameters)
    for species in extant_species:
        active_file = get_active_gene_order_file(parameters, species)
        backup_file = f'{active_file}_{backup_suffix}'
        shutil.copy(active_file, backup_file)
        with open(backup_file, 'r') as backup, open(active_file, 'w') as active:
            for gene in backup.readlines():
                gene_name = gene.split(SEP_ORDER)[0]
                if genes_map[gene_name][0] in active_families:
                    active.write(gene)

def update_active_gene_orders_post_step(parameters, backup_suffix):
    update_active_gene_orders(parameters, backup_suffix)

# Auxiliary functions: SLURM -------------------------------------------------------------

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

# Auxiliary functions: I/O -------------------------------------------------------------

''' Read the last line of a file '''
def get_last_line_file(file_path):
    '''
    output: (str) last line of file or EMPTY_FILE if empty file
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0: return(f'{file_path} {EMPTY_FILE}')
        else: return(lines[-1].rstrip())
    

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
            idx,fam = get_family_idx(err_family),get_family_name(err_family)
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
    fam_id<SEP_ERR_FIELDS><ERROR_MSG/SUCCESS_MSG><SEP_ERR_FIELDS>error/success message
    '''
    active_families = get_active_families(parameters)
    with open(parameters['macse_log_file'], 'w') as log_file, open(parameters['macse_err_file'], 'w') as err_file:
        for idx in range(1,len(active_families)+1):
            fam_id = set_family_id(idx, active_families[idx-1])
            idx_log_pref = os.path.join(parameters['macse_log_dir'], f'{parameters["macse_log_pref"]}_{idx}')
            idx_log_file,idx_err_file = f'{idx_log_pref}.{LOG_SUFF}',f'{idx_log_pref}.{ERR_SUFF}'
            if not (os.path.exists(idx_log_file) and os.path.exists(idx_err_file)):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, ERROR_MSG, "missing SLURM log"])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "missing SLURM log"])}')
                continue
            log_last,err_last = get_last_line_file(idx_log_file),get_last_line_file(idx_err_file)
            if log_last != 'PROGRAM HAS FINISHED SUCCESSFULLY':
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, ERROR_MSG, log_last])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, err_last])}')
                continue
            log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, SUCCESS_MSG, log_last])}')
        return(None)

# RecPhyloXML ----------------------------------------------------------------

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
            stats[last_event_species][STATS_xmlkeys[last_event_tag]] += 1
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

# Species tree ---------------------------------------------------------------

''' Creates a map from node names to list of descendant extant species '''
def get_leaves(tree_file):
    '''
    input: paths to a Newick tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    tree = ete3.Tree(tree_file, format=1)
    leaves = defaultdict(list)
    for node in tree.traverse():
        for leaf in node: leaves[node.name].append(leaf.name)
        leaves[node.name].sort()
    return(leaves)

''' Creates a map from node names to children '''
def get_children(tree_file):
    '''
    input: paths to a Newick tree file with internal nodes named
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
    '''
    tree = ete3.Tree(tree_file, format=1)
    children = defaultdict(list)
    for node in tree.traverse():
        if not node.is_leaf():
            children[node.name] = [ch.name for ch in node.children]
    return(children)

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
    families_map = get_families_map(parameters)
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

''' Reformat in proper recPhyloXML format all generax XML files '''
def reformat_generax(parameters):
    def reformat_generax_RecPhyloXML(in_file, out_file):
        ''' Should be done using the XML libray '''
        with open(in_file, 'r') as in_xml, open(out_file, 'w') as out_xml:
            out_xml.write('<recPhylo>\n')
            name = 0
            for line in in_xml.readlines()[1:]:
                line1 = line.strip()
                if line1[0]!='<': continue
                if line1 == '<name></name>':
                    out_xml.write(line.replace('><', f'>n{name}<'))
                    name += 1
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
                
    with open(parameters['generax_log_file'], 'r') as log_file:
        families_data = log_file.readlines()[1:]
        for family_data in families_data:
            fam_id,status,msg = family_data.rstrip().split(SEP_ERR_FIELDS)
            if status == ERROR_MSG:
                continue
            rec_tree = os.path.splitext(msg)[0]
            in_xml_rec_tree = rec_tree+'.'+XML_SUFF
            out_xml_rec_tree = rec_tree+'.'+REC_SUFF
            reformat_generax_RecPhyloXML(in_xml_rec_tree, out_xml_rec_tree)


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
            error_families[err_line_header.split()[3]] = err_line_msg
    with open(parameters['generax_log_file'], 'w') as log_file, open(parameters['generax_err_file'], 'w') as err_file:
        for idx in range(1,len(active_families)+1):            
            family = active_families[idx-1]
            fam_id = set_family_id(idx, family)
            if family in error_families.keys():
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, ERROR_MSG, error_families[family]])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, error_families[family]])}')
                continue
            rec_tree = os.path.join(parameters['generax_results_dir'], 'reconciliations', f'{family}_reconciliated.nhx')
            if not os.path.isfile(rec_tree):
                log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, ERROR_MSG, "missing reconciled tree"])}')
                err_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, "missing reconciled tree"])}')
                continue
            log_file.write(f'\n{SEP_ERR_FIELDS.join([fam_id, SUCCESS_MSG, rec_tree])}')
    return(None)

''' Returns the path to the XML reconciled gene tree for a family '''
def generax_gene_tree(parameters, family, suffix):
    '''
    output: path to XML reconciled gene tree file for family
    '''
    return(os.path.join(parameters['generax_results_dir'], 'reconciliations', f'{family}_reconciliated.{suffix}'))

''' Computes statistics post GeneRax '''
def stats_generax(parameters):
    ''' 
    output: 
    creates parameters['generax_stats_file'] with reconciliation statistics per species 
    '''
    active_families = get_active_families(parameters)
    statistics = {}
    for family in active_families:
        rec_tree = generax_gene_tree(parameters, family, REC_SUFF)
        try:
            stats_all = read_RecPhyloXML(rec_tree)
            for species,stats in stats_all.items():
                if species not in statistics.keys(): 
                    statistics[species] = {STATS_genes: 0, STATS_dup: 0, STATS_loss: 0}
                for stats_key in STATS_keys:
                    statistics[species][stats_key] += stats[stats_key]
        except FileNotFoundError:
            print(f'File {rec_tree} not found')                
    with open(parameters['generax_stats_file'], 'w') as stats_file:
        stats_file.write(SEP_STATS_FIELDS.join(['species', STATS_genes, STATS_dup, STATS_loss]))
        for species,stats in statistics.items():
            stats_str = [str(species), str(stats[STATS_genes]), str(stats[STATS_dup]), str(stats[STATS_loss])]
            stats_file.write(f'\n{SEP_STATS_FIELDS.join(stats_str)}')

            
# DeCoSTAR functions ------------------------------------------------------------

'''  Create DeCoSTAR input files: gene trees, adjacencies and parameters files '''

def aux_decostar_gene_trees(parameters):
    '''
    output: parameters['decostar_in_gene_trees_file']
    DeCoSTAR file containing the list of gene trees
    '''
    input_tool = parameters['decostar_input'].lower()
    with open(parameters['decostar_in_gene_trees_file'], 'w') as gene_trees:
        if input_tool == 'generax':
            for family in get_active_families(parameters):
                gene_trees.write(f'{generax_gene_tree(parameters, family)}\n')

def aux_decostar_adjacencies(parameters):
    '''
    output: parameters['decostar_in_adjacencies_file']
    DeCoSTAR file containing the list of extant adjacencies
    '''
    orientation = {
        ('0','0'): ['-','+'], ('0','1'): ['-','-'], ('1','0'): ['+','+'], ('1','1'): ['+','-']
    }
    with open(parameters['decostar_in_adjacencies_file'], 'w') as adjacencies:
        for species in get_extant_species(parameters):
            gene_order_file = os.path.join(parameters['active_gene_orders_dir'], f'{species}.txt')
            with open(gene_order_file, 'r') as gene_order:
                prev_gene = None
                for gene in gene_order.readlines():
                    gene_data = gene.rstrip().split(SEP_ORDER)
                    gene_name,gene_chr,gene_sign = gene_data[0],gene_data[5],gene_data[1]
                    if prev_gene is not None and prev_gene[1] == gene_chr:
                        adj = [prev_gene[0], gene_name] + orientation[(prev_gene[2],gene_sign)] + ['1']
                        adjacencies.write(f'{SEP_ADJ.join(adj)}\n')
                    prev_gene = [gene_name,gene_chr,gene_sign]

def aux_decostar_parameters(parameters):
    '''
    output: parameters['decostar_parameters_file']
    DeCoSTAR file containing the list of DeCoSTAR parameters
    '''
    input_tool = parameters['decostar_input'].lower()
    with open(parameters['decostar_parameters_file'], 'w') as decostar_parameters:
        decostar_parameters.write(f'species.file={parameters["active_species_tree"]}\n')
        decostar_parameters.write(f'adjacencies.file={parameters["decostar_in_adjacencies_file"]}\n')
        decostar_parameters.write(f'gene.distribution.file={parameters["decostar_in_gene_trees_file"]}\n')
        decostar_parameters.write(f'output.dir={parameters["decostar_results_dir"]}\n')
        if input_tool == 'generax':
            decostar_parameters.write('already.reconciled=true\n')
        decostar_parameters.write('use.boltzmann=true\n')
        decostar_parameters.write(f'boltzmann.temperature={parameters["decostar_temperature"]}\n')
        decostar_parameters.write(f'nb.sample={parameters["decostar_nb_samples"]}\n')
        decostar_parameters.write(f'rooted={parameters["decostar_rooted"]}\n')
        decostar_parameters.write(f'dated.species.tree={parameters["decostar_dated"]}\n')
        decostar_parameters.write(f'with.transfer={parameters["decostar_hgt"]}\n')
        decostar_parameters.write(f'try.all.amalgamation={parameters["decostar_amalgamation"]}\n')
        decostar_parameters.write(f'write.newick=true\n')
        decostar_parameters.write(f'write.adjacencies=true\n')
        decostar_parameters.write(f'write.genes=true\n')
        decostar_parameters.write(f'verbose={parameters["decostar_verbose"]}')

''' Creates the input data files for DeCoSTAR '''    
def aux_decostar(parameters):
    '''
    output:
    - parameters['decostar_in_gene_trees_file']
    - parameters['decostar_in_adjacencies_file']
    - parameters['decostar_parameters_file']
    File formats are the ones required by DeCoSTAR
    '''
    # Creating gene trees file
    aux_decostar_gene_trees(parameters)
    # Creating the adjacencies
    aux_decostar_adjacencies(parameters)
    # Creating the parameters file
    aux_decostar_parameters(parameters)

''' Substitutions in DeCoSTAR template file to create DeCoSTAR SLURM script '''
def decostar_script_patterns(parameters):
    return(
        {
            'XX_slurm_account': parameters['slurm_account'],
            'XX_tools_dir': parameters['tools_dir'],
            'XX_decostar_memory': parameters['decostar_memory'],
            'XX_decostar_time': str(parameters['decostar_time']),
            'XX_decostar_log_dir': parameters['decostar_log_dir'],
            'XX_decostar_log_pref': parameters['decostar_log_pref'],
            'XX_decostar_parameters_file': parameters['decostar_parameters_file']
        }
    )

''' Create a DeCoSTAR SLURM script '''
def run_decostar(parameters, run_script=False):
    '''
    input: run_script: (boolean) run created scripts if True
    output: 
    - creates parameters['decostar_script_file']
    - jobid: (str/None) SLURM job ID if job is run
    '''
    return(
        create_slurm_script(
            parameters,
            'decostar_template_file',
            'decostar_script_file',
            decostar_script_patterns(parameters),
            run_script=run_script
        )
    )

''' Read the map from nodes to descendant leaves from DeCoSTAR output '''
def decostar_get_leaves(parameters):
    '''
    output:
    - dictionary dict(str->list(str)) indexed by names of nodes in tree_file
      each list is sorted in alphabetical order
    '''
    map_file = os.path.join(parameters['decostar_results_dir'],'species.txt')
    leaves = {}
    with open(map_file, 'r') as map:
        for node in map.readlines():
            node_data = node.rstrip().split()
            leaves[node_data[0]] = node_data[1:]
            leaves[node_data[0]].sort()
    return(leaves)

''' Return a map of correspondance between species names pf active species tree and DeCoSTAR species '''
def decostar_species_map(parameters):
    '''
    output: dict(str->str) indexd by DeCoSTAR species labels
    '''
    active_leaves_map = get_leaves(parameters['active_species_tree'])
    decostar_leaves_map = decostar_get_leaves(parameters)
    map_aux = defaultdict(list)
    for species,leaves in active_leaves_map.items():
        map_aux[''.join(leaves)].append(species)
    for species,leaves in decostar_leaves_map.items():
        map_aux[''.join(leaves)].append(species)
    map = {}
    for species_pair in map_aux.values():
        map[species_pair[1]] = species_pair[0]
    return(map)

''' Reformat the DeCoSTAR adjacencies and genes files to use species names of active species tree and names of active families '''
def reformat_decostar(parameters):
    '''
    output: parameters['decostar_out_genes_file'], parameters['decostar_out_adjacencies_file']
    '''
    active_families = get_active_families(parameters)
    species_map = decostar_species_map(parameters)
    char_sep = parameters['decostar_sep']
    # Map of gene names initialized by extant genes
    genes_map = {}
    for gene,data in get_genes_map(parameters).items(): genes_map[gene] = f'{data[0]}{char_sep}{gene}'
    # Genes file
    genes_file = os.path.join(parameters['decostar_results_dir'], 'genes.txt')
    with open(genes_file, 'r') as in_genes, open(parameters['decostar_out_genes_file'], 'w') as out_genes:
        for line in in_genes.readlines():
            line_split = line.rstrip().split()
            in_species,in_gene = line_split[0],line_split[1]
            out_species = species_map[in_species]
            if char_sep in in_gene:
                family,gene_id = in_gene.split(char_sep)
                out_gene = f'{active_families[int(family)]}{char_sep}{gene_id}'
                genes_map[in_gene] = out_gene
            else:
                out_gene = in_gene
            out_gene_str = ' '.join([out_species, out_gene] + [genes_map[in_gene] for in_gene in line_split[2:]])
            out_genes.write(f'{out_gene_str}\n')
    # Adjacencies file
    adjacencies_file = os.path.join(parameters['decostar_results_dir'], 'adjacencies.txt')
    with open(adjacencies_file, 'r') as in_adj, open(parameters['decostar_out_adjacencies_file'], 'w') as out_adj:
        for line in in_adj.readlines():
            line_split = line.rstrip().split()
            in_species,in_gene1,in_gene2 = line_split[0],line_split[1],line_split[2]
            out_species = species_map[in_species]
            out_gene1,out_gene2 = genes_map[in_gene1],genes_map[in_gene2]
            out_adj_str = ' '.join([out_species, out_gene1, out_gene2] + line_split[3:])
            out_adj.write(f'{out_adj_str}\n')


# SPP-DCJ -----------------------------------------------------------------------

''' Creates SPP-DCJ species tree file '''
def aux_sppdcj_species_trees(parameters):
    '''
    output: parameters['sppdcj_in_species_tree_file']
    '''
    children_map = get_children(parameters['active_species_tree'])
    with open(parameters['sppdcj_in_species_tree_file'], 'w') as species_tree:
        for species,children in children_map.items():
            species_tree.write(f'{species}{SEP_SPPDCJ_FIELDS}{children[0]}\n')
            species_tree.write(f'{species}{SEP_SPPDCJ_FIELDS}{children[1]}\n')

''' Creates the SPP-DCJ adjacencies file '''
def aux_sppdcj_adjacencies(parameters):
    '''
    output: parameters['sppdcj_in_adjacencies_file']
    '''
    orientation = {
        ('-','+'): ['t','t'], ('-','-'): ['t','h'], ('+','-'): ['h','h'], ('+','+'): ['h','t']
    }
    decostar_sep = parameters['decostar_sep']
    sppdcj_sep = parameters['sppdcj_sep']
    weight_threshold = float(parameters['sppdcj_threshold'])
    with open(parameters['decostar_out_adjacencies_file'], 'r') as decostar_adj, open(parameters['sppdcj_in_adjacencies_file'], 'w') as sppdcj_adj:
        header_str = ["#Species","Gene_1","Ext_1","Species","Gene_2","Ext_2","Weight"]
        sppdcj_adj.write(f'{SEP_SPPDCJ_FIELDS.join(header_str)}')
        for adj in decostar_adj.readlines():
            species,gene1,gene2,sign1,sign2,_,weight = adj.rstrip().split()
            signs = orientation[(sign1,sign2)]
            fam1,gene1_name = gene1.split(decostar_sep)
            fam2,gene2_name = gene2.split(decostar_sep)
            if float(weight) >= weight_threshold:
                adj_str = [species,f'{fam1}{sppdcj_sep}{gene1_name}',signs[0],species,f'{fam2}{sppdcj_sep}{gene2_name}',signs[1],weight]
                sppdcj_adj.write(f'\n{SEP_SPPDCJ_FIELDS.join(adj_str)}')

''' Creates SPP-DCJ input files '''
def aux_sppdcj(parameters):
    '''
    output:
    parameters['sppdcj_in_species_tree_file']
    parameters['sppdcj_in_adjacencies_file']
    '''
    aux_sppdcj_species_trees(parameters)
    aux_sppdcj_adjacencies(parameters)

''' Substitutions in SPP-DCJ template files to create SLURM scripts '''
def sppdcj_script_patterns(parameters):
    return(
        {
            'XX_slurm_account': parameters['slurm_account'],
            'XX_tools_dir': parameters['tools_dir'],
            'XX_sppdcj_ilp_memory': parameters['sppdcj_ilp_memory'],
            'XX_sppdcj_ilp_time': str(parameters['sppdcj_ilp_time']),
            'XX_sppdcj_gurobi_memory': parameters['sppdcj_gurobi_memory'],
            'XX_sppdcj_gurobi_time': str(parameters['sppdcj_gurobi_time']),
            'XX_sppdcj_alpha': str(parameters['sppdcj_alpha']),
            'XX_sppdcj_beta': str(parameters['sppdcj_beta']),
            'XX_sppdcj_ilp_options': parameters['sppdcj_ilp_options'],
            'XX_sppdcj_log_dir': parameters['sppdcj_log_dir'],
            'XX_sppdcj_log_pref': parameters['sppdcj_log_pref'],
            'XX_sppdcj_species_tree_file': parameters['sppdcj_in_species_tree_file'],
            'XX_sppdcj_adjacencies_file': parameters['sppdcj_in_adjacencies_file'],
            'XX_sppdcj_idmap_file': parameters['sppdcj_out_idmap_file']
        }
    )

''' Create a SPP-DCJ SLURM script to create the ILP '''
def run_sppdcj_ilp(parameters, run_script=False):
    '''
    input: run_script: (boolean) run created scripts if True
    output: 
    - creates parameters['sppdcj_ilp_script_file']
    - jobid: (str/None) SLURM job ID if job is run
    '''
    return(
        create_slurm_script(
            parameters,
            'sppdcj_ilp_template_file',
            'sppdcj_ilp_script_file',
            sppdcj_script_patterns(parameters),
            run_script=run_script
        )
    )


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
        check_macse(parameters)
    elif command == 'rerun_macse':
        mem = sys.argv[3]
        time = sys.argv[4]
        if len(sys.argv) == 6: run_val = (sys.argv[5] in TRUE_LIST)
        else: run_val = False
        rerun_macse_jobsid = rerun_macse(parameters, mem, time, run_script=run_val)
    elif command == 'update_post_macse':
        backup_suffix = sys.argv[3]
        update_active_families_post_step(parameters, parameters['macse_err_file'], backup_suffix)
        update_active_gene_orders_post_step(parameters, backup_suffix)
    elif command == 'aux_generax':
        aux_generax(parameters)
    elif command == 'run_generax':
        if len(sys.argv) == 4: run_val = (sys.argv[3] in TRUE_LIST)
        else: run_val = False
        run_generax_jobid = run_generax(parameters, run_script=run_val)
    elif command == 'check_generax':
        check_generax(parameters)
    elif command == 'reformat_generax':
        reformat_generax(parameters)
    elif command == 'stats_generax':
        stats_generax(parameters)
    elif command == 'update_post_generax':
        backup_suffix = sys.argv[3]
        update_active_families_post_step(parameters, parameters['generax_err_file'], backup_suffix)
        update_active_species_tree(parameters, parameters['generax_species_tree'], backup_suffix)
        update_active_gene_orders_post_step(parameters, backup_suffix)
    elif command == 'aux_decostar':
        aux_decostar(parameters)
    elif command == 'run_decostar':
        if len(sys.argv) == 4: run_val = (sys.argv[3] in TRUE_LIST)
        else: run_val = False
        run_decostar_jobid = run_decostar(parameters, run_script=run_val)
    elif command == 'reformat_decostar':
        reformat_decostar(parameters)
    elif command == 'aux_sppdcj':
        aux_sppdcj(parameters)
    elif command == 'run_sppdcj_ilp':
        if len(sys.argv) == 4: run_val = (sys.argv[3] in TRUE_LIST)
        else: run_val = False
        run_sppdcj_ilp_jobid = run_sppdcj_ilp(parameters, run_script=run_val)

        
if __name__ == "__main__":
    main()
