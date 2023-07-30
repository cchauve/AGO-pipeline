#!/bin/bash

source ../config.sh
EXP_NAME=exp_2
TMP_EXP_DIR=${OMA_TMP_DIR}/${EXP_NAME}
cd ${TMP_EXP_DIR}

sbatch --account=def-chauvec --array=1-100 --time=16:00:00 --mem=8G --output=log/OMA2_%A_%a.out --error=log/OMA2_%A_%a.err --job-name=OMA2 -N1 <<EOF
#!/bin/sh 
export NR_PROCESSES=100
${OMA_PATH}/oma -s
EOF
