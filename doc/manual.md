# AGO Manual

## Overview

AGO is a suite of python scripts, aimed at implementing phylogenomics
pipelines for reconstructing ancestral syntenies and gene orders in a phylogenetic
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
- a set of input data files that include, at minima, a species tree, a set of gene families and gene orders for extant species, together with possibly additional data depending on the specific implemented pipeline;
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
- for each gene family, an MSA is computed using `MACSE`;
- for each gene family, a reconciled gene tree is computed from its MSA using `GeneRax`;
- for each ancestral species, a set of candidate ancestral gene adjacencies, that might not be compatible with a linear ancestral gene order, is computed using `DeCoSTAR`;
- for each ancestral species, a subset of the candidate ancestral adjacencies is computed, using `spp_dcj`, that is compatible with a linear gene order.

This pipeline does not compute explicitly gene trees for the gene families, that are explicitly defined by the reconciled gene trees.

### Pipeline 2, based on ALE

In the second pipeline, the following steps are implemented:
- for each gene family, an MSA is computed using `MACSE`;
- for each gene family, a sample of gene trees is computed from its MSA using `IQ-TREE`;
- for each gene family, a reconciled gene tree is computed from the sampled gene trees using `ALE`;
- for each ancestral species, a set of candidate ancestral gene adjacencies, that might not be compatible with a linear ancestral gene order, is computed using `DeCoSTAR`;
- for each ancestral species, a subset of the candidate ancestral adjacencies is computed, using `spp_dcj`, that is compatible with a linear gene order.

### Pipeline 3, based on ecceTERA

The third pipeline takes advantage of the fact that the parsimony reconciliation algorithm ecceTERA is implemented within DeCoSTAR:
- for each gene family, an MSA is computed using MACSE;
- for each gene family, a sample of gene trees is computed from its MSA using IQ-TREE;
- for each gene family, a reconciled gene tree is computed from the sampled gene trees using ecceTERA;
- for each ancestral species, a set of candidate ancestral gene adjacencies, that might not be compatible with a linear ancestral gene order, is computed using `DeCoSTAR`;
- for each ancestral species, a subset of the candidate ancestral adjacencies is computed, using `spp_dcj`, that is compatible with a linear gene order.

In this pipeline, the reconciled gene trees are not generated explicitly and are only created as input to the `DeCoSTAR` ancestral adjacencies inference algorithm.

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



## File Formats

The various tools interfaced into an AGO pipeline communicate through
data files, each associated to a specific kind of data: species tree,
species, gene orders, gene families, gene sequences, gene trees,
reconciled gene trees and adjacencies.

### Species and species tree

The *species tree* provided to an AGO pipeline is expected to be a
rooted tree, in Newick format, with labeled ancestral species and
branch lengths (see
[species tree](../data/VectorBase/species_tree_4.newick)).

The species names, for both extant and ancestral species, are expected
to be composed only of **alphanumeric characters** (a-z, A-Z, 0-9).

The *species file* is a tabulated file, where every line
indicates for each species the space-separated list of its extant
descendants, including the species itself if it is an extant species
(see [species file](../data/VectorBase/species_4.txt)).

The species file can be generated from the species tree using the command
```
python ./scripts/newick_utils.py species <species tree file> <species file>
```

**Any AGO pipeline requires a species tree file and a species file.**

### Gene families

A *gene family* is composed of a set of extant genes. The file
describing the set of all gene families is also a tabulated file where
each line defines a single family. Its format is
```
family name<TAB>space-separated list of genes in format <species name><SEP><gene name>
```
where `<SEP>` is specified separator character (suggested `|`).

As for species, the actual name of a gene is assumed to be composed
only of **alphanumeric characters**.

See [families file](../data/VectorBase/families_X_4.txt) for an
example.

**Any AGO pipeline requires a gene family input file.**

### Gene orders

A *gene orders* file is a tabulated file where each line contains the
path to the gene order file for an extant species:
```
extant species name<TAB>path to gene order file for the species
```

See [gene orders file](../data/VectorBase/gene_orders_X_4.txt)
for an example.


