# Reconstructing Anopheles ancestral X chromosome gene orders

## Overview

This directory contains parameters files for the AGO pipeline aimed at
reconstructing the ancestral gene orders of the X chromosomes for
three ancestral *Anopheles* mosquito species.

The ancestral gene orders are reconstructed according to three different versions of the pipeline, in order to illustrate the modularity of the pipeline:
- all three approaches start from the same data, described in the section Data below;
- all three approaches rely on Multiple Sequences Alignments (MSA) for the gene families obtained with the tool `MACSE`;
- the first approach computes reconciled gene trees from the MSAs using the tool `GeneRax`;
- the second approach computes gene trees samples using the tool `IQ-TREE` and reconciled gene trees from these gene trees using the tool `ALE`;
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
- a [species tree](../data/VectorBase/species_tree_4.newick) with branch lengths;
- 554 [gene families](../data/VectorBase/families_X_3.txt) containing 2,265 genes;
- DNA [sequences](../data/VectorBase/sequences_X_3.txt) for all genes, grouped by families.

Note that the sequences file is provided with absolute path with
prefix (`/home/chauvec/projects/ctb-chauvec/`) corresponding to the
experiments that were ran on the `cedar` HPC cluster of the <a
href="https://alliancecan.ca/en">Digital Research Alliance of
Canada</a>; to be reproduced, this prefix will need to be changed.

Similarly, the path to access the external tools used in the
pipelines (`MACSE`, `GeneRax`, `IQ-TREE`, `ALE`, `DeCoSTAR`,
`spp_dcj`) are provided in the parameters files under the assumption
that all such tools are either available as a module on the
corresponding HPC system or have been installed in the directory
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/bin`): this would
need to be updated to be reproduced on another system.

Finally, all computations we ran within a python 3 virtual environment
`AGO-pipeline` including all the required packages (see
[README.md](../README.md)).

## GeneRax-based pipeline

We first create a parameters file for a pipeline that uses, in
sequence, `MACSE` to compute MSAs based on nucleotide sequences,
`GeneRax` to compute reconciled gene trees from these alignments,
`DeCoSTAR` to compute ancestral adjacencies, and `spp_dcj` to compute a
set of conflict-free adjacencies defining ancestral gene orders.

To do so, we first create and edit a copy of [header
template](../parameters/header_template.yaml) into the parameters
header file [GeneRax pipeline
header](anopheles_X_3_GeneRax_header.yaml).


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
(AGO-pipeline) > python scripts/data_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_3.txt 'sequences'
SUCCESS SPECIES TREE
SUCCESS FAMILIES
SUCCESS GENE ORDERS
SUCCESS SEQUENCES
```

Then we create the pipeline parameters file:

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml create example/anopheles_X_3_GeneRax_header.yaml parameters MACSE GeneRax DeCoSTAR SPPDCJ
        example/anopheles_X_3_GeneRax.yaml
```

The next step was to initialize the pipeline.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/families_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/gene_orders_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/sequences_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/alignments_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/reconciliations_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/adjacencies_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/adjacencies_ago_X_3.txt will be computed.
```

Then we run in sequence the pipeline tools. First we run `MACSE` to
compute an MSA for each family.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml slurm MACSE
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/MACSE/MACSE.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml check MACSE
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/MACSE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/alignments_X_3.txt
```

This shows that `MACSE` succeeded to compute an MSA for all gene
families. The next step is `GeneRax` to compute reconciled gene trees.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml slurm GeneRax
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/GeneRax/GeneRax.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/GeneRax/GeneRax.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml check GeneRax
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/GeneRax.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/reconciliations_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml stats GeneRax
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/GeneRax/GeneRax_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/GeneRax/GeneRax_families.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses:transfers
node2:549:45:0:0
AnophelesgambiaePEST:564:7:47:0
AnophelesfunestusFUMOZ:579:7:32:0
node0:604:3:39:0
AnophelesatroparvusEBRO:577:18:81:0
node1:640:42:1:0
AnophelesalbimanusSTECLA:545:8:12:0
```

Again, all expected output files are present and there is no error
in running `GeneRax`.
  
We can observe from the statistics that the number of ancestral genes
is slightly higher than the number of extant genes and one can suspect
the well-documented issue of the reconciliation algorithm having a
tendancy to locate duplications higher in the species tree.
  
