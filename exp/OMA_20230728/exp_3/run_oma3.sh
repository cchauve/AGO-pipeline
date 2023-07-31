#!/bin/bash
#SBATCH --mem=16G
#SBATCH --time=8:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=log/OMA3.out
#SBATCH --error=log/OMA3.err
#SBATCH --job-name=OMA3

source ../config.sh
EXP_NAME=exp_3

TMP_EXP_DIR=${OMA_TMP_DIR}/${EXP_NAME}
cd ${TMP_EXP_DIR}
${OMA_PATH}/oma

OUT_EXP_DIR=${OMA_OUT_DIR}/${EXP_NAME}
rm -rf ${OUT_EXP_DIR}/results
mkdir -p ${OUT_EXP_DIR}/results
cp -pr ${TMP_EXP_DIR}/results/* ${OUT_EXP_DIR}/results/
python ${SCRIPTS_DIR}/OMA_reformat.py ${OUT_EXP_DIR}/results/OrthologousGroups.txt ${OUT_EXP_DIR}/families.txt
