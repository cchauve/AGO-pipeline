# Reconstructing Anopheles ancestral X chromosome gene orders

## Overview

This directory contains parameters files for the AGO pipeline aimed at
reconstructing the ancestral gene orders of the X chromosomes for
three ancestral *Anopheles* mosquito species.

The ancestral gene orders are reconstructed according to three different versions of the pipeline, in order to illustrate the modularity of the pipeline:
- all three approaches start from the same data, described in the section Data below;
- all three approaches rely on Multiple Sequences Alignments (MSA) for the gene families obtained with the tool `MACSE`;
- the first approach computes reconciled gene trees from the MSAs using the tool `GeneRax`;
- the second approach computes gene trees samples using the tool `IQ-TREE` and reconciled gene tres from these gene trees using the tool `ALE`;
- the third approach computes reconciled gene trees from the `IQ-TREE` gene trees samples using the tool `ecceTERA` implemented in `DeCoSTAR`;
- all three approaches computes ancestral gene adjacencies candidates using `DeCoSTAR` and remove conflicts from these adjacencies using the tool `spp_dcj`.

In order to run `spp_dcj`, the optimization solver `gurobi` is used,
that requires a local license; we refer to <a
href="https://www.gurobi.com/academia/academic-program-and-licenses/">Get
the License That’s Right for You</a> for a description of how to
obtain a (free for academics) license. If you run AGO on a HPC
cluster, we recommend that you contact your system administrators in
order to obtain a cluster license for Gurobi.

The provided parameters files are written to run the AGO pipeline on
the `cedar` HPC cluster of the <a
href="https://alliancecan.ca/en">Digital Research Alliance of
Canada</a> using the `slurm` job scheduling system.

## Data

The data needed to run the experiments are located in [data/VectorBase](../data/VectorBase/).

This dataset focuses on reconstructing the ancestral gene orders of the X chromosomes for
three ancestral *Anopheles* mosquito species, defined as the ancestors of the following extant *Anopheles* species:
*Anopheles gambiae PEST, Anopheles atroparvus EBRO, Anopheles funestus FUMOZ, Anopheles albimanus STECLA*.

The data were obtained from the data repository <a
href="https://vectorbase.org/">VectorBase</a>, as described in
[data/VectorBase/README.md](../data/VectorBase/README.md).

They are composed of
- a species tree with branch lengths, [species tree](../data/VectorBase/species_tree_4.newick);
- 451 gene families containing 1,935 genes [gene families](../data/VectorBase/families_X_4.txt);
- DNA sequences [sequences](../data/VectorBase/sequences_X_4.txt) for all genes, grouped by families.


Note that the sequences file is provided with absolute path with
prefix (`/home/chauvec/projects/ctb-chauvec/`) corresponding to the
experiments that were ran on the `cedar` HPC cluster of the <a
href="https://alliancecan.ca/en">Digital Research Alliance of
Canada</a>; to be reproduced, this prefix will need to be changed.

Similarly, the path to access to the external tools used in the
pipelines (`MACSE`, `GeneRax`, `IQ-TREE`, `ALE`, `DeCoSTAR`,
`spp_dcj`) are provided in the parameters files under the assumption
that all such tools are either available as a module on the
corresponding HPC system or have been installed in the directory
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/bin`): this would
need to be updated to be reproduced on another system.

Finally, all computations we ran within a python 3 virtual environment
`AGO-pipeline` including all the required packages (see
[README.md](../README.md).

## GeneRax-based pipeline

We first create a parameters file for a pipeline that uses, in
sequence, `MACSE` to compute MSAs based on nucleotide sequences,
`GeneRax` to compute reconciled gene tres from these alignments,
`DeCoSTAR` to compute ancestral adjacencies, and `spp_dcj` to compute a
set of conflict-free adjacencies defining ancestral gene orders.

To do so, we first create and edit a copy of [header
template](../parameters/header_template.yaml) into the parameters
header file [GeneRax pipeline
header](anopheles_X_GeneRax_header.yaml).


The root directory where the AGO-pipeline github repo was cloned is
`home/chauvec/projects/ctb-chauvec/AGO-pipeline`.  All external tools
that were not already available on the `cedar` system were installed
locally in the directory `home/chauvec/projects/ctb-chauvec/AGO-pipeline/bin`.

We refer to the comments in the parameters files and the online
documentation of each tool for the specifics of the chosen parameters
chosen for each tool.  Note that in this header file, we edit only the
sections corresponding to the tools that will be used in the pipeline
and delete the sections for unused tools (`IQ-TREE`, `ALE`).

Before creating the pipeline parameters file, we check that the
input data is in correct format and consistent:
```
(AGO-pipeline) > python scripts/data_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt NA NA
SUCCESS SPECIES TREE
SUCCESS FAMILIES
SUCCESS GENE ORDERS
SUCCESS SEQUENCES
```

Then we create the pipeline parameters file:

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml create example/anopheles_X_GeneRax_header.yaml parameters MACSE GeneRax DeCoSTAR SPPDCJ
        example/anopheles_X_GeneRax.yaml
```