The gene order file for a given species is also a tabulated file where
each line describes one gene as follows:
```
species name<SEP>gene name<TAB>orientation (1 for forward, 0 for reverse)<TAB>start coordinate<TAB>end coordinate<TAB>unused field<TAB>chromosome/scaffold/contig
```

The genes are assumed to be **sorted first by location
(chromosome/scaffold/contig) and then by start coordinate**. Moreover,
AGO does assume that no gene is fully included (in terms of
coordinate) within another gene, although overlapping genes are
allowed, in which case their relative order is defined by their start
coordinate.

See [species gene order file](../data/VectorBase/gene_orders_X_4/AnophelesalbimanusSTECLA.txt)
for an example.

**Any AGO pipeline requires extant species gene orders.**

### Gene sequences

The sequence data associated to the considered genes is described in a
*sequences file*. This is a tabulated file, where each line describes
a unique sequence file (assumed to be in `FASTA` format) for the genes
of a single family:
```
family name<TAB>path to FASTA file for all genes in the family
```

See [sequences file](../data/VectorBase/sequences_X_4.txt)
for an example.

Sequence data is optional in an AGO pipeline, currently only needed if
MSAs are computed using `MACSE`.

### MSA

The MSAs associated to gene families, if used in the pipeline, are
described in a tabulated file in the format
```
family name<TAB>path to MSA file for the family
```
Currently, MSAs are computed by `MACSE` that creates, for each gene
family, two MSA files, one for nucleotide sequences (suffixed by
`_NT.fasta`) and one for amino-acid sequences (suffixed by
`_AA.fasta`).

The tools currently included in AGO and processing MSAs assume that a
single MSA is provided for each gene family. The AGO design however
allows to associate to a gene family a sample of MSAs, if some
subsequent steps would require such a representation of MSAs. This
will be considered in further developments of AGO.

### Gene trees and reconciled gene trees

Similarly to MSAs, the gene tree, or set of gene trees, associated to
gene families, are described in a tabulated file in the format
```
family name<TAB>path to gene tree(s) file for the family
```

In the current version of AGO, gene trees are computed by `IQ-TREE`,
under the form of a sample of bootstrap gene trees per family. This is
motivated by the fact that gen trees are used either by `ecceTERA` or
`ALE` to compute reconciled gene trees using the amalgamation method
that defines reconciled gene trees in terms of clades observed in a
sample of gene trees.

In the provided examples running `IQ-TREE` (file
[anopheles_X_GeneRax_header.yaml](../example/anopheles_X_GeneRax_header.yaml)),
1000 bootstrap gene trees are generated for each family.

Reconciled gene trees are described in the same way:
```
family name<TAB>path to reconciled gene tree file for the family
```

Reconciled gene trees are computed using either `GeneRax` (from an MSA
per family), `ALE` or `ecceTERA` (both from a sample of gene trees per
family). Reconciled gene trees are used by `DeCoSTAR` and are required
to be provided in the <a
href="http://phylariane.univ-lyon1.fr/recphyloxml/">recPhyloXML</a>
format.

### Gene adjacencies

Gene orders computed by AGO are represented in the form of oriented gene adjacencies, i.e. adjacencies between pairs of gene extremities. 
A gene adjacency file is associated to a single species. A dataset-wide set of gene adjacencies is described in a tabulated file in the format
```
species name<TAB>path to the an adjacencies file for the species
```

A gene adjacencies file for a given species is a space-separated file where each line encodes a single adjacency in the format
```
family 1 name<SEP>specie name<SEP>gene 1 name<SPACE>family 2 name<SEP>specie name<SEP>gene 2 name<SPACE>+/-<SPACE>+/-<SPACE>input weight<SPACE>output weight
```
- The first field `family 1 name<SEP>specie name<SEP>gene 1 name` encodes the first gene of the adjacency and includes the family it belongs to;
- The second field encodes similarly the second gene of the adjacency;
- The third field encodes the orientation of the first gene (`+` for forward, `-` for reverse);
- The fourth field encodes the orientation of the second gene;
- The fifth field encodes the prior weight associated to this adjacency (in [0,1], 1 for an extant adjacency);
- The last field encodes the post-DeCoSTAR weight associated to this adjacency (in [0,1], 1 for an extant adjacency).

