#!/usr/bin/env python3
# coding: utf-8

""" AGO pipeline main script"""

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "1.0"
__status__    = "Released"

import sys

from AGO_parameters import Parameters
from AGO_utils import (
    create_parameters_file,
    create_slurm_script,
    create_bash_script,
    check_results,
    clean_results,
    compute_statistics
)

CMD = {
    'slurm': create_slurm_script,
    'bash': create_bash_script,    
    'check': check_results,
    'clean': clean_results,
    'stats': compute_statistics
}

# MAIN --------------------------------------------------------------------------

def main():
    parameters_file = sys.argv[1]
    command = sys.argv[2]

    if command == 'create':
        header_file = sys.argv[3]
        yaml_dir = sys.argv[4]
        tools_list = sys.argv[5:]
        create_parameters_file(header_file, yaml_dir, tools_list, parameters_file)
    elif command == 'init':
        parameters = Parameters(parameters_file)
        parameters.init()
    else:
        tool = sys.argv[3]
        parameters = Parameters(parameters_file)            
        cmd_out = CMD[command](parameters, tool)
        for out_msg in cmd_out:
            print(f'\t{out_msg}')
        
if __name__ == "__main__":
    main()
