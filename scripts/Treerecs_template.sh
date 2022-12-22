#!/bin/bash

#SBATCH --time=XX_treerecs_time
#SBATCH --mem=XX_treerecs_memory
#SBATCH --account=XX_slurm_account
#SBATCH --array=1-XX_families_nb
#SBATCH --output=XX_treerecs_log_dir/XX_treerecs_log_pref_%a.log
#SBATCH --error=XX_treerecs_log_dir/XX_treerecs_log_pref_%a.err

FAMILY_ID=$(sed "${SLURM_ARRAY_TASK_ID}q;d" XX_families_file | cut -f 1)
echo "SLURM_ARRAY_TASK_ID:${SLURM_ARRAY_TASK_ID} FAMILY_ID:${FAMILY_ID}"

XX_tools_dir/treerecs -s XX_species_tree -g XX_generax_results_dir/reconciliations/${FAMILY_ID}_reconciliated.nhx -S XX_treerecs_map_file_prefix_${FAMILY_ID}  -o XX_treerecs_results_dir XX_treerecs_options
