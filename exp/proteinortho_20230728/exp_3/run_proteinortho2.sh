#!/bin/bash
#SBATCH --mem=16G
#SBATCH --time=8:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=log/proteinortho2_%A_%a.out
#SBATCH --error=log/proteinortho2_%A_%a.err
#SBATCH --job-name=proteinortho2
#SBATCH --array=1-6

source ../config.sh
EXP_NAME=exp_3
TMP_EXP_DIR=${PO_TMP_DIR}/${EXP_NAME}

module load StdEnv/2020  gcc/9.3.0 blast+/2.14.0

cd ${TMP_EXP_DIR}
${PO_PATH}/proteinortho6.pl \
	  --project=results --p=blastp+ --step=2 \
	  --jobs=${SLURM_ARRAY_TASK_ID}/6 DB/*faa