Next, to illustrate the feature that the AGO pipeline tools can be ran
either through `slurm` or a `bash` script, we run `DeCoSTAR` as a bash script,
redirecting the standard output and error output into specific files.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml bash DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > chmod 755 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh 2> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/DeCoSTAR/DeCoSTAR.err 1> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/DeCoSTAR/DeCoSTAR.log
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/DeCoSTAR.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/adjacencies_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml stats DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/DeCoSTAR/DeCoSTAR_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/DeCoSTAR/DeCoSTAR_components.csv
(AGO-pipeline) > head -1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/DeCoSTAR/DeCoSTAR_species.csv; grep -P ':0.5\t' /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/DeCoSTAR/DeCoSTAR_species.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:545:0.5        545:544:0:2
AnophelesatroparvusEBRO:577:0.5 577:576:0:2
AnophelesfunestusFUMOZ:579:0.5  579:578:0:2
AnophelesgambiaePEST:564:0.5    564:563:0:2
node0:604:0.5   584:551:36:142
node1:640:0.5   551:440:15:415
node2:549:0.5   366:247:3:607
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/DeCoSTAR/DeCoSTAR_components.csv
#species        nb_comp:nb_lin_comp:nb_circ_comp:list(nb_genes.nb_adj.nb_comp)
node2   295:294:1:11.10.2,9.8.1,8.7.1,7.6.3,6.6.1,6.5.5,5.4.3,4.3.14,3.2.29,2.1.59,1.0.177
node1   172:158:12:32.35.1,19.18.1,18.17.1,15.15.1,15.14.2,12.12.1,10.10.4,10.9.2,9.10.1,9.9.3,9.8.4,8.7.4,7.6.4,6.6.2,6.5.7,5.4.11,4.4.1,4.3.12,3.2.12,2.1.27,1.0.71
AnophelesalbimanusSTECLA        1:1:0:545.544.1
node0   55:46:5:98.102.1,69.70.1,55.60.1,42.41.1,34.35.1,29.28.1,22.21.1,20.20.1,18.17.1,16.15.2,14.13.1,12.11.1,11.11.2,11.10.2,10.10.1,10.9.1,9.9.1,9.8.1,8.7.1,7.6.1,6.5.1,5.4.3,4.3.1,3.2.2,2.1.6,1.0.19
AnophelesatroparvusEBRO 1:1:0:577.576.1
AnophelesgambiaePEST    1:1:0:564.563.1
AnophelesfunestusFUMOZ  1:1:0:579.578.1
```

We can observe that `DeCoSTAR` runs with no error. But the statistics
on the resulting ancestral adjacencies show that we can expect highly
fragmented ancestral gene orders, as there is a significant level of
free gene extremities in the ancestral gene adjacencies. The level of
conflict in the ancestral gene adjacencies is however very low.
Looking at the statistics in terms of connected components of the
graphs defined by candidate ancestral adjacencies we can observe that
for ancestral `node1` and `node2`, the adjacencies almost define
gene orders composed of linear fragments (CARs), while there is
limited syntenic conflict in `node0` (5 circular components and 4
components being neither linear nor circular).

Finally, we clear sytenic conflicts in ancestral adjacencies using
`spp_dcj`. This requires to first compute the Mixed Integer Linear
Program (MILP) and then to solve it using `gurobi`.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml slurm SPPDCJ_ILP
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
```
We solve the MILP.
```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml slurm SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/SPPDCJ/SPPDCJ.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/SPPDCJ.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/adjacencies_ago_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_GeneRax.yaml stats SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/SPPDCJ/SPPDCJ_components.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/CARs.txt
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   255:247.3:244:242.87
node1   486:447.24:426:419.16
AnophelesalbimanusSTECLA        544:544.0:544:544.0
node0   569:538.75:518:507.5
AnophelesatroparvusEBRO 576:576.0:576:576.0
AnophelesgambiaePEST    563:563.0:563:563.0
AnophelesfunestusFUMOZ  578:578.0:578:578.0
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/SPPDCJ/SPPDCJ_CARs.csv
#species        nb_comp:nb_lin_comp:nb_circ_comp:list(nb_genes.nb_adj.nb_comp)
node2   305:305:0:10.9.2,9.8.1,8.7.1,7.6.2,6.5.4,5.4.4,4.3.16,3.2.26,2.1.63,1.0.186
node1   214:214:0:23.22.1,18.17.1,15.14.1,11.10.1,10.9.1,9.8.4,8.7.9,7.6.6,6.5.8,5.4.15,4.3.17,3.2.19,2.1.34,1.0.97
AnophelesalbimanusSTECLA        1:1:0:545.544.1
node0   86:86:0:69.68.1,46.45.1,42.41.1,35.34.1,26.25.2,24.23.1,22.21.1,16.15.2,15.14.2,14.13.1,12.11.1,11.10.3,10.9.2,9.8.4,8.7.1,7.6.4,6.5.1,5.4.3,4.3.1,3.2.5,2.1.13,1.0.35
AnophelesatroparvusEBRO 1:1:0:577.576.1
AnophelesgambiaePEST    1:1:0:564.563.1
AnophelesfunestusFUMOZ  1:1:0:579.578.1
```

