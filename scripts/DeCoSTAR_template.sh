#!/bin/bash

#SBATCH --time=XX_decostar_time
#SBATCH --mem=XX_decostar_memory
#SBATCH --account=XX_slurm_account
#SBATCH --output=XX_decostar_log_dir/XX_decostar_log_pref.log
#SBATCH --error=XX_decostar_log_dir/XX_decostar_log_pref.err

XX_tools_dir/DeCoSTAR parameter.file=XX_decostar_parameters_file
