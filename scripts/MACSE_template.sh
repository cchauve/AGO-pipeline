#!/bin/bash

#SBATCH --time=XX_macse_time
#SBATCH --mem=XX_macse_memory
#SBATCH --account=XX_slurm_account
#SBATCH --array=1-XX_families_nb
#SBATCH --output=XX_macse_log_dir/XX_macse_log_pref_%a.log
#SBATCH --error=XX_macse_log_dir/XX_macse_log_pref_%a.err

module load java

FAMILY_ID=$(sed "${SLURM_ARRAY_TASK_ID}q;d" XX_families_file | cut -f 1)
echo "SLURM_ARRAY_TASK_ID:${SLURM_ARRAY_TASK_ID} FAMILY_ID:${FAMILY_ID}"

java -jar XX_tools_dir/macse_v2.06.jar -prog alignSequences -seq XX_genes_dir/${FAMILY_ID}.fasta -out_NT XX_macse_results_dir/${FAMILY_ID}_NT.fasta -out_AA XX_macse_results_dir/${FAMILY_ID}_AA.fasta