The `spp_dcj` statistics show that, as expected, very few adjacencies
needed to be discarded to clear all conflicts in ancestral
species `node2`, unlike in `node0` and `node1`, but in both cases the
weight of the discarded adjacencies is quite low.

FASTA-like files describing the extant gene orders and CARs have been created and
are listed in the file
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/CARs.txt`.
Statistics on the CARs described in
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/statistics/SPPDCJ/SPPDCJ_CARs.csv`
show that the largest CAR for ancestral species `node0`,`node1` and `node2` are of respective size
(number of genes) 69, 23 and 10,
while the respective numbers of CARs of size 1 are 35, 97 and 186,
illustrating the fragmentation of the reconstructed ancestral gene orders.

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
header ([ALE pipeline header](anopheles_X_3_ALE_header.yaml)), writing
the parameters for the tools `IQ-TREE` (available as a module in our
HPC system), `ALE` (installed locally), `DeCoSTAR` and `spp_dcj`
(similar to the previous experiment) and writing an explicit path to
access the `MACSE` MSAs generated in the previous experiment in order
to not recompute them.

We first check that the data is correctly formatted and consistent:
```
(AGO-pipeline) > python scripts/data_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/alignments_X_3.txt 'alignments'
SUCCESS SPECIES TREE
SUCCESS FAMILIES
SUCCESS GENE ORDERS
SUCCESS ALIGNMENTS
```

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml create example/anopheles_X_3_ALE_header.yaml parameters IQ-TREE ALE DeCoSTAR SPPDCJ
        example/anopheles_X_3_ALE.yaml
```
Next we initialize he pipeline, and we can observe that indeed the MSA files will not be recomputed.
```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/families_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/gene_orders_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/sequences_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/alignments_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/alignments_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/gene_trees_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/reconciliations_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/adjacencies_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/adjacencies_ago_X_3.txt will be computed.
```
Next we run `IQ-TREE` through `slurm`.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml slurm IQ-TREE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/aux/IQ-TREE/IQ-TREE.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/aux/IQ-TREE/IQ-TREE.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml check IQ-TREE
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/log/IQ-TREE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/gene_trees_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml slurm ALE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/aux/ALE/ALE.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/aux/ALE/ALE.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml check ALE
        ERRORS: 120
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/log/ALE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/reconciliations_X_3.txt
```

