#!/usr/bin/env python3
# coding: utf-8

""" Reading AGO pipeline parameters """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

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
Parameters class and methods
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
        for AGO_object_name,AGO_object_values in self.parameters['data'].items():
            # Copy only input data files for record
            in_file_path = AGO_object_values['path']
            if os.path.isfile(in_file_path):
                in_file_name = os.path.basename(in_file_path)
                out_file_path = os.path.join(
                    self.parameters['dir']['data'],
                    in_file_name 
                )
                if out_file_path != in_file_path:
                    shutil.copy(in_file_path, out_file_path)
                    print(f'\t{in_file_path} -> {out_file_path}.')
                else:
                    print(f'\t{in_file_path} will be computed.')                            
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
    
    def get_log_file(self, tool, suffix=False):
        return os.path.join(
            self.get_dir_log(),
            f'{self.get_tool_name(tool, suffix=suffix)}{self.get_log_ext()}'
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

    def get_tool_name(self, tool, suffix=False):
        name = self.parameters['tools'][tool]['name']
        if suffix and 'suffix' in self.parameters['tools'][tool].keys():
            name += self.parameters['tools'][tool]['suffix']
        return name

    def check_tool_input_script(self, tool):
        return ('script' in self.parameters['tools'][tool]['input'])
    def _get_script(self, input_script):
        result,current_script = [],[]
        for i in range(len(input_script)):
            if input_script[i] != ';':
                current_script.append(input_script[i])
            else:
                result.append(current_script)
                current_script = []
        result.append(current_script)
        return result
    def get_tool_input_script(self, tool):
        return self._get_script(self.parameters['tools'][tool]['input']['script'])
        
    
    def get_slurm_log_file_ext(self, tool, key, suffix=False):
        array = self.check_slurm_array_input(tool)
        log_dir = self.get_dir_log(tool)
        tool_name = self.get_tool_name(tool, suffix=suffix)
        LOG_ARRAY = {True: '_%a', False: ''}
        return os.path.join(
            log_dir, f'{tool_name}{LOG_ARRAY[array]}{self.get_ext(key)}'
        )
    def get_slurm_log_file(self, tool, suffix=False):
        return self.get_slurm_log_file_ext(tool, 'log', suffix=suffix)
    def get_slurm_err_file(self, tool, suffix=False):
        return self.get_slurm_log_file_ext(tool, 'err', suffix=suffix)

    def _get_slurm_options(self, tool):
        options = self.parameters['tools'][tool]['slurm']['options']
        if isinstance(options, str):
            options = options.split()
        return options    
    def get_slurm_options(self, tool, suffix=False):
        return [f'--account={self.parameters["slurm"]["account"]}'] +\
            self._get_slurm_options(tool) +\
            [f'--output={self.get_slurm_log_file(tool, suffix=suffix)}'] +\
            [f'--error={self.get_slurm_err_file(tool, suffix=suffix)}']

    def get_slurm_modules(self, tool):
        modules = self.parameters['tools'][tool]['slurm']['modules']
        if len(modules) > 0:
            return modules
        else:
            return None

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
        elif 'files' in all_results.keys():
            results_files += [
                ['', results_file]
                for results_file in all_results['files']
            ]
        return results_files

    def get_output_file(self, tool):
        tool_dict = self.parameters['tools'][tool]
        if 'output' in tool_dict.keys() and 'file' in  tool_dict['output'].keys():
            return self.parameters['tools'][tool]['output']['file']
        else:
            return None

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
            return []
        else:
            return self._get_script(stats['script'])
