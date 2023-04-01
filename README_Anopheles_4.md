
`Sun Mar 19 14:34:24 PDT 2023`

Anopheles data, for the 4 assembled species and the X chromosome.

The parameters file is `parameters/Anopheles_GeneRax_NT_4.yaml`.
The output root directory is `/scratch/chauvec/SPP`.

```
> source AGO_python3/bin/activate
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml init
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/gene_orders_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/species_4.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/alignments_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/tree_inference_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/adjacencies_X_4.txt will be computed.
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/families_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/families_X_4.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 63752686
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/MACSE.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/alignments_X_4.txt
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/MACSE.log
0
```

### GeneRax

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/GeneRax/GeneRax.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/GeneRax/GeneRax.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 63812158
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/GeneRax.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/GeneRax/GeneRax_families.csv
> m /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses
node_2:492:41:0
Anopheles_gambiae_PEST:471:6:30
Anopheles_funestus_FUMOZ:472:2:25
node_0:495:0:34
Anopheles_atroparvus_EBRO:503:16:42
node_1:529:37:0
Anopheles_albimanus_STECLA:489:8:11
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/GeneRax.log
0
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt
```

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/DeCoSTAR/DeCoSTAR.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 63829230
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/DeCoSTAR.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/adjacencies_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
```

### SPPDCJ
We consider only the three ingroup species as node_0 has almost no signal.

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_ingroups.sh
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_ingroups.sh
sbatch: NOTE: Your memory request of 262144M was likely submitted as 256G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 63925788
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check SPPDCJ_ILP
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/SPPDCJ_ILP_all_species.log
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/SPPDCJ_ILP/SPPDCJ_ILP_all_species.err
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats SPPDCJ_ILP
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ/SPPDCJ_ingroups.sh
```