The AGO pipelines implemented in [example](../example) compute 2 sets
of adjacencies per species, one that contains potentially conflicting
adjacencies computed by `DeCoSTAR` and a conflict-free set of
adjacencies computed from the `DeCoSTAR` adjacencies by `spp_dcj`.

## Pipeline tools

In this section, we describe several choices that are currently
enforced regarding the use of the tools integrated in AGO
pipelines. We refer to the references of the tools for detailed
explanations.
- `IQ-TREE` is used only in ultrafast bootstrap mode; the extension of the file computed by `IQ-TREE` used by AGO is `.ufboot`.
- `ALE` uses amalgamation for computing (sampling) a single reconciliation per gene family.
- Reconciliations generated by `ALE` that contain a gene transfer are discarded and the corresponding families are excluded from further steps.
- `DeCoSTAR` does not consider gene transfer in its model and samples ancestral adjacencies using Boltzmann sampling.

## Pipeline creation and running

### Editing the parameters file header

The main step in creating an AGO pipeline consists into editing the
file [header template](../paramaters/header_template.yaml). This file
is composed of five sections.

The section `run:` contains a single required field,
`run_dir_scripts`, the path to the directory containing the AGO
scripts (directory `scripts` of this repo).

Other fields can be added in order to create YAML variables that can
be reused. For example, in
[anopheles_X_GeneRax_header.yaml](example/anopheles_X_GeneRax_header.yaml),
this section contains several additional fields that are reused later
in the file.

```
run:
   # Run name
   - &run_name            'anopheles_X_GeneRax'
   # Root directory created by cloning the AGO pipline github repo
   - &run_dir_root        '/home/chauvec/projects/ctb-chauvec/AGO-pipeline'
   # VectorBase data
   - &run_vectorbase_data !join [*run_dir_root, 'data', 'VectorBase']
   # Directory containing the AGO pipeline scripts
   - &run_dir_scripts     !join [*run_dir_root, 'scripts']
   # Directory containing all files created by the AGO pipeline
   - &run_dir_exp         !join ['/home/chauvec/projects/ctb-chauvec/AGO-pipeline', 'example', *run_name]
   # Directory containing local installations of external tools
   - &run_dir_bin         !join [*run_dir_root, 'bin']
```

The YAML command `!join [ ... ]` allows to create a path by joining
all its arguments by the symbol `/`.

The section `slurm:` contains a single field, required only if the AGO
pipeline is to use the `slurm` job scheduling system. The required
field is the account used to run the pipeline processes.

The section `dir:` contains the path to the various directories
created by the pipeline. These directories do not have to be all
subdirectories of a same directory, although this is the most logical
approach, which is used in
[anopheles_X_GeneRax_header.yaml](example/anopheles_X_GeneRax_header.yaml)
```
dir:
   # Directory containing the input used by AGO and the output files created by AGO
   data:    &dir_data    !join [*run_dir_exp, 'data']
   # Directory containing the input files and running scripts for each external tool
   aux:     &dir_aux     !join [*run_dir_exp, 'aux']
   # Directory containing the log files of external tools and the AGO log files
   log:     &dir_log     !join [*run_dir_exp, 'log']
   # Directory containing the statistics files created by AGO
   stats:   &dir_stats   !join [*run_dir_exp, 'statistics']
   # Directory containing the results of external tools
   results: &dir_results !join [*run_dir_exp, 'results']
```
where the directory associated to this specific pipeline is
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/anopheles_X_GeneRax`
and contains directories named `data`, `aux`, `log`, `statistics` and
`results`.

The next section, `data:` contains the path to the files either used
as input by the pipeline or generated as output by the pipeline, as
well as some other variables that should not be edited
(`species_gene_name_separator`, `data_alignments_NT_ext`,
`data_alignments_AA_ext`, `.data_reconciliations_ext`,
`data_adjacencies_ext`, `data_ago_adjacencies_ext`).

The header file [anopheles_X_ALE_header.yaml (line
43)](../example/anopheles_X_ALE_header.yaml) illustrates how the results
of computations obtained with a different pipeline (in this case the
MSAs computed by the GeneRax-based pipeline) can be reused as input
data.

Also, depending on the implemented pipeline, some data are not needed
nor will be computed. For example, the GeneRax-based pipeline does not
generate gene trees, but directly reconciled gene trees from the MSAs,
so the fields related to gene trees in the template header have been
deleted.


Finally, the last section, `tools:` contains the parameters of the
external tools integrated into the pipeline. There is a section per
tool: it requires to be edited for the tools included in the pipeline,
and can be deleted for the tools that are not part of the pipeline.

Once a header file has been edited, a full parameters file can be
created by the command
```
python src/AGO.py <parameters file to be created> create <edited header file> <included tools: subset of MACSE, IQ-TREE, GeneRax, ALE, DeCoSTAR, SPPDCJ>
```
that combines the provided header file with the tool-specific files
available in [parameters](../parameters/) into a full pipeline
parameters file.

### Initialization

The initialization of a pipeline is done by the command
```
python src/AGO.py <parameters file> init
```

This creates, if needed, all the required directories, and copies the
existing data files (the input to the pipeline) into the `data`
directory of the pipeline.

**Remark.** Initializing a pipeline copies in the `data` directories
  the pipeline data files that, for most, contain the paths to files
  containing the actual data (such as the sequence data for the
  genes). But these actual data files are not copied themselves, so any
  modification of these files will render the results obtained by the
  pipeline out-dated, and re-running the pipeline will generate
  different results.

When initialized, AGO prints all data files for the pipeline and indicates if they already exist or will be computed.
For example:
```
python src/AGO.py example/anopheles_X_ALE.yaml init
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