There are 120 families involving lateral gene transfers. They will be
discarded from further steps without the need to do anything, as this
is handled automatically by the AGO pipeline.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml stats ALE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/ALE/ALE_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/ALE/ALE_families.csv
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/ALE/ALE_species.csv
#species:genes:duplications:losses:transfers
node2:389:0:0:0
AnophelesgambiaePEST:440:7:1:0
AnophelesfunestusFUMOZ:438:5:1:0
node0:433:0:0:0
AnophelesatroparvusEBRO:435:2:0:0
node1:434:0:0:0
AnophelesalbimanusSTECLA:393:4:0:0
```

We can observe that very few gene duplication/loss events are left in
the non-discarded gene families, showing that on this dataset, `ALE`
explained most of the discrepancy between the gene trees and the
species tree using at least one lateral gene transfer. The lower
number of gene families results from discarding the 66 ones whose
reconciled gene tree included a lateral gene transfer.

Next we run `DeCoSTAR` through `slurm`.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml slurm DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/aux/DeCoSTAR/DeCoSTAR.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/log/DeCoSTAR.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/adjacencies_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ALE.yaml stats DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/DeCoSTAR/DeCoSTAR_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/DeCoSTAR/DeCoSTAR_components.csv
(AGO-pipeline) > head -1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/DeCoSTAR/DeCoSTAR_species.csv; grep -P ':0.5\t' /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/DeCoSTAR/DeCoSTAR_species.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:393:0.5        393:392:0:2
AnophelesatroparvusEBRO:435:0.5 435:434:0:2
AnophelesfunestusFUMOZ:438:0.5  438:437:0:2
AnophelesgambiaePEST:440:0.5    440:439:0:2
node0:433:0.5   417:386:0:94
node1:434:0.5   384:303:0:262
node2:389:0.5   227:152:0:474
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/statistics/DeCoSTAR/DeCoSTAR_components.csv
#species        nb_comp:nb_lin_comp:nb_circ_comp:list(nb_genes.nb_adj.nb_comp)
node2   237:237:0:8.7.1,7.6.2,6.5.5,5.4.5,4.3.3,3.2.20,2.1.39,1.0.162
node1   131:131:0:17.16.3,15.14.1,14.13.1,12.11.1,10.9.1,9.8.1,8.7.1,7.6.7,6.5.7,5.4.7,4.3.10,3.2.17,2.1.24,1.0.50
AnophelesalbimanusSTECLA        1:1:0:393.392.1
node0   47:47:0:50.49.1,34.33.1,31.30.1,28.27.1,27.26.1,24.23.2,20.19.3,15.14.2,14.13.1,12.11.2,9.8.1,7.6.3,6.5.3,5.4.1,3.2.2,2.1.6,1.0.16
AnophelesatroparvusEBRO 1:1:0:435.434.1
AnophelesgambiaePEST    1:1:0:440.439.1
AnophelesfunestusFUMOZ  1:1:0:438.437.1
```

We can observe an absence of syntenic conflict and a
high number of free gene extremities, which will result in
highly fragmented ancestral gene orders.

It is unnecessary to run spp_dcj as the DeCoSTAR adjacencies
have no syntenic conflict and every component is a CAR.
The ancestral gene orders are quite fragmented with `node0`, `node`,
and `node2` having respectively 47, 131 and 237 CARs and the largest
CAR in each being of respective size 50, 17 and 8.
CARs in FASTA-like format can be generated from DeCoSTAR adjacencies.
```
(AGO-pipeline) > python scripts/gene_orders_utils.py build /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/adjacencies_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTARctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/CARs.txt
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/CARs.txt
node2   /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/node2_CARs.txt
node1   /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/node1_CARs.txt
AnophelesalbimanusSTECLA        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/AnophelesalbimanusSTECLA_CARs.txt
node0   /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/node0_CARs.txt
AnophelesatroparvusEBRO /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/AnophelesatroparvusEBRO_CARs.txt
AnophelesgambiaePEST    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/AnophelesgambiaePEST_CARs.txt
AnophelesfunestusFUMOZ  /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/results/DeCoSTAR/AnophelesfunestusFUMOZ_CARs.txt
```

## ecceTERA-based pipeline

In this last experiment, we reuse the gene trees obtained with
`IQ-TREE` in the previous experiment, but the reconciled gene trees
are computed using the parsimony tool `ecceTERA`, implemented in
`DeCoSTAR`. Note that in the header file, we deleted the sections
about sequences and MSAs data, as they will not be needed by any tool.

We first check that the data is correctly formatted and consistent:
```
(AGO-pipeline) > python scripts/data_utils.py /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_3.txt /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/gene_trees_X_3.txt 'gene_trees'
SUCCESS SPECIES TREE
SUCCESS FAMILIES
SUCCESS GENE ORDERS
SUCCESS GENE TREES
```

Next we create the pipeline parameters file and initialize the pipeline.
```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml create example/anopheles_X_3_ecceTERA_header.yaml parameters DeCoSTAR SPPDCJ
        example/anopheles_X_3_ecceTERA.yaml
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/families_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/gene_orders_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ALE/data/gene_trees_X_3.txt -> /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/gene_trees_X_3.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/adjacencies_X_3.txt will be computed.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/adjacencies_ago_X_3.txt will be computed.
```

