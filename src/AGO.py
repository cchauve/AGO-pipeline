#!/usr/bin/env python3
# coding: utf-8

""" AGO pipeline main script"""

__author__    = "Cedric Chauve"
__email__     = "cedric.chauve@sfu.ca"
__version__   = "0.99"
__status__    = "Development"

import sys

from AGO_parameters import Parameters
from AGO_utils import (
    create_slurm_script,
    check_slurm_results,
    clean_slurm_results,
    compute_statistics
)

CMD = {
    'script': create_slurm_script,
    'check': check_slurm_results,
    'clean': clean_slurm_results,
    'stats': compute_statistics
}

# MAIN --------------------------------------------------------------------------

def main():
    parameters_file = sys.argv[1]
    parameters = Parameters(parameters_file)
    command = sys.argv[2]

    if command == 'init':
        parameters.init()
    else:
        tool = sys.argv[3]
        cmd_out = CMD[command](parameters, tool)
        for out_msg in cmd_out:
            print(f'\t{out_msg}')
        
if __name__ == "__main__":
    main()