The next step was to initialize the pipeline.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/sequences_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/alignments_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/reconciliations_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/adjacencies_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/adjacencies_ago_X.txt will be computed.
```

Then we run in sequence the pipeline tools. First we run `MACSE` to
compute an MSA for each family.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm MACSE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml check MACSE
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/MACSE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/alignments_X.txt
```

This shows that `MACSE` succeeded to compute an MSA for all gene
families. The next step is `GeneRax` to compute reconciled gene trees.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm GeneRax
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml check GeneRax
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/GeneRax.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/reconciliations_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml stats GeneRax
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_families.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses:transfers
node2:492:41:0:0
AnophelesgambiaePEST:471:6:30:0
AnophelesfunestusFUMOZ:472:2:25:0
node0:495:0:34:0
AnophelesatroparvusEBRO:503:16:42:0
node1:529:37:0:0
AnophelesalbimanusSTECLA:489:8:11:0
```

Again, all expected output files are present and there is no error
in running `GeneRax`.
  
We can observe from the statistics that the number of ancestral genes
is slightly higher than the number of extant genes and one can suspect
the well-documented issue of the reconciliation algorithm having a
tendancy to locate duplications higher in the species tree.
  
Next to illustrate the feature that the AGO pipeline tools can be ran
either through `slurm` or a `bash` script, we run `DeCoSTAR` as a bash script,
redirecting the standard output and error output into specific files.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml bash DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > chmod 755 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh 2> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.err 1> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.log
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/DeCoSTAR.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/adjacencies_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml stats DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
(AGO-pipeline) > head -1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv; grep -P ':0.5\t' /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:495:0.5   474:448:33:127
node1:529:0.5   462:368:11:333
node2:492:0.5   331:224:0:536
```

We can observe that `DeCoSTAR` runs with no error. But the statistics
on the resulting ancestral adjacencies show that we can expect highly
fragmented ancestral gene orders, as there is a significant level of
free gene extremities in the ancestral gene adjacencies. The level of
conflict in the ancestral gene adjacencies is howver very low.
  
Finally, we clear the conflict in ancestral adjacencies using
`spp_dcj`. This requires to first compute the Mixed Integer Linear
Program (MILP) and then to solve it using `gurobi`.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ_ILP
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
```
We solve the MILP.
```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/log/SPPDCJ.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/adjacencies_ago_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_GeneRax.yaml stats SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   231:225.74:224:223.24
node1   404:372.4:357:351.14
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   460:436.96:416:409.12
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
```

The `spp_dcj` statistics show that, as expected, very few adjacencies
need to be discarded to clear all conflicts in ancestral
species `node2`, unlike in `node0` and `node1`, but in both cases the
weight of the discarded adjacencies is quite low.


Last we generate from the selected ancestral adjacencies FASTA-like
format files describing the ancestral gene orders.

```
(AGO-pipeline) > python scripts/gene_orders_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/results/DeCoSTAR/genes_reformatted.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/adjacencies_ago_X.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/results/SPPDCJ/ /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/gene_orders_ago_X.txt
```

One can look at the gene order files (whose paths are given in
`./anopheles_X_GeneRax/data/gene_orders_ago_X.txt`)
to analyze the resulting gene orders.  

## ALE-based pipeline

In this second experiment, we do not use `GeneRax` to compute
reconciled gene trees.  We reuse the alignments obtained with `MACSE`
in the previous experiment, then run `IQ-TREE` in fast bootstrap mode
to obtain a sample of 1,000 gene trees for each gene family, and
compute reconciled gene trees from these sampled gene trees using
`ALE`. We use the evolution model of `ALE` that allows lateral gene
transfers, to account for an implementation issue in `ALEml_undated`
when the parameter `tau=0` is set (see [Manual](../doc/manual.md));
however, we filter out all gene families for which the reconciled gene
tree includes a lateral gene transfer.

Similarly to the previous experiment, we first edit a parameters file
header ([ALE pipeline header](anopheles_X_ALE_header.yaml), writing
the parameters for the tools `IQ-TREE` (available as a module in our
HPC system), `ALE` (installed locally), `DeCoSTAR` and `spp_dcj`
(similar to the previous experiment) and writing an explicit path to
access the `MACSE` MSAs generated in the previous experiment in order
to not recompute them.

We first check that the data is correctly formatted and consistent:
```
(AGO-pipeline) > python scripts/data_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/alignments_X.txt NA
SUCCESS SPECIES TREE
SUCCESS FAMILIES
SUCCESS GENE ORDERS
SUCCESS ALIGNMENTS
```

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml create example/anopheles_X_ALE_header.yaml parameters IQ-TREE ALE DeCoSTAR SPPDCJ
        example/anopheles_X_ALE.yaml
```
Next we initialize he pipeline, and we can observe that indeed the MSA files will not be recomputed.
```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/sequences_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_GeneRax/data/alignments_X.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/alignments_X.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_trees_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/reconciliations_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/adjacencies_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/adjacencies_ago_X.txt will be computed.
```
Next we run `IQ-TREE` through `slurm`.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml slurm IQ-TREE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml check IQ-TREE
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/IQ-TREE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_trees_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml slurm ALE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/ALE/ALE.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/ALE/ALE.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml check ALE
        ERRORS: 66
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/ALE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/reconciliations_X.txt
```

There are 66 families involving lateral gene transfers. They will be
discarded from further steps without the need to do anything, as this
is handled automatically by the AGO pipeline.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml stats ALE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/ALE/ALE_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/ALE/ALE_families.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/ALE/ALE_species.csv
#species:genes:duplications:losses:transfers
node2:385:0:0:0
AnophelesgambiaePEST:391:6:0:0
AnophelesfunestusFUMOZ:387:2:0:0
node0:385:0:0:0
AnophelesatroparvusEBRO:387:2:0:0
node1:385:0:0:0
AnophelesalbimanusSTECLA:389:4:0:0
```