Next, we run `DeCoSTAR` to compute reconciled gene trees and ancestral adjacencies. 
```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml slurm DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/log/DeCoSTAR.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/adjacencies_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml stats DeCoSTAR
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_components.csv
(AGO-pipeline) > head -1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_species.csv; grep -P ':0.5\t' /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_species.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:545:0.5        545:544:0:2
AnophelesatroparvusEBRO:577:0.5 577:576:0:2
AnophelesfunestusFUMOZ:579:0.5  579:578:0:2
AnophelesgambiaePEST:564:0.5    564:563:0:2
node0:580:0.5   559:524:7:119
node1:607:0.5   534:430:8:362
node2:538:0.5   362:245:0:586
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_components.csv
#species        nb_comp:nb_lin_comp:nb_circ_comp:list(nb_genes.nb_adj.nb_comp)
node2   292:292:0:11.10.1,10.9.1,9.8.1,8.7.1,7.6.3,6.5.5,5.4.4,4.3.14,3.2.24,2.1.63,1.0.175
node1   172:164:7:29.31.1,19.18.1,18.17.1,15.14.1,14.13.1,10.10.3,10.9.1,9.9.2,9.8.4,8.7.8,7.6.5,6.6.2,6.5.6,5.4.8,4.3.13,3.2.18,2.1.28,1.0.69
AnophelesalbimanusSTECLA        1:1:0:545.544.1
node0   55:51:3:68.67.1,60.59.1,47.46.1,42.41.1,35.35.1,31.31.1,26.25.1,22.21.1,21.22.1,17.16.1,16.15.1,15.14.1,14.13.1,12.11.1,11.11.1,11.10.2,10.9.1,9.8.3,8.7.2,7.6.1,6.5.1,5.4.3,4.3.1,3.2.2,2.1.6,1.0.18
AnophelesatroparvusEBRO 1:1:0:577.576.1
AnophelesgambiaePEST    1:1:0:564.563.1
AnophelesfunestusFUMOZ  1:1:0:579.578.1
```

As in previous experiments, there is a low level of conflict and a
high number of free gene extremities and adjacencies component
indicating the CARs will be highly fragmented.

We clean conflicts using `spp_dcj` and generate CARs files.

```
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml slurm SPPDCJ_ILP
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml slurm SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
(AGO-pipeline) > sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
	  	    ... wait for the slurm processes to complete ...
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/log/SPPDCJ.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_GeneRax/data/adjacencies_ago_X_3.txt
(AGO-pipeline) > python src/AGO.py example/anopheles_X_3_ecceTERA.yaml stats SPPDCJ
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/SPPDCJ/SPPDCJ_CARs.csv
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/data/CARs.txt
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   246:244.32:245:244.01
node1   446:428.68:422:417.51
AnophelesalbimanusSTECLA        544:544.0:544:544.0
node0   530:521.07:518:514.8
AnophelesatroparvusEBRO 576:576.0:576:576.0
AnophelesgambiaePEST    563:563.0:563:563.0
AnophelesfunestusFUMOZ  578:578.0:578:578.0
(AGO-pipeline) > cat /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_3_ecceTERA/statistics/SPPDCJ/SPPDCJ_CARs.csv
#species        nb_comp:nb_lin_comp:nb_circ_comp:list(nb_genes.nb_adj.nb_comp)
node2   293:293:0:10.9.2,9.8.1,8.7.1,7.6.3,6.5.5,5.4.4,4.3.14,3.2.24,2.1.63,1.0.176
node1   185:185:0:21.20.1,18.17.1,15.14.1,14.13.1,11.10.1,10.9.1,9.8.5,8.7.11,7.6.5,6.5.9,5.4.9,4.3.14,3.2.19,2.1.31,1.0.76
AnophelesalbimanusSTECLA        1:1:0:545.544.1
node0   62:62:0:68.67.1,57.56.1,47.46.1,42.41.1,35.34.1,31.30.1,26.25.1,22.21.1,17.16.1,16.15.1,15.14.1,14.13.1,12.11.1,11.10.3,10.9.2,9.8.3,8.7.1,7.6.2,6.5.2,5.4.2,4.3.2,3.2.3,2.1.8,1.0.21
AnophelesatroparvusEBRO 1:1:0:577.576.1
AnophelesgambiaePEST    1:1:0:564.563.1
AnophelesfunestusFUMOZ  1:1:0:579.578.1
```

As expected very few adjacencies needed to be discarded to clean syntenic conflicts and
the ancestral gene orders are quite fragmented.
