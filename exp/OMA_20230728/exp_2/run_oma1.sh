#!/bin/bash
#SBATCH --mem=4G
#SBATCH --time=8:00:00
#SBATCH --account=def-chauvec
#SBATCH --output=log/OMA1.out
#SBATCH --error=log/OMA1.err
#SBATCH --job-name=OMA1

source ../config.sh
EXP_NAME=exp_2

TMP_EXP_DIR=${OMA_TMP_DIR}/${EXP_NAME}
mkdir -p ${TMP_EXP_DIR}

SEQ_FILE=${DATA_DIR}/sequences_ALL_2.txt
rm -rf ${TMP_EXP_DIR}/DB
mkdir -p ${TMP_EXP_DIR}/DB
FASTA_FILES=`cut -f2 ${SEQ_FILE}`
for FASTA_FILE in ${FASTA_FILES}
do
    SPECIES=`basename ${FASTA_FILE} .fasta`
    cp ${FASTA_FILE} ${TMP_EXP_DIR}/DB/${SPECIES}.fa
done

cp parameters.drw ${TMP_EXP_DIR}/
cd ${TMP_EXP_DIR}
rm -rf Cache
${OMA_PATH}/oma -c 
