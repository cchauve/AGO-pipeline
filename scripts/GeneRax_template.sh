#!/bin/bash

#SBATCH --time=XX_generax_time
#SBATCH --mem-per-cpu=XX_generax_memory
#SBATCH --account=XX_slurm_account
#SBATCH --ntasks=XX_generax_ntasks
#SBATCH --output=XX_generax_log_dir/XX_generax_log_pref.log
#SBATCH --error=XX_generax_log_dir/XX_generax_log_pref.err

mpiexec -np XX_generax_ncores XX_tools_dir/GeneRax/build/bin/generax -f XX_generax_aux_dir/XX_generax_families -s XX_species_tree -p XX_generax_results_dir XX_generax_options --seed XX_generax_seed --rec-model XX_generax_model --strategy XX_generax_strategy