### Running tools

Once a pipeline has been initialized, the tools it contain can be run
using the following commands. Let `TOOL` be any tool of the pipeline
(e.g. `MACSE`).

- `python src/AGO.py bash TOOL` creates a `bash` script to run
  `TOOL`. The path to the created script is printed.

- `python src/AGO.py slurm TOOL` creates a `slurm` script to run
  `TOOL`. As above, the path to the created script is printed.

For example:
```
python src/AGO.py example/anopheles_X_ALE.yaml slurm IQ-TREE
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
```

The slurm script `/home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh` is can then be run by
```
sbatch /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
```

Scripts to run a tool, as well as specific input files created from
the pipeline data, are always written in the `aux/TOOL` subdirectory
of the pipeline directory architecture.


The files created by the tool are written in the subdirectory
`results/<TOOL>` of the pipeline.

Once a tool has finished to run, and has generated result files, these
results files need to be recorded in the corresponding data files of
the pipeline. This is done with the `check` command.
```
python src/AGO.py example/anopheles_X_ALE.yaml check IQ-TREE
        ERRORS: 0
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/IQ-TREE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_trees_X.txt
```
This shows that the tool `IQ-TREE` generated as expected a gene trees
file per gene family (`ERRORS: 0`) and they have been recorded in the
gene trees data file of the pipeline
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/gene_trees_X.txt`.

Logs files are recorded in the log directory of the pipeline. For each
tool `TOOL`, a files `<TOOL>.log` is created that described which
expected files were computed or are missing, and a `TOOL` subdirectory
records all the log and error files generated by `slurm`. For example,
after running `ALE` next using the gene trees as input:
```
python src/AGO.py example/anopheles_X_ALE.yaml check ALE
        ERRORS: 66
        LOG:    /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/ALE.log
        OUTPUT: /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/data/reconciliations_X.txt
