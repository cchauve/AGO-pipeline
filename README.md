# AGO, a Pipeline for Ancestral Gene Orders Reconstruction

AGO is a tool aimed at creating pipelines of existing bioinformatics
tools for reconstructing ancestral gene orders from extant gene orders
and homologous gene families, in a phylogenetic context.

## Overview

AGO is based on the general methodology described in <a
href="https://doi.org/10.1007/978-1-4471-5298-9_4">Duplication,
Rearrangement and Reconciliation: A Follow-Up 13 Years Later</a>
(see also the review <a
href="https://doi.org/10.1007/978-1-4939-7463-4_13">Comparative
Methods for Reconstructing Ancient Genome Organization</a>).  It
consists in the following steps:
- computing a multiple sequences
alignment (MSA) for each homologous gene family;  
- computing a gene
tree, or sample of gene trees, from the MSA for each gene family;  
- computing a reconciled gene tree, from the MSA and/or gene tree(s),
for each gene family;  
- computing ancestral gene adjacency candidates
from the extant gene orders and the reconciled gene trees;  
- clearing
conflicts from the set of candidate ancestral gene adjacency (Small Parsimony
Problem).  

This approach allows to account for the full complement of genes in
extant genomes, at the expense of necessitating several steps,
implemented in various tools, that are not trivial to interface
together into a pipeline. AGO is aimed at easing the creation of such
pipelines; AGO in itself dos not introduce any novel algorithm, and
aims solely at allowing to create pipelines based on published
existing tools.

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
- Multiple sequence alignments: <a href="https://bioweb.supagro.inra.fr/macse/">MACSE, version 2.06</a>; requires <a href="https://openjdk.org/">Java, OpenJDK version 17.0.2</a>.
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

## Documentation

The [AGO manual](doc/manual.md) describes how to create and run a pipeline.

AGO is illustrated in a test case, focusing on the reconstruction of
the ancestral gene orders of the X chromosome of *Anopheles*
mosquitoes genomes using different implementations of the methodology
described above:
- Computing reconciled gene trees from MSAs using <a href="https://github.com/BenoitMorel/GeneRax">GeneRax</a>.
- Computing gene trees from MSAs using <a href="http://www.iqtree.org/">IQ-TREE</a> and reconciled gene trees from the gene trees using <a href="https://github.com/ssolo/ALE">ALE</a>.
- Computing gene trees from MSAs using <a href="http://www.iqtree.org/">IQ-TREE</a> and reconciled gene trees using <a href="https://github.com/WandrilleD/DeCoSTAR">DeCoSTAR</a>.

These experiments are described in [example/README.md](./example/README.md).

### Contact
cedric.chauve@sfu.ca
