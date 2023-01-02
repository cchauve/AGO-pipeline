# SPP-DCJ Pipeline
### Evan Cribbie, Cedric Chauve.

## Data

```python3 scripts/import_YGOB_data.py > log/YGOB_test1/import_data.log```  

Families were labeled from 1 increasingly.
Family `352` was renamed `10352` for robustness checking.
Family `353` was renamed `353a` for the same purpose.  

This script imports already filtered data from Evan's
directory. Ideally we should have two scripts to (1) import data from
the YGOB website and generates statistics and (2) filter data from
users choices.  

The first script should be parameterized by an optional list of
species and download only data files for the selected species and
filter the species tree to include only the considered species.  

The second script shoud be parameterized by a min/max thresholds for
the size of gene families. It would then filter gene families to the
ones not in the size range.  

## Pipeline

The parameters file is `parameters/YGOB_test2_NT.yml`. As I had spaces issues,
I have set the output directories (log and results) in
`/scratch/chauvec/SPP`.

The principle of the pipeline is that all computations are specified in the
parameters file.

Scripts that are independent of the tools used as ins `src`.

Scripts specific to tools (such as creating the input files, formatting the
output, computing statistics) are in `scripts`.

```
source AGO_python3/bin/activate
python3 src/AGO_pipeline.py parameters/YGOB_test2_NT.yml init
> source AGO_python3/bin/activate
> python src/AGO.py parameters/YGOB_test2_NT.yaml init
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/YGOB/species_tree.newick -> /scratch/chauvec/SPP/YGOB_test2_NT/data/species_tree.newick.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/YGOB/families.txt -> /scratch/chauvec/SPP/YGOB_test2_NT/data/families.txt.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/YGOB/gene_orders.txt -> /scratch/chauvec/SPP/YGOB_test2_NT/data/gene_orders.txt.
        /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/YGOB/sequences.txt -> /scratch/chauvec/SPP/YGOB_test2_NT/data/sequences.txt.
        reconciliations.txt will be computed.
> wc -l /scratch/chauvec/SPP/YGOB_test2_NT/data/families.txt
5028 /scratch/chauvec/SPP/YGOB_test2_NT/data/families.txt
```

We start with 5028 families.  

### MACSE

```
> python src/AGO.py parameters/YGOB_test2_NT.yaml script MACSE
        /scratch/chauvec/SPP/YGOB_test2_NT/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/YGOB_test2_NT/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 54943853
> python src/AGO.py parameters/YGOB_test2_NT.yaml check MACSE
        /scratch/chauvec/SPP/YGOB_test2_NT/log/MACSE.log
        /scratch/chauvec/SPP/YGOB_test2_NT/data/alignments.txt
```

Log files are available at
`/scratch/chauvec/SPP/YGOB_test2_NT/log/MACSE.log`
and `/scratch/chauvec/SPP/YGOB_test2_NT/log/MACSE/*.[log,err].  

```
grep -c "ERROR" /scratch/chauvec/SPP/YGOB_test2_NT/log/MACSE.log
7
```

There are 7 families that were not aligned. We leave it as is to
test the robustness of the pipeline to intermediate computations
failing on some families.  

We now have 5021 families. 

### GeneRax

```
> python src/AGO.py parameters/YGOB_test2_NT.yaml script GeneRax
        /scratch/chauvec/SPP/YGOB_test2_NT/aux/GeneRax/GeneRax.sh
> sbatch /scratch/chauvec/SPP/YGOB_test2_NT/aux/GeneRax/GeneRax.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 54957315
> python src/AGO.py parameters/YGOB_test2_NT.yaml check GeneRax
        /scratch/chauvec/SPP/YGOB_test2_NT/log/GeneRax.log
        /scratch/chauvec/SPP/YGOB_test2_NT/data/reconciliations.txt
> python src/AGO.py parameters/YGOB_test2_NT.yaml stats GeneRax
        /scratch/chauvec/SPP/YGOB_test2_NT/statistics/GeneRax/GeneRax.csv

```

Log and error files are available at
`/scratch/chauvec/SPP/YGOB_test2_NT/log/GeneRax.log` and
`/scratch/chauvec/SPP/YGOB_test2_NT/log/GeneRax/*.[log,err]`.

```
> grep -c "ERROR" /scratch/chauvec/SPP/YGOB_test2_NT/log/GeneRax.log
194
```

There are 194 families for which GeneRax could not read the alignment
or mape genes to species.


```
> wc -l /scratch/chauvec/SPP/YGOB_test2_NT/data/reconciliations.txt
4827 /scratch/chauvec/SPP/YGOB_test2_NT/data/reconciliations.txt
```

We now have 4827 families for which the reconciled trees are in a
recPhyloXML format that can be read by DeCoSTAR.  

In `/scratch/chauvec/SPP/YGOB_test2_NT/statistics/GeneRax/GeneRax.csv`
we can observe again a gene content inflation in reconciled gene trees 
obtained with GeneRax.  


### DeCoSTAR

```
> python src/AGO.py parameters/YGOB_test2_NT.yaml script DeCoSTAR
        /scratch/chauvec/SPP/YGOB_test2_NT/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch /scratch/chauvec/SPP/YGOB_test2_NT/aux/DeCoSTAR/DeCoSTAR.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 54997458
> python src/AGO.py parameters/YGOB_test2_NT.yaml check DeCoSTAR
        /scratch/chauvec/SPP/YGOB_test2_NT/log/DeCoSTAR.log
        /scratch/chauvec/SPP/YGOB_test2_NT/aux/DeCoSTAR/DeCoSTAR_dummy_output.txt
> python src/AGO.py parameters/YGOB_test2_NT.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/YGOB_test2_NT/statistics/DeCoSTAR/DeCoSTAR.csv
```

DeCoSTAR ran without any issue. From the statistics file
`/scratch/chauvec/SPP/YGOB_test2_NT/statistics/DeCoSTAR/DeCoSTAR.csv`
we decide to create an ILP for adjacencies of weight at least 0.75.

### SPPDCJ: creating the ILP

```
> python src/AGO.py parameters/YGOB_test2_NT.yaml script SPPDCJ_ILP
        /scratch/chauvec/SPP/YGOB_test2_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
> sbatch  /scratch/chauvec/SPP/YGOB_test2_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
sbatch: NOTE: Your memory request of 262144M was likely submitted as 256G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 55016665
```

The ILP creation is currently running.