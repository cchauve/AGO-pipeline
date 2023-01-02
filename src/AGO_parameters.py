#!/usr/bin/env python3
# coding: utf-8

""" AGO pipeline parameters """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys
import os
import shutil
import yaml


## define custom tag handler
def join(loader, node):
    seq = loader.construct_sequence(node)
    return os.path.join(*[str(s) for s in seq])

def concat(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(s) for s in seq])

def ref(loader, node):
    return concat(loader, node)

## register the tag handler
yaml.add_constructor('!join', join)
yaml.add_constructor('!concat', concat)
yaml.add_constructor('!ref', ref)

''' 
Parameters for the AGO pipeline 
'''
class Parameters:

    def __init__(self, yaml_file_path):
        ''' Parameters can only be created from a YAML file '''        
        with open(yaml_file_path, 'r') as yaml_file:
            self.parameters = yaml.load(yaml_file, Loader=yaml.Loader)

    def init(self):
        ''' Creates directories and initial data files '''
        for _,dir_path in self.parameters['dir'].items():
            os.makedirs(dir_path, exist_ok=True)
            for tool in self.parameters['tools'].keys():
                os.makedirs(os.path.join(dir_path, tool), exist_ok=True)
        for in_file_keys,in_file_values in self.parameters['data'].items():
            # Copy only input data files for record
            in_file_name = in_file_values['name']
            in_file_path = in_file_values['path']
            if os.path.isfile(in_file_path):
                in_file_path = in_file_values['path']
                out_file_path = os.path.join(
                    self.parameters['dir']['data'],
                    in_file_name
                )
                shutil.copy(in_file_path, out_file_path)
                print(f'\t{in_file_path} -> {out_file_path}.')
            else:
                print(f'\t{in_file_path} will be computed.')        

    def get_dir(self, dir_key, tool=None):
        if tool is None:
            out_dir = self.parameters['dir'][dir_key]
        else:
            out_dir = os.path.join(
                self.parameters['dir'][dir_key],
                tool
            )
        os.makedirs(out_dir, exist_ok=True)
        return out_dir

    def get_dir_aux(self, tool):
        return self.get_dir('aux', tool)
    def get_dir_log(self, tool=None):
        return self.get_dir('log', tool=tool)
    def get_dir_results(self, tool=None):
        return self.get_dir('results', tool=tool)    
    
    def get_log_file(self, tool):
        return os.path.join(
            self.get_dir_log(),
            f'{self.get_tool_name(tool)}.{self.get_log_ext()}'
        )

    def get_ext(self, key):
        return self.parameters['log']['ext'][key]
    def get_log_ext(self):
        return self.get_ext('log')
    def get_err_ext(self):
        return self.get_ext('err')

    def get_success_msg(self):
        return self.parameters['log']['msg']['success']    
    def get_error_msg(self):
        return self.parameters['log']['msg']['error']
    def get_missing_msg(self):
        return self.parameters['log']['msg']['missing']

    def get_sep_fields(self):
        return '\t'
    def get_sep_list(self):
        return ':'
    def get_sep_space(self):
        return ' '    

    def get_tool_name(self, tool):
        return self.parameters['tools'][tool]['name']

    def check_tool_input_script(self, tool):
        return ('script' in self.parameters['tools'][tool]['input'])
    def get_tool_input_script(self, tool):
        return self.parameters['tools'][tool]['input']['script']
    
    def get_slurm_log_file_ext(self, tool, key):
        array = self.check_slurm_array_input(tool)
        log_dir = self.get_dir_log(tool)
        LOG_ARRAY = {True: '_%a', False: ''}
        return os.path.join(
            log_dir, f'{tool}{LOG_ARRAY[array]}.{self.get_ext(key)}'
        )
    def get_slurm_log_file(self, tool):
        return self.get_slurm_log_file_ext(tool, 'log')
    def get_slurm_err_file(self, tool):
        return self.get_slurm_log_file_ext(tool, 'err')

    def get_slurm_options(self, tool):
        return [f'--account={self.parameters["slurm"]["account"]}'] +\
            self.parameters['tools'][tool]['slurm']['options'] +\
            [f'--output={self.get_slurm_log_file(tool)}'] +\
            [f'--error={self.get_slurm_err_file(tool)}']

    def get_slurm_modules(self, tool, concat=None):
        modules = self.parameters['tools'][tool]['slurm']['modules']
        if concat is None:
            return modules
        else:
            return concat.join(modules)

    def check_slurm_array_key(self, tool, key):
        slurm = self.parameters['tools'][tool]['slurm']
        test1 = 'array' in slurm.keys()
        test2 = test1 and (key in slurm['array'].keys())
        return test2
    def check_slurm_array_input(self, tool):
        return self.check_slurm_array_key(tool, 'input')
    def check_slurm_array_results(self, tool):
        return self.check_slurm_array_key(tool, 'results')
    def get_slurm_array_all(self, tool):
        return self.parameters['tools'][tool]['slurm']['array']
    def get_slurm_array_results(self, tool):
        return self.get_slurm_array_all(tool)['results']
    def get_slurm_array_data(self, tool):
        in_array = self.get_slurm_array_all(tool)
        out_array = {}
        for id,data in in_array.items():
            out_array[id] = {
                'file': data['file'],
                'field': data['field'],
                'var': data['var']
            }
        return out_array
    def get_slurm_array_input_file(self, tool):
        return self.get_slurm_array_all(tool)['input']['file']            
    def get_slurm_array_input_field(self, tool):
        return self.get_slurm_array_all(tool)['input']['field']
    def get_slurm_array_input_var(self, tool):
        return self.get_slurm_array_all(tool)['input']['var']    
    def get_slurm_array_input_len(self, tool):
        return len(
            open(self.get_slurm_array_input_file(tool)).readlines()
        )

    def get_slurm_cmd(self, tool, concat=None):
        cmd = self.parameters['tools'][tool]['slurm']['cmd']
        if concat is None:
            return cmd
        else:
            return concat.join(cmd)
        
    def get_slurm_results_all(self, tool):
        return self.parameters['tools'][tool]['slurm']['results']
    def check_slurm_reformat_results_files(self, tool):
        return ('script' in self.get_slurm_results_all(tool).keys())
    def get_slurm_reformat_results_files(self, tool):
        return self.get_slurm_results_all(tool)['script']

    def get_slurm_results_files(self, tool, suffix=''):
        all_results = self.get_slurm_results_all(tool)
        if 'other' in all_results.keys():
            results_files = [
                ['', other_file]
                for other_file in all_results['other']
            ]
        else:
            results_files = []
        if self.check_slurm_array_results(tool):
            array = self.get_slurm_array_results(tool)
            array_file = array['file']
            array_field = array['field']-1
            array_var = f'${{{array["var"]}}}'
            if 'ext' in array.keys(): suffix = array['ext']
            var_list = []
            with open(array_file, 'r') as in_file:
                for in_line in in_file.readlines():
                    var_list.append(in_line.rstrip().split()[array_field])
            results_files_template = all_results['files']
            for var in var_list:
                for results_file_template in results_files_template:
                    result_file = results_file_template.replace(array_var, var)
                    if result_file.endswith(suffix):
                        results_files.append([var, result_file])
        else:
            results_files += [
                ['', results_file]
                for results_file in all_results['files']
            ]
        return results_files

    def get_output_dir(self, tool):
        return self.parameters['tools'][tool]['output']['dir']
    def get_output_file(self, tool):
        return self.parameters['tools'][tool]['output']['file']

    def get_statistics_all(self, tool):
        if 'stats' in self.parameters['tools'][tool].keys():
            stats = self.parameters['tools'][tool]['stats']
        else:
            stats = None
        return stats
    def get_statistics_files(self, tool):
        stats = self.get_statistics_all(tool)
        if stats is None:
            return []
        else:
            return stats['files']
    def get_statistics_cmd(self, tool):
        stats = self.get_statistics_all(tool)
        if stats is None:
            return None
        else:
            return stats['cmd']
