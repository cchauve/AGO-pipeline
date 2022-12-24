#!/bin/bash

#SBATCH --time=XX_sppdcj_ilp_time
#SBATCH --mem=XX_sppdcj_ilp_memory
#SBATCH --account=XX_slurm_account
#SBATCH --output=XX_sppdcj_log_dir/XX_sppdcj_log_pref_ILP.log
#SBATCH --error=XX_sppdcj_log_dir/XX_sppdcj_log_pref_ILP.err

python3 XX_tools_dir/spp_dcj/scripts/spp_dcj.py -m XX_sppdcj_idmap_file -a XX_sppdcj_alpha -b XX_sppdcj_beta XX_sppdcj_ilp_options XX_sppdcj_species_tree_file XX_sppdcj_adjacencies_file


