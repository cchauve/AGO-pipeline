#!/usr/bin/env python3
# coding: utf-8

''' Running the various steps of the ancestral gene order pipeline, python2 functions '''

import os
import sys
import yaml
import subprocess

''' Constants '''

# log/err files suffixes
LOG_SUFF = 'log'
ERR_SUFF = 'err'
CSV_SUFF = 'csv'
REC_SUFF = 'recphyloxml.xml'
NHX_SUFF = 'nhx'
# log messages
ERROR_MSG = 'ERROR'
# Error files separators
SEP_ERR_FAM_ID = ':'
SEP_ERR_FIELDS = '\t'
# Tools names
GENERAX = 'GeneRax'

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
        # Tools-independent directories
        parameters['exp_dir'] = os.path.join(parameters['exp_dir_pref'], run_name)
        parameters['results_dir'] = os.path.join(parameters['exp_dir'], 'results')
        parameters['log_dir'] = os.path.join(parameters['exp_dir'], 'log')
        parameters['aux_dir'] = os.path.join(parameters['exp_dir'], 'aux')
        # Tools-specific directories
        parameters['generax_log_dir'] = os.path.join(parameters['log_dir'], parameters['generax_dir'])
        parameters['generax_results_dir'] = os.path.join(parameters['results_dir'], parameters['generax_dir'])
        parameters['generax_aux_dir'] = os.path.join(parameters['aux_dir'], parameters['generax_dir'])
        # Tools-specific files
        parameters['generax_log_file'] = os.path.join(parameters['log_dir'], run_name+'_'+GENERAX+'.'+LOG_SUFF)
        parameters['generax_species_tree'] = os.path.join(
            parameters['generax_results_dir'], 'species_trees', 'starting_species_tree.newick'
        )

    return(parameters)



# Auxiliary functions ----------------------------------------------------------
        
''' Extracts the family name (str) from an error family index '''
def get_family_name(family):
    return(family.split(SEP_ERR_FAM_ID)[1])
    
# GeneRax functions ----------------------------------------------------------

''' Post-processing GeneRax results '''
def postprocess_generax(parameters):
    '''
    Convert each reconciled gene tree into a recPhyloXML tree
    Compute statistics per species
    '''
    generax_species_tree = parameters['generax_species_tree']
    converter = ['python', parameters['tools_dir']+'/'+parameters['recphyloxml_convert']]
    statistics = ['python', parameters['tools_dir']+'/'+parameters['recphyloxml_events']]
    with open(parameters['generax_log_file'], 'r') as log_file:
        families_data = log_file.readlines()[1:]
        for family_data in families_data:
            fam_id,status,msg = family_data.rstrip().split(SEP_ERR_FIELDS)
            if status == ERROR_MSG:
                continue
            family = get_family_name(fam_id)
            rec_tree = os.path.splitext(msg)[0]
            nhx_rec_tree = rec_tree+'.'+NHX_SUFF
            xml_rec_tree = rec_tree+'.'+REC_SUFF
            stats_file = rec_tree+'.'+CSV_SUFF
            try:
                converter_cmd = converter + ['-g', nhx_rec_tree, '-s', generax_species_tree, '-o', xml_rec_tree, '--include.species']
                converter_jobid = subprocess.check_output(' '.join(converter_cmd), shell=True)
                statistics_cmd = statistics + ['-i', xml_rec_tree, '-o', stats_file]
                stats_jobid = subprocess.check_output(' '.join(statistics_cmd), shell=True)
            except subprocess.CalledProcessError, e:
                print(ERROR_MSG+'\t'+e.output)

# MAIN --------------------------------------------------------------------------

def main():
    parameters_file = sys.argv[1]
    parameters = read_parameters(parameters_file)
    command = sys.argv[2]

    if command == 'postprocess_generax':
        postprocess_generax(parameters)
           
if __name__ == "__main__":
    main()