```

we can see that 66 expectted reconciliations files are missing (due to
the fact that AGO currently assumes an evolutionary model without gene
transfers and discards `ALE` results for families whose reconciled
gene tree contains a gene transfer). They can be identified by looking at the file
`/home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/ALE.log`:
```
grep ERROR /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/log/ALE.log
ERROR   ALE     OG6100220       /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/results/ALE/OG6100220.recphyloxml file is missing
ERROR   ALE     OG6100435       /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/results/ALE/OG6100435.recphyloxml file is missing
ERROR   ALE     OG6100445       /home/chauvec/projects/ctb-chauvec/AGO-pipeline/example/anopheles_X_ALE/results/ALE/OG6100445.recphyloxml file is missing
...
```
shows that for gene family `OG6100220` the expected reconciliation
file `results/ALE/OG6100220.recphyloxml` is not present.

In order to avoid propagating errors, the `check` command of AGO
discards from the further steps the families for which the computation
did not generate the expected file.

For tools `ALE, GeneRax, DeCoSTAR, spp_dcj`, an additional command
`stats` is available: running `python src/AGO.py stats TOOL` creates
one or several `csv` files recording statistics on the results
generated by the tool.

Last, the command `python src/AGO.py clean TOOL` deletes the files
generated by `TOOL`.

We refer to [example/README.md](../example/README.md) for detailed
illustrations of the three standard AGP pipelines.

As it can be seen above, an AGO pipeline is not a single script that
runs all steps at once.  This is motivated by the fact that each step
of a phylogenomics pipeline is prone to errors (due to implemntation
bugs of the considered tools for example, or inconsistencies with the
input data formats), or might require to be tested with different
options (e.g. in terms of the considered evolutionary model). So AGO
is designed in such a way that a user can analyze the results of a
step, possibly run it several times with various options, before
providing its output to the next step; the creation of statistics
files after each step allows the user to rely on high-level statistics
in order to assess the quality of the computed results.

## Implementation notes

The python code for creating and running the pipeline is in the directory `src`.

Python scripts that are specific to some tool or some data format,
used for example to create tool-specific input files or reformat the
result files of a tool in order that they are consistent with the pipeline data format,
are in the `scripts` directory (see [scripts/README.md](../scripts/README.md)).

The YAML code specific to run each tool is in the directory `parameters`. 


## Future work

The current release of AGO serves as a proof of concept for the idea
of an ancestral gene orders reconstruction pipeline, together with the
implementation of three different pipelines based on state-of-the-art
tools.

Future work will include an easier and less constrained
parameterization of the tools, the inclusion of new tools (for example
to compute MSAs or gene trees), the inclusion of options for the
reconciliation tools and `DeCoSTAR` to allow lateral gene transfer.

## References

1. Methodology: <a href="https://doi.org/10.1007/978-1-4471-5298-9_4">Duplication,
Rearrangement and Reconciliation: A Follow-Up 13 Years Later</a> (2013).

2. Methodology: <a href="https://doi.org/10.1007/978-1-4939-7463-4_13">Comparative
Methods for Reconstructing Ancient Genome Organization</a> (2018).

3. MACSE: <a href="https://doi.org/10.1371/journal.pone.0022594">MACSE: Multiple
Alignment of Coding SEquences Accounting for Frameshifts and Stop
Codons</a> (2011).

4. IQ-TREE: <a href="https://doi.org/10.1093/molbev/msaa015">IQ-TREE 2: New models
and efficient methods for phylogenetic inference in the genomic
era</a> (2020).

5. IQ-TREE: <a href="https://doi.org/10.1093/molbev/msx281">UFBoot2: Improving the
ultrafast bootstrap approximation</a> (2018).

6. GeneRax: <a href="https://doi.org/10.1093/molbev/msaa141">GeneRax: A Tool for
Species-Tree-Aware Maximum Likelihood-Based Gene Family Tree Inference
under Gene Duplication, Transfer, and Loss</a> (2020).

7. ALE: <a href="https://doi.org/10.1093/sysbio/syt054">Efficient exploration
of the space of reconciled gene trees</a> (2013).

8. DeCoSTAR: <a href="https://doi.org/10.1093/gbe/evx069">DeCoSTAR: Reconstructing
the Ancestral Organization of Genes or Genomes Using Reconciled
Phylogenies</a> (2017).

9. spp_dcj: <a href="https://doi.org/10.1142/S0219720021400096">Small parsimony
for natural genomes in the DCJ-indel model</a> (2021).

10. Reconciliations: <a href="https://hal.science/hal-02535529">Reconciling Gene trees with
Species Trees</a> (2020).

11. Reconciliations: <a href="https://doi.org/10.1371/journal.pcbi.1010621">Phylogenetic
reconciliation</a> (2022).

12. Methodology: <a href="https://inria.hal.science/PGE/hal-02535466">Ancestral Genome
Organization as a Diagnosis Tool for Phylogenomics</a> (2020).

13. RecPhyloXML: <a href="https://doi.org/10.1093/bioinformatics/bty389">RecPhyloXML: a
format for reconciled gene trees</a> (2018).

