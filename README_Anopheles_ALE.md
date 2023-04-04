
Anopheles data, for the 4 assembled species and the X chromosome.

The parameters file is `parameters/Anopheles_ALE_NT.yaml`.
The output root directory is `/scratch/chauvec/SPP`.

```
> source AGO_python3/bin/activate
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/Anopheles_ALE_NT/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/Anopheles_ALE_NT/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/Anopheles_ALE_NT/data/gene_orders_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_ALE_NT/data/species_4.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/Anopheles_ALE_NT/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_ALE_NT/data/alignments_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_ALE_NT/data/gene_trees.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_ALE_NT/data/reconciled_species_file.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_ALE_NT/data/adjacencies_X_4.txt will be computed.
> wc -l /scratch/chauvec/SPP/Anopheles_ALE_NT/data/families_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_ALE_NT/data/families_X_4.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_ALE_NT/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_ALE_NT/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64153898
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml check MACSE
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_ALE_NT/log/MACSE.log
```

### IQ-TREE

### ALE

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml script DeCoSTAR
> sbatch /scratch/chauvec/SPP/Anopheles_ALE_NT/aux/DeCoSTAR/DeCoSTAR.sh
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml check DeCoSTAR
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml stats DeCoSTAR
```

### SPPDCJ
We consider only the three ingroup species as node_0 has almost no signal.

```
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml script SPPDCJ_ILP
> sbatch  /scratch/chauvec/SPP/Anopheles_ALE_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_ingroups.sh
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml check SPPDCJ_ILP
> cat /scratch/chauvec/SPP/Anopheles_ALE_NT/log/SPPDCJ_ILP_ingroups.log
> cat /scratch/chauvec/SPP/Anopheles_ALE_NT/log/SPPDCJ_ILP/SPPDCJ_ILP_ingroups.err
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml stats SPPDCJ_ILP
> python src/AGO.py parameters/Anopheles_ALE_NT.yaml script SPPDCJ
> sbatch /scratch/chauvec/SPP/Anopheles_ALE_NT/aux/SPPDCJ/SPPDCJ_ingroups.sh
```
