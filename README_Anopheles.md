
`Sat Mar 18 09:16:35 PDT 2023`

The parameters file is `parameters/Anopheles_GeneRax_NT.yaml`.
The output root directory is `/scratch/chauvec/SPP`.

```
> cd /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase
> ln -s families_X.txt families.txt
> ln -s gene_orders_X.txt gene_orders.txt
> ln -s sequences_X.txt sequences.txt
> cd /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/
```

```
> source AGO_python3/bin/activate
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml init
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/species_tree.newick -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/species_tree.newick.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/families.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families.txt.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/gene_orders.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/gene_orders.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/species.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase/sequences.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/sequences.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/alignments.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/tree_inference.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies.txt will be computed.
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families.txt
606 /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62862555
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/alignments.txt
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
1
```

### GeneRax

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62872666
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_families.csv
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
0
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations.txt
605 /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations.txt
```

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62883101
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/DeCoSTAR.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats DeCoSTAR
```

### SPPDCJ

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ_ILP
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check SPPDCJ_ILP
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP_all_species.log
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats SPPDCJ_ILP
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ/SPPDCJ_all_species.sh
```
