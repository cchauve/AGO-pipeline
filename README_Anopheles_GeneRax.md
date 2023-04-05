Anopheles data, for the 4 assembled species and the X chromosome.

The parameters file is `parameters/Anopheles_GeneRax_NT.yaml`.
The output root directory is `/scratch/chauvec/SPP`.

```
> source AGO_python3/bin/activate
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/gene_orders_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/species_4.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/alignments_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/gene_trees.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciled_species_file.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies_X_4.txt will be computed.
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families_X_4.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64257173
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/alignments_X_4.txt
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
0
```

### GeneRax

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64272604
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
0
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_families.csv
> m /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_species.csv
```


### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64273185
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/DeCoSTAR.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
```

### SPPDCJ

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_all.sh
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_all.sh
sbatch: NOTE: Your memory request of 262144M was likely submitted as 256G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64274354
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP_all.log
        No output file is created
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP_all.log
#status tool    index   message
SUCCESS SPPDCJ_ILP              /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/SPPDCJ_ILP/all_0.5_0.5_0.25.idmap
SUCCESS SPPDCJ_ILP              /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/SPPDCJ_ILP/all_0.5_0.5_0.25.ilp
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP/SPPDCJ_ILP_all.err
INFO    2023-04-04 18:39:07,735 loading species tree from /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/species_tree_all.txt
INFO    2023-04-04 18:39:07,745 loading candidate adjacencies from /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/adjacencies_complemented_all.txt, using "_" to separate gene family from uniquifying identifier
INFO    2023-04-04 18:39:07,810 identified 214 candidate telomeres in genome node2
INFO    2023-04-04 18:39:07,812 identified 210 candidate telomeres in genome node1
INFO    2023-04-04 18:39:07,812 identified 2 candidate telomeres in genome AnophelesalbimanusSTECLA
INFO    2023-04-04 18:39:07,813 identified 116 candidate telomeres in genome node0
INFO    2023-04-04 18:39:07,813 identified 2 candidate telomeres in genome AnophelesatroparvusEBRO
INFO    2023-04-04 18:39:07,813 identified 2 candidate telomeres in genome AnophelesgambiaePEST
INFO    2023-04-04 18:39:07,814 identified 2 candidate telomeres in genome AnophelesfunestusFUMOZ
INFO    2023-04-04 18:39:07,814 constructing relational diagrams for all 6 branches of the tree
INFO    2023-04-04 18:39:11,425 identified 0 circular singleton candidates
INFO    2023-04-04 18:39:11,455 identified 0 circular singleton candidates
INFO    2023-04-04 18:39:11,487 identified 0 circular singleton candidates
INFO    2023-04-04 18:39:11,520 identified 0 circular singleton candidates
INFO    2023-04-04 18:39:11,544 identified 1 circular singleton candidates
INFO    2023-04-04 18:39:11,567 identified 0 circular singleton candidates
INFO    2023-04-04 18:39:11,571 writing objective over all graphs
INFO    2023-04-04 18:39:12,060 writing constraints...
INFO    2023-04-04 18:39:12,060 writing constraints for relational diagram of node0 and AnophelesfunestusFUMOZ
INFO    2023-04-04 18:39:12,344 writing constraints for relational diagram of node0 and AnophelesgambiaePEST
INFO    2023-04-04 18:39:12,639 writing constraints for relational diagram of node1 and AnophelesatroparvusEBRO
INFO    2023-04-04 18:39:13,130 writing constraints for relational diagram of node1 and node0
INFO    2023-04-04 18:39:13,572 writing constraints for relational diagram of node2 and AnophelesalbimanusSTECLA
INFO    2023-04-04 18:39:14,136 writing constraints for relational diagram of node2 and node1
INFO    2023-04-04 18:39:15,102 writing domains...
INFO    2023-04-04 18:39:15,102 writing domains for relational diagram of node0 and AnophelesfunestusFUMOZ
INFO    2023-04-04 18:39:15,104 writing domains for relational diagram of node0 and AnophelesgambiaePEST
INFO    2023-04-04 18:39:15,106 writing domains for relational diagram of node1 and AnophelesatroparvusEBRO
INFO    2023-04-04 18:39:15,109 writing domains for relational diagram of node1 and node0
INFO    2023-04-04 18:39:15,111 writing domains for relational diagram of node2 and AnophelesalbimanusSTECLA
INFO    2023-04-04 18:39:15,113 writing domains for relational diagram of node2 and node1
INFO    2023-04-04 18:39:15,115 writing variables...
INFO    2023-04-04 18:39:15,115 writing general variables for relational diagram of node0 and AnophelesfunestusFUMOZ
INFO    2023-04-04 18:39:15,116 writing general variables for relational diagram of node0 and AnophelesgambiaePEST
INFO    2023-04-04 18:39:15,118 writing general variables for relational diagram of node1 and AnophelesatroparvusEBRO
INFO    2023-04-04 18:39:15,120 writing general variables for relational diagram of node1 and node0
INFO    2023-04-04 18:39:15,121 writing general variables for relational diagram of node2 and AnophelesalbimanusSTECLA
INFO    2023-04-04 18:39:15,123 writing general variables for relational diagram of node2 and node1
INFO    2023-04-04 18:39:15,125 writing binary variables for relational diagram of node0 and AnophelesfunestusFUMOZ
INFO    2023-04-04 18:39:15,162 writing binary variables for relational diagram of node0 and AnophelesgambiaePEST
INFO    2023-04-04 18:39:15,199 writing binary variables for relational diagram of node1 and AnophelesatroparvusEBRO
INFO    2023-04-04 18:39:15,260 writing binary variables for relational diagram of node1 and node0
INFO    2023-04-04 18:39:15,319 writing binary variables for relational diagram of node2 and AnophelesalbimanusSTECLA
INFO    2023-04-04 18:39:15,383 writing binary variables for relational diagram of node2 and node1
INFO    2023-04-04 18:39:15,543 writing ID-to-gene extremity mapping to /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/SPPDCJ_ILP/all_0.5_0.5_0.25.idmap
INFO    2023-04-04 18:39:15,559 DONE
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/SPPDCJ_ILP/components_all.log
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ/SPPDCJ_all.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ/SPPDCJ_all.sh
Submitted batch job 64275505
```

