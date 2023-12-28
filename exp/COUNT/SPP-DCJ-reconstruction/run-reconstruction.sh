#!/bin/sh

COUNT_DATA_DIR=../Anopheles
RAW_DATA_DIR=../../../data/VectorBase
SPP_DCJ_BIN=./spp_dcj_v2/scripts
THREADS=8
MIN_SIZE=5

echo "reformat weight table (weights.formatted.tsv)"
./reformat_weight_table.py weights.tsv > weights.formatted.tsv
echo "produce adjacencies file (adjacencies.txt)"
$SPP_DCJ_BIN/count2adjacencies.py -p weights.formatted.tsv $RAW_DATA_DIR/species_tree_4.newick $COUNT_DATA_DIR/X_2_AsymmetricWagner.family.csv $RAW_DATA_DIR/families_X_2.txt $RAW_DATA_DIR/gene_orders_X_2.rel.txt > adjacencies.txt 2> adjacencies.log

echo "prepare input files for SPP-DCJ (X_2_AsymmetricWagner.family.clean.tsv, species_tree_4.tsv)"
cut -f-8 $COUNT_DATA_DIR/X_2_AsymmetricWagner.family.csv > X_2_AsymmetricWagner.family.clean.csv
$SPP_DCJ_BIN/nwk2tabular.py $RAW_DATA_DIR/species_tree_4.newick > species_tree_4.tsv

echo "run SPP-DCJ (X_2_AsymmetricWagner.family.adjacencies.ilp)"
$SPP_DCJ_BIN/spp_dcj.py -r -c X_2_AsymmetricWagner.family.clean.csv -t species_tree_4.tsv adjacencies.txt -m X_2_AsymmetricWagner.family.adjacencies.idmap > X_2_AsymmetricWagner.family.adjacencies.ilp 2> X_2_AsymmetricWagner.family.adjacencies.sppdcj.log

echo "run gurobi (X_2_AsymmetricWagner.family.adjacencies.sol)"
# clear log file
echo > X_2_AsymmetricWagner.family.adjacencies.gurobi.log
gurobi_cl Threadss=$THREADS ResultFile=X_2_AsymmetricWagner.family.adjacencies.sol LogFile=X_2_AsymmetricWagner.family.adjacencies.gurobi.log X_2_AsymmetricWagner.family.adjacencies.ilp

echo "extract adjacencies (X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.tsv)"
$SPP_DCJ_BIN/sol2adjacencies.py X_2_AsymmetricWagner.family.adjacencies.sol X_2_AsymmetricWagner.family.adjacencies.idmap > X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.tsv 2> X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.log

echo "produce UniMoG file (X_2_AsymmetricWagner.family.adjacencies.sol.unimog.tsv)"
$SPP_DCJ_BIN/sol2unimog.py X_2_AsymmetricWagner.family.adjacencies.sol X_2_AsymmetricWagner.family.adjacencies.idmap > X_2_AsymmetricWagner.family.adjacencies.sol.unimog.tsv 2> X_2_AsymmetricWagner.family.adjacencies.sol.unimog.log

echo "visualize reconstructed genomes (X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.pdf), omitting components smaller $MIN_SIZE"
$SPP_DCJ_BIN/visualize_genomes.py -o $MIN_SIZE X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.tsv 2>&1 > X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.pdf | tee X_2_AsymmetricWagner.family.adjacencies.sol.adjacencies.log