We can observe that very few gene duplication/loss events are left in
the non-discarded gene families, showing that on this dataset, `ALE`
explained most of the discrepancy between the gene trees and the
species tree using at least one lateral gene transfer. The lower
number of gene families results from discarding the 66 ones whose
reconciled gene tree included a lateral gene transfer.

Next we run `DeCoSTAR` through `slurm`.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml slurm DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/DeCoSTAR.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/adjacencies_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml stats DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv
(AGO-pipeline) > head -1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv; grep -P ':0.5\t' /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:389:0.5        389:388:0:2
AnophelesatroparvusEBRO:387:0.5 387:386:0:2
AnophelesfunestusFUMOZ:387:0.5  387:386:0:2
AnophelesgambiaePEST:391:0.5    391:390:0:2
node0:385:0.5   364:335:0:100
node1:385:0.5   337:264:0:242
node2:385:0.5   233:157:0:456
```

As in the previous experiment, we can observe a low level of conflict
and a high number of free gene extremities, which will result in
highly fragmented ancestral gene orders.

Last, we clean conflicts in the `DeCoSTAR` ancestral gene adjacencies
using `spp_dcj` as in the previous experiment, and create FASTA-like
ancestral gene orders files.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ_ILP
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/SPPDCJ.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/adjacencies_ago_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ALE.yaml stats SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/SPPDCJ/SPPDCJ_species.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   157:156.51:157:156.51
node1   264:263.51:264:263.51
AnophelesalbimanusSTECLA        388:388.0:388:388.0
node0   335:334.51:335:334.51
AnophelesatroparvusEBRO 386:386.0:386:386.0
AnophelesgambiaePEST    390:390.0:390:390.0
AnophelesfunestusFUMOZ  386:386.0:386:386.0
```
```
(AGO-pipeline) > python scripts/gene_orders_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/results/DeCoSTAR/genes_reformatted.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/adjacencies_ago_X.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/results/SPPDCJ/ /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_orders_ago_X.txt
```

## ecceTERA-based pipeline

In this last experiment, we reuse the gene trees obtained with
`IQ-TREE` in the previous experiment, but the reconciled gene trees
are computed using the parsimony tool `ecceTERA`, implemented in
`DeCoSTAR`. Note that in the header file, we deleted the sections
about sequences and MSAs data, as they will not be eeded by any tool.


We first check that the data is correctly formatted and consistent:
```
(AGO-pipeline) > python scripts/data_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt NA NA /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_trees_X.txt 
SUCCESS SPECIES TREE
SUCCESS FAMILIES
SUCCESS GENE ORDERS
SUCCESS GENE TREES
```

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml create example/anopheles_X_ecceTERA_header.yaml parameters DeCoSTAR SPPDCJ
        example/anopheles_X_ecceTERA.yaml
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml init
         /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_trees_X.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/gene_trees_X.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/adjacencies_X.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt will be computed.
```

Next, we run `DeCoSTAR` to compute reconciled gene trees and ancestral adjacencies. 

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/log/DeCoSTAR.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/adjacencies_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
(AGO-pipeline) > head -1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv; grep -P ':0.5\t' /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:473:0.5   453:422:6:108
node1:500:0.5   447:359:6:288
node2:483:0.5   331:224:0:518
```

As in previous experiments, there is a low level of conflict and a high number of free gene extremities.

We clean conflicts using `spp_dcj` and generate gene orders files.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ_ILP
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/log/SPPDCJ.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   227:224.4:224:223.08
node1   370:357.7:353:348.87
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   424:420.38:417:415.68
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
```
```
(AGO-pipeline) > python scripts/gene_orders_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/results/DeCoSTAR/genes_reformatted.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/results/SPPDCJ/ /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ecceTERA/data/gene_orders_ago_X.txt
```

