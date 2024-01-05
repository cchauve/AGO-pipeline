python src/AGO.py tests/anopheles_X_2_IQTREE.yaml create tests/anopheles_X_2_IQTREE_header.yaml parameters MACSE IQ-TREE ALE DeCoSTAR SPPDCJ
python src/AGO.py tests/anopheles_X_2_IQTREE.yaml init
python src/AGO.py tests/anopheles_X_2_IQTREE.yaml slurm MACSE
sbatch /scratch/chauvec/SPP/anopheles_X_2_IQTREE/aux/MACSE/MACSE.sh
python src/AGO.py tests/anopheles_X_2_IQTREE.yaml check MACSE
python src/AGO.py tests/anopheles_X_2_IQTREE.yaml slurm IQ-TREE
sbatch /scratch/chauvec/SPP/anopheles_X_2_IQTREE/aux/IQ-TREE/IQ-TREE.sh
python src/AGO.py tests/anopheles_X_2_IQTREE.yaml check IQ-TREE
