#!/bin/bash
#SBATCH --mem=100G
#SBATCH --time=36:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=log/proteinortho3.out
#SBATCH --error=log/proteinortho3.err
#SBATCH --job-name=proteinortho3

source ../config.sh
EXP_NAME=exp_2
TMP_EXP_DIR=${PO_TMP_DIR}/${EXP_NAME}
OUT_EXP_DIR=${PO_OUT_DIR}/${EXP_NAME}
rm -rf ${OUT_EXP_DIR}/results
mkdir -p ${OUT_EXP_DIR}/results

module load StdEnv/2020  gcc/9.3.0 blast+/2.14.0

cd ${TMP_EXP_DIR}
${PO_PATH}/proteinortho6.pl \
    --project=results --p=blastp+ --clean --step=3 DB/*faa

cp results.proteinortho-graph ${OUT_EXP_DIR}/results/
cp results.proteinortho.tsv ${OUT_EXP_DIR}/results/
cp results.proteinortho.html ${OUT_EXP_DIR}/results/
python ${SCRIPTS_DIR}/proteinortho_reformat.py ${OUT_EXP_DIR}/results/results.proteinortho.tsv ${OUT_EXP_DIR}/families.txt
