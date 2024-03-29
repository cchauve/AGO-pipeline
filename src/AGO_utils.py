#!/usr/bin/env python3
# coding: utf-8

""" AGO pipeline: utils functions """

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0.3"
__status__    = "Released"

import os
from collections import defaultdict
import subprocess
from AGO_parameters import Parameters

'''Create a parameters file '''
def create_parameters_file(header_file_path, yaml_dir, tools_list, out_file_path):
    with open(out_file_path, 'w') as out_file:
        files_list = [header_file_path, os.path.join(yaml_dir, 'LOG.yaml')]
        for file_path in files_list:
            with open(file_path) as in_file:
                out_file.write(in_file.read())
        out_file.write('tools:\n')
        files_list = [os.path.join(yaml_dir, f'{tool}.yaml') for tool in tools_list]
        for file_path in files_list:
            with open(file_path) as in_file:
                out_file.write(in_file.read())

''' Generic function to create SLURM script '''
def create_slurm_script(parameters, tool):
    aux_dir = parameters.get_dir_aux(tool)
    script_name = f'{parameters.get_tool_name(tool, suffix=True)}.sh'
    script_file = os.path.join(aux_dir, script_name)
    if parameters.check_tool_input_script(tool):
        for cmd in parameters.get_tool_input_script(tool):
            subprocess.run(cmd)
    with open(script_file, 'w') as script:
        script.write('#!/bin/bash\n')
        slurm_options = parameters.get_slurm_options(tool, suffix=True)
        slurm_modules = parameters.get_slurm_modules(tool)
        slurm_cmd = parameters.get_slurm_cmd(tool, concat='\n')
        for option in slurm_options:
            script.write(f'\n#SBATCH {option}')
        if parameters.check_slurm_array_input(tool):
            TASK_ID = '${SLURM_ARRAY_TASK_ID}'
            array_size = parameters.get_slurm_array_input_len(tool)
            script.write(f'\n#SBATCH --array=1-{array_size}\n')
            array_specs = parameters.get_slurm_array_data(tool)
            for array_spec in array_specs.values():                
                script.write(
                    f'\n{array_spec["var"]}='
                    f'$(sed "{TASK_ID}q;d" {array_spec["file"]} |'
                    f'cut -f {array_spec["field"]})'
                )
        if slurm_modules is not None:
            script.write(f'\n\nmodule load {slurm_modules}')
        script.write(f'\n\n{slurm_cmd}')
    return [script_file]

''' Generic function to create BASH script '''
def create_bash_script(parameters, tool):
    aux_dir = parameters.get_dir_aux(tool)
    script_name = f'{parameters.get_tool_name(tool, suffix=True)}.sh'
    script_file = os.path.join(aux_dir, script_name)
    if parameters.check_tool_input_script(tool):
        for cmd in parameters.get_tool_input_script(tool):
            subprocess.run(cmd)
    with open(script_file, 'w') as script:
        script.write('#!/bin/bash\n\n')
        bash_modules = parameters.get_slurm_modules(tool)
        if bash_modules is not None:
            script.write(f'\n\nmodule load {bash_modules}\n\n')        
        if parameters.check_slurm_array_input(tool):
            TASK_ID = '${TASK_ID}'
            array_size = parameters.get_slurm_array_input_len(tool)
            script.write(f'for ((TASK_ID=1;TASK_ID<={array_size};TASK_ID++));\ndo\n')
            array_specs = parameters.get_slurm_array_data(tool)            
            for array_spec in array_specs.values():
                script.write(
                    f'\n\t{array_spec["var"]}='
                    f'$(sed "{TASK_ID}q;d" {array_spec["file"]} |'
                    f'cut -f {array_spec["field"]})'
                )
            script.write('\n\n\t')
            script.write(parameters.get_slurm_cmd(tool, concat='\n\t'))
            script.write('\ndone\n')
        else:
            bash_cmd = parameters.get_slurm_cmd(tool, concat='\n')
            script.write(f'\n\n{bash_cmd}')
    return [script_file]


''' Generic function to create a log file '''
def create_log_file(parameters, tool):
    # File where to write the link to output files
    log_file = parameters.get_log_file(tool, suffix=True)
    # Separators
    sep1 = parameters.get_sep_fields()
    sep2 = parameters.get_sep_space()
    sep3 = parameters.get_sep_list()
    # List of errors
    errors = []
    results_files = parameters.get_slurm_results_files(tool)
    with open(log_file, 'w') as log:
        log.write(
            f'#status{sep1}tool{sep1}index{sep1}message\n'
        )
        for results_file in results_files:
            res_index,res_path = results_file[0],results_file[1]
            if not os.path.isfile(res_path):
                log.write(
                    f'{parameters.get_error_msg()}{sep1}'
                    f'{tool}{sep1}'
                    f'{res_index}{sep1}'
                    f'{res_path}{sep2}{parameters.get_missing_msg()}\n'
                )
                if res_index not in errors:
                    errors.append(res_index)
            else:
                log.write(
                    f'{parameters.get_success_msg()}{sep1}'
                    f'{tool}{sep1}'
                    f'{res_index}{sep1}'
                    f'{res_path}\n'
                )
    return log_file,len(errors)

''' Generic function to create an output file from Slurm results '''
def create_output_file(parameters, tool):
    output_file = parameters.get_output_file(tool)
    if output_file is not None:
        sep1 = parameters.get_sep_fields()        
        results_files = parameters.get_slurm_results_files(tool)
        # Reading file if it does exist
        res_dict = defaultdict(str)
        if os.path.isfile(output_file):
            with open(output_file, 'r') as output:
                for result in output.readlines():
                    res_index,res_path = result.rstrip().split(sep1)
                    res_dict[res_index] = res_path
        # Updating the results dictionary
        for results_file in results_files:
            res_index,res_path = results_file[0],results_file[1]
            if res_index != '':
                res_dict[res_index] = res_path
        # Writing the results dictionary in the output file
        with open(output_file, 'w') as output:
            for res_index,res_path in res_dict.items():
                if os.path.isfile(res_path):
                    output.write(f'{res_index}{sep1}{res_path}\n')        
        return output_file
    else:
        return 'No output file is created'

''' Generic function to check the results of a Slurm process and create a log file '''
def check_results(parameters, tool):
    log_file,nb_errors = create_log_file(parameters, tool)
    output_file = create_output_file(parameters, tool)
    return [f'ERRORS:\t{nb_errors}', f'LOG:\t{log_file}', f'OUTPUT:\t{output_file}']

''' Generic function to delete the results file creates by a Slurm process '''
def clean_results(parameters, tool):
    nb_deleted_files = 0
    for results_file in parameters.get_slurm_results_files(tool):
        res_path = results_file[1]
        if os.path.isfile(res_path):
            os.remove(res_path)
            nb_deleted_files += 1
    return [nb_deleted_files]

''' Generic function to compute a statistics file '''
def compute_statistics(parameters, tool):
    for cmd in parameters.get_statistics_cmd(tool):
        subprocess.run(cmd)
    return parameters.get_statistics_files(tool)
