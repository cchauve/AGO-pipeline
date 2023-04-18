# AGO Manual

## Overview

AGO is a suite of python scripts, aimed at implementing phylogenomics
pipelines for reconstructing ancestral gene orders in a phylogenetic
context, from extant gene orders, gene families and gene sequence
data.

AGO pipelines are is based on the general methodology described in <a
href="https://doi.org/10.1007/978-1-4471-5298-9_4">Duplication,
Rearrangement and Reconciliation: A Follow-Up 13 Years Later</a>
(see also the review <a
href="https://doi.org/10.1007/978-1-4939-7463-4_13">Comparative
Methods for Reconstructing Ancient Genome Organization</a>).  It
consists in the following steps:
- computing a multiple sequences alignment (MSA) for each homologous gene family;
- computing a gene tree, or sample of gene trees, from the MSA for each gene family;
- computing a reconciled gene tree, from the MSA and/or gene tree(s), for each gene family;
- computing ancestral gene adjacency candidates from the species tree, the extant gene orders and the reconciled gene trees;
- clearing conflicts from the set of candidate ancestral gene adjacency (variant of the Small Parsimony Problem for gene orders).

This approach allows to account for the full complement of genes in
extant genomes, at the expense of necessitating several steps,
implemented in various tools, that are not trivial to interface
together into a pipeline. AGO is aimed at easing the creation of such
pipelines; AGO in itself dos not introduce any novel algorithm, and
aims solely at allowing to create pipelines based on published
existing tools.

The documentation below assumes knowledge of the phylogenomics approach described in <a
href="https://doi.org/10.1007/978-1-4471-5298-9_4">Duplication,
Rearrangement and Reconciliation: A Follow-Up 13 Years Later</a>.

## Installation

