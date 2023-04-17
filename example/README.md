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

The provided parameters files include the parameters needed to run the AGO pipeline on the `cedar` HPC cluster of the
<a href="https://alliancecan.ca/en">Digital Research Alliance of Canada</a>.

## Data

The data needed to run the experiments are located in [data/VectorBase](../data/VectorBase/README.md).

This dataset focuses on reconstructing the ancestral gene orders of the X chromosomes for
three ancestral *Anopheles* mosquito species, dfined as the ancestors of the following extant *Anopheles* species:
*Anopheles gambiae PEST, Anopheles atroparvus EBRO, Anopheles funestus FUMOZ, Anopheles albimanus STECLA*.

The data were obtained from the data repository <a
href="https://vectorbase.org/">VectorBase</a>, as described in
[data/VectorBase](../data/VectorBase/README.md).

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

## GeneRax-based pipeline

We first create a parameters file for a pipeline that uses, in
sequence, MACSE to compute alignments based on nucleotide sequences,
GeneRax to compute reconciled gene tres from these alignments,
DeCoSTAR to compute ancestral adjacencies, and spp_dcj to compute a
set of conflict-free adjacencies defining ancestral gen orders.

To create this pipeline, we first created the pipeline-specific YAML file
[Anopheles example parameters file header, GeneRax pipeline](example/anopheles_X_GeneRax_header.yaml)
from
[header template](parameters/header_template.yaml).

*TODO: explain pipeline choices*

Then we created the pipeline parameters file:

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml create example/anopheles_X_GeneRax_header.yaml parameters MACSE GeneRax DeCoSTAR SPPDCJ
        example/anopheles_X_GeneRax.yaml
```

The next step was to initialize the pipeline.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt will be computed.
```

Then we run in sequence the pipeline tools. First we run MACSE to
compute a multiple sequence alignment for each family.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm MACSE
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check MACSE
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/MACSE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt
```

This shows that MACSE succeeded to compute an MSA for all gene
families. The next step is GeneRax.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check GeneRax
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/GeneRax.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_families.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
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
in running GeneRax.
  
We can observe that the number of ancestral genes is slightly higher
than the number of extant genes and oe can suspect the well-documented
issue of the reconciliation algorithm having a tendancy to locate
duplications higher in the species tree.
  
Next to illustrate the feature that the AGO pipeline tools can be ran
either through slurm or locally, we ran DeCoSTAR as a bash script,
redirecting the standard output and error output into specific files.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml bash DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
AGO-pipeline > chmod 755 /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
AGO-pipeline > /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh 2> /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.err 1> /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.log
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv; grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:495:0.5   474:448:33:127
node1:529:0.5   462:368:11:333
node2:492:0.5   331:224:0:536
```

We can observe that DeCoSTAR ran with no problem. But the statistics on
the resulting ancestral adjacencies show that we can expect highly
fragmented ancestral gene orders, as there is a significant level of
conflicting adjacencies and free extremities in the ancestral species.
  
Finally, we clear the conflict in ancestral adjacencies using spp_dcj.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/SPPDCJ.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   231:225.74:224:223.24
node1   404:372.4:357:351.14
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   460:436.96:416:409.12
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
AGO-pipeline > python scripts/gene_orders_utils.py /scratch/chauvec/SPP/anopheles_X_GeneRax/results/DeCoSTAR/genes_reformatted.txt /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt /scratch/chauvec/SPP/anopheles_X_GeneRax/results/SPPDCJ/ /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_ago_X.txt
```

One can look at the gene order files (whose paths are given in
`/scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_ago_X.txt`)
to analyze the resulting gene orders.  The spp_dcj statistics show
that actually very few adjacencies need to be discarded to clear all
conflicts in ancestral species`node2`, unlike in `node0` and `node1`,
but in both cases the weight of the discarded adjacencies is quite
low.

## ALE-based pipeline

We reuse the alignments obtained with MACSE for the previous experiment.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml create example/anopheles_X_ALE_header.yaml parameters IQ-TREE ALE DeCoSTAR SPPDCJ
        example/anopheles_X_ALE.yaml
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/alignments_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_trees_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt will be computed.
```

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm IQ-TREE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check IQ-TREE
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/IQ-TREE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check ALE
        ERRORS: 66
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/ALE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/reconciliations_X.txt
```

There are 66 families involving transfers. They will be discarded from further steps.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_species.csv
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_families.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_species.csv
#species:genes:duplications:losses:transfers
node2:385:0:0:0
AnophelesgambiaePEST:391:6:0:0
AnophelesfunestusFUMOZ:387:2:0:0
node0:385:0:0:0
AnophelesatroparvusEBRO:387:2:0:0
node1:385:0:0:0
AnophelesalbimanusSTECLA:389:4:0:0
```

Very few gene duplication/loss events are left in the non-discarded gene families.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv
AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv; grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:389:0.5        389:388:0:2
AnophelesatroparvusEBRO:387:0.5 387:386:0:2
AnophelesfunestusFUMOZ:387:0.5  387:386:0:2
AnophelesgambiaePEST:391:0.5    391:390:0:2
node0:385:0.5   364:335:0:100
node1:385:0.5   337:264:0:242
node2:385:0.5   233:157:0:456
```

Comment on level of conflict.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/SPPDCJ.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/SPPDCJ/SPPDCJ_species.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ALE/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   157:156.51:157:156.51
node1   264:263.51:264:263.51
AnophelesalbimanusSTECLA        388:388.0:388:388.0
node0   335:334.51:335:334.51
AnophelesatroparvusEBRO 386:386.0:386:386.0
AnophelesgambiaePEST    390:390.0:390:390.0
AnophelesfunestusFUMOZ  386:386.0:386:386.0
AGO-pipeline > python scripts/gene_orders_utils.py /scratch/chauvec/SPP/anopheles_X_ALE/results/DeCoSTAR/genes_reformatted.txt /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt /scratch/chauvec/SPP/anopheles_X_ALE/results/SPPDCJ/ /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_orders_ago_X.txt
```

Comment on final ancestral gene orders.

## ecceTERA-based pipeline

We reuse the gene trees obtained with IQ-TREE for the previous experiment.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml create example/anopheles_X_ecceTERA_header.yaml parameters DeCoSTAR SPPDCJ
        example/anopheles_X_ecceTERA.yaml
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/alignments_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_trees_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt will be computed.
```

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv; grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:473:0.5   453:422:6:108
node1:500:0.5   447:359:6:288
node2:483:0.5   331:224:0:518
```

Comment on level of conflict.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/SPPDCJ.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   227:224.4:224:223.08
node1   370:357.7:353:348.87
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   424:420.38:417:415.68
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
AGO-pipeline > python scripts/gene_orders_utils.py /scratch/chauvec/SPP/anopheles_X_ecceTERA/results/DeCoSTAR/genes_reformatted.txt /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt /scratch/chauvec/SPP/anopheles_X_ecceTERA/results/SPPDCJ/ /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_ago_X.txt
```

Comment on final ancestral gene orders.