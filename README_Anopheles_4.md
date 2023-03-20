
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
559 /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/families_X_4.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62960122
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
Submitted batch job 62962473
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/GeneRax.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/GeneRax/GeneRax_families.csv
> m /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses
node_2:551:45:0
Anopheles_gambiae_PEST:568:8:47
Anopheles_funestus_FUMOZ:584:9:32
node_0:607:3:41
Anopheles_atroparvus_EBRO:581:19:81
node_1:643:42:1
Anopheles_albimanus_STECLA:548:9:12
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/GeneRax.log
0
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt
559 /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations_X_4.txt
```

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/DeCoSTAR/DeCoSTAR.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62962707
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/DeCoSTAR.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/adjacencies_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/statistics/DeCoSTAR/DeCoSTAR_0.4_conflicts.txt
```

### SPPDCJ

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
sbatch: NOTE: Your memory request of 262144M was likely submitted as 256G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62963704
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/SPPDCJ_ILP_all_species.log
        No output file is created
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/SPPDCJ_ILP_all_species.log
#status tool    index   message
SUCCESS SPPDCJ_ILP              /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/results/SPPDCJ_ILP/all_species_0.4_0.5_0.25.idmap
SUCCESS SPPDCJ_ILP              /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/results/SPPDCJ_ILP/all_species_0.4_0.5_0.25.ilp
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP/SPPDCJ_ILP_all_species.err
INFO    2023-03-18 19:46:57,106 loading species tree from /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/species_tree_all_species.txt
INFO    2023-03-18 19:46:57,126 loading candidate adjacencies from /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/adjacencies_complemented_all_species.txt
INFO    2023-03-18 19:46:57,232 identified 260 candidate telomeres in genome node_5
INFO    2023-03-18 19:46:57,235 identified 268 candidate telomeres in genome node_4
INFO    2023-03-18 19:46:57,235 identified 2 candidate telomeres in genome Anopheles_albimanus_STECLA
INFO    2023-03-18 19:46:57,238 identified 244 candidate telomeres in genome node_3
INFO    2023-03-18 19:46:57,238 identified 2 candidate telomeres in genome Anopheles_atroparvus_EBRO
INFO    2023-03-18 19:46:57,240 identified 192 candidate telomeres in genome node_2
INFO    2023-03-18 19:46:57,240 identified 36 candidate telomeres in genome Anopheles_farauti_FAR1
INFO    2023-03-18 19:46:57,241 identified 16 candidate telomeres in genome node_0
INFO    2023-03-18 19:46:57,242 identified 78 candidate telomeres in genome node_1
INFO    2023-03-18 19:46:57,242 identified 2 candidate telomeres in genome Anopheles_gambiae_PEST
INFO    2023-03-18 19:46:57,242 identified 26 candidate telomeres in genome Anopheles_coluzzii_Ngousso
INFO    2023-03-18 19:46:57,242 identified 2 candidate telomeres in genome Anopheles_funestus_FUMOZ
INFO    2023-03-18 19:46:57,243 identified 14 candidate telomeres in genome Anopheles_minimus_MINIMUS1
INFO    2023-03-18 19:46:57,243 constructing relational diagrams for all 12 branches of the tree
INFO    2023-03-19 17:23:35,245 identified 5 circular singleton candidates
INFO    2023-03-19 17:27:09,149 identified 0 circular singleton candidates
INFO    2023-03-19 17:27:38,880 identified 4 circular singleton candidates
INFO    2023-03-19 17:27:55,834 identified 5 circular singleton candidates
slurmstepd: error: *** JOB 62889614 ON cdr811 CANCELLED AT 2023-03-19T19:46:53 DUE TO TIME LIMIT ***
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats SPPDCJ_ILP
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ/SPPDCJ_all_species.sh
```

Retried with a time limit of 72h00.

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
sbatch: NOTE: Your memory request of 262144M was likely submitted as 256G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 63026147
```