AGO has been developed using <a
href="https://www.python.org/downloads/release/python-3810/">python
version 3.8.10</a>. We recommend to run AGO within a python virtual
environment (https://docs.python.org/3.8/library/venv.html) including
the following python packages, that are required:
- <a href="https://pypi.org/project/ete3/3.1.2/">ete3, version 3.1.2</a>
- <a href="https://matplotlib.org/3.7.1/">matplotlib, version 3.7.0</a>.
- <a href="https://pypi.org/project/networkx/3.1/">networkx, version 3.1</a>.
- <a href="https://numpy.org/">numpy, version 1.24.2</a>.
- <a href="https://pandas.pydata.org/pandas-docs/version/1.5.3/">pandas, version 1.5.3</a>.
- <a href="https://pypi.org/project/PyYAML/6.0/">PyYAML, version 6.0</a>.

AGO allows to include the following external tools in an ancestral
gene orders reconstruction pipeline:
- Multiple sequence alignments: <a href="https://bioweb.supagro.inra.fr/macse/">MACSE, version 2.06</a>; requires <a href="https://openjdk.org/">Java, OpenJDK version 17
.0.2</a>.
- Gene trees: <a href="http://www.iqtree.org/">IQ-TREE, version 2.0.7</a>.
- Reconciled gene trees: <a href="https://github.com/ssolo/ALE">ALE, version 1.0</a>.
- Reconciled gene trees: <a href="https://github.com/BenoitMorel/GeneRax">GeneRax, version 2.1.0</a>.
- Ancestral adjacencies: <a href="https://github.com/WandrilleD/DeCoSTAR">DeCoSTAR, version 1.2</a>.
- Ancestral gene orders: <a href="https://github.com/danydoerr/spp_dcj">SPP_DCJ</a>; requires <a href="https://www.gurobi.com/">gurobi, version 10.0.1</a>.

These tools require to be installed independently from AGO; we refer
to the specific documentation of each tool for the installation
instructions; a future release of AGO will include these tools in a
<a href="https://sylabs.io/singularity/">Singularity</a> container.

Finally AGO can run the external tools integrated into a pipeline
either on local workstations (through shell scripts) or on
High-Performance Computing (HPC) clusters using the <a
href="https://slurm.schedmd.com/documentation.html">slurm</a>
scheduler.

## AGO architecture

An AGO pipeline is defined by the following elements:
- a set of input data files that include, at minima, a species tree, a set of gene families and gene orders for extant species, together with possibly additional data depending on the sp[ecific implemented pipeline;
- a set of external computational tools, each with specific options, aimed to be run in a specific order, aimed at processing the input data to generate a set of gene orders for the ancestral species defined by the input species tree.

An AGO pipeline is described by a YAML parameters file that is composed of two parts:
- the first part, customized by the user, describes the input data, the tools to use in the pipeline and the options to run each tool;
- the second part, that is fixed and should not be modified by the user, describes how to implement each step of the pipeline.

The external tools that can be integrated into an AGO pipeline can be
interfaced to create three different pipelines, each broadly defined
by the method used to computed reconciled gene trees.

All three pipelines assumes that the input data contains a species
tree, a set of gene families, gene orders for extant species and the
DNA sequences for the genes in each family.

### Pipeline 1, based on GeneRax

In the first pipeline, the following steps are implemented:
- for each gene family, an MSA is computed using MACSE;
- for each gene family, a reconciled gene tree is computed from its MSA using GeneRax;
- for each ancestral species, a set of candidate ancestral gene adjacencies is computed (consistent with the reconciled gene trees), that might not be compatible with a linear ancestral gene order;
- for each ancestral species, a subset of the candidate ancestral adjacencies is computed, using spp_dcj, that is compatible with a linear gene order.

This pipeline does not compute explicitly gene trees for the gene families, that are explicitly defined by the reconciled gene trees.

### Pipeline 2, based on ALE

In the second pipeline, the following steps are implemented:
- for each gene family, an MSA is computed using MACSE;
- for each gene family, a sample of gene trees is computed from its MSA using IQ-TREE;
- for each gene family, a reconciled gene tree is computed from the sampled gene trees using ALE;
- for each ancestral species, a set of candidate ancestral gene adjacencies is computed (consistent with the reconciled gene trees), that might not be compatible with a linear ancestral gene order;
- for each ancestral species, a subset of the candidate ancestral adjacencies is computed, using spp_dcj, that is compatible with a linear gene order.

### Pipeline 3, based on DeCoSTAR,ecceTERA

The third pipeline takes advantage of the fact that the parsimony reconciliation algorithm ecceTERA is implemented within DeCoSTAR:
- for each gene family, an MSA is computed using MACSE;
- for each gene family, a sample of gene trees is computed from its MSA using IQ-TREE;
- for each gene family, a reconciled gene tree is computed from the sampled gene trees using ecceTERA;
- for each ancestral species, a set of candidate ancestral gene adjacencies is computed (consistent with the reconciled gene trees), that might not be compatible with a linear ancestral gene order;
- for each ancestral species, a subset of the candidate ancestral adjacencies is computed, using spp_dcj, that is compatible with a linear gene order.

In this pipeline, the reconciled gene trees are not generated explicitly and are only created as input to the DeCoSTAR ancestral adjacencies inference algorithm.

### Alternative pipelines

AGO allows to define alternative pipeline, where MSAs, gene trees and
reconciled gene trees can have been generated independently to AGO and
are provided to further steps.

For example, AGO allows a user to compute a sample of gene trees for
each gene family using another method than IQ-TREE, such as <a
href="https://nbisweden.github.io/MrBayes/">MrBayes</a>, followed by
pipeline steps that rely on such gene trees (`ALE+DeCoSTAR+spp_dcj` as
in pipeline 2 or `DeCoSTAR+spp_dcj` as in pipeline 3).

Creating such a pipeline can be done by creating a pipeline YAML
paramaters file in which the path to an existing gene trees data file
is specified.

Alternative pipeline can also skip the last step, `spp_dcj`, in which
case only (potentially conflicting) ancestral adjacencies are
computed.

### Creating a pipeline.

Creating an AGO pipeline is done in two steps:
- creating a pipeline YAML header file, by editing a copy of the header template file [header_template.yaml](header_template.yaml) to specify input data files, pipeline tools and pipeline tools options;
- running the command AGO `create`.

For example, in the directory [example](../example), an implementation of pipeline 1 (`Generax+DeCoSTAR+spp_dcj`) to reconstruct ancestral gene orders of the X chromosomes of three *Anopheles* mosquito species is provided, obtained by
- creating the file [anopheles_X_GeneRax_header.yaml](../example/anopheles_X_GeneRax_header.yaml),
- running the command `python src/AGO.py example/anopheles_X_GeneRax.yaml create example/anopheles_X_GeneRax_header.yaml parameters MACSE GeneRax DeCoSTAR SPPDCJ`,
resulting in a pipeline parameters file [anopheles_X_GeneRax.yaml](../example/anopheles_X_GeneRax.yaml).

### Running a pipeline.

A pipeline can then be ran, from a pipeline parameters file, by a sequence of AGO commands `init`, `slurm`, `bash`, `check` and `stats`.

For example, for the pipeline defined by [anopheles_X_GeneRax.yaml](../example/anopheles_X_GeneRax.yaml):
```
python src/AGO.py example/anopheles_X_GeneRax.yaml init
```
This will initialize the pipeline, creating its directory architecture and local versions of the input data files.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml slurm MACSE
```
This will create a `slurm` script to run `MACSE`, that can be launched by the `slurm` command `sbatch`.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml check MACSE
```
This will check the results of `MACSE`, creating log files and a data file describing the MSA that were computed.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml slurm GeneRax
```
This will create a `slurm` script to run `GeneRax`, that can be launched by the `slurm` command `sbatch`.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml check GeneRax
```
This will check the results of `GeneRax`, creating log files and a data file describing the reconciled gene trees that were computed.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml stats GeneRax
```
This will create CSV files that describes statistics of the reconciled gene trees.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml bash DeCoSTAR
```
This will create a `bash` script to run `DeCoSTAR`.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml check DeCoSTAR
```
This will check the results of `DeCoSTAR`, creating log files and a data file describing the ancestral adjacencies that were computed.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml stats DeCoSTAR
```
This will create CSV files that describes statistics of the ancestral adjacencies.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ_ILP
```
This will create a `slurm` script to create the input (Integer Linear Program, ILP) required by `spp_dcj`.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ_ILP
```
This will check that the ILP required by `spp_dcj` has been properly computed.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ
```
This will create a `slurm` script to run `spp_dcj` (solving the ILP), computed conflict-free adjacencies for each ancestral species.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ
```
This will check the results of `spp-dcj`.
```
python src/AGO.py example/anopheles_X_GeneRax.yaml stats SPPDCJ
```
This will create CSV files that describes statistics of the ancestral adjacencies subsets defining ancestral gene orders.

We refer to [example/README.md](../example/README.md) for a precise
description of running the three pipelines on the *Anopheles* X
chromosome dataset.  

As it can be seen above, an AGO pipeline is not a single script that
runs all steps at once.  This is motivated by the fact that each step
of a phylogenomics pipeline is prone to errors (due to implemntation
bugs of the considered tools for example, or inconsistencies with the
input data formats), or might require to be tested with different
options (e.g. in terms of the considered evolutionary model). So AGO
is designed in such a way tha a user is given the possibility to
explore the results of a step, possibly to run it several times with
various options, before providing its output to the next step; the
creation of statistics files after each step allows the user to rely
on high-level statistics in order to assess the quality of the
computed results.


Currently, the commands `slurm`, `bash` and `check` are available for
all tools (`MACSE`, `IQ-TREE`, `GeneRax`, `ALE`, `DeCoSTAR`,
`spp_dcj`), while the command `stats` is not available for te tools
`MACSE` and `IQ-TREE`.

## Data Formats

Define a data file, in terms of object and definition of the object: family, gene order, species tree, species, alignment, gene tree, reconciliation, adjacencies.

Data file format: object ID, definition.

Object IDs: alphanumeric only.

Species tree: ancestral species.

Object files format: FASTA, newick, recphyloxml, gene order, adjacency.

## Pipeline tools

### MACSE

### IQ-TREE

### ALE

### GeneRax

### DeCoSTAR

### SPP_DCJ

## Pipeline creation and running

### Editing the parameters file header, creating and initializing.

### Running tools: slurm/bash, check, stats



## Future work

Extant adjacencies and scaffolding

bali-phy

HGT

intermediate steps