#!/bin/bash
#SBATCH --mem=8G
#SBATCH --time=2:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=log/proteinortho1.out
#SBATCH --error=log/proteinortho1.err
#SBATCH --job-name=proteinortho1

source ../config.sh
EXP_NAME=exp_2

TMP_EXP_DIR=${PO_TMP_DIR}/${EXP_NAME}
mkdir -p ${TMP_EXP_DIR}

SEQ_FILE=${DATA_DIR}/sequences_ALL_2.txt
rm -rf ${TMP_EXP_DIR}/DB
mkdir -p ${TMP_EXP_DIR}/DB
FASTA_FILES=`cut -f2 ${SEQ_FILE}`
for FASTA_FILE in ${FASTA_FILES}
do
    SPECIES=`basename ${FASTA_FILE} .fasta`
    cp ${FASTA_FILE} ${TMP_EXP_DIR}/DB/${SPECIES}.faa
done

module load StdEnv/2020  gcc/9.3.0 blast+/2.14.0

cd ${TMP_EXP_DIR}
${PO_PATH}/proteinortho6.pl \
	  --project=results --p=blastp+ --step=1 DB/*faa
