
`Sun Mar 19 14:34:24 PDT 2023`

Anopheles data, for the 4 assembled species and the X chromosome.

The parameters file is `parameters/Anopheles_GeneRax_NT_4.yaml`.
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
548 /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/families_X_4.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 62956523
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check MACSE
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/MACSE.log
```

### GeneRax

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script GeneRax
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/GeneRax/GeneRax.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check GeneRax
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats GeneRax
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/GeneRax.log
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/data/reconciliations.txt
```

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script DeCoSTAR
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/DeCoSTAR/DeCoSTAR.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check DeCoSTAR
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats DeCoSTAR
```

### SPPDCJ

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ_ILP
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ_ILP/SPPDCJ_ILP_all_species.sh
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml check SPPDCJ_ILP
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/log/SPPDCJ_ILP_all_species.log
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml stats SPPDCJ_ILP
> python src/AGO.py parameters/Anopheles_GeneRax_NT_4.yaml script SPPDCJ
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT_4/aux/SPPDCJ/SPPDCJ_all_species.sh
```
