# AGO, a Pipeline for Ancestral Gene Orders Reconstruction

### Evan Cribbie, Cedric Chauve.
### Contact: cedric.chauve@sfu.ca

## Overview

- Reconstructing ancestral gene orders from homologous gene families.
- Multiple steps, multiple tools.
- HPC: <a href="https://slurm.schedmd.com/">slurm</a>.

## Installation

Python version 3.8.10. Virtual environment (https://docs.python.org/3.8/library/venv.html).
Packages:
- <a href="https://pypi.org/project/ete3/3.1.2/">ete3, version 3.1.2</a>
- <a href="https://matplotlib.org/3.7.1/">matplotlib, version 3.7.0</a>.
- <a href="https://pypi.org/project/networkx/3.1/">networkx, version 3.1</a>.
- <a href="https://numpy.org/">numpy, version 1.24.2</a>.
- <a href="https://pandas.pydata.org/pandas-docs/version/1.5.3/">pandas, version 1.5.3</a>.
- <a href="https://pypi.org/project/PyYAML/6.0/">PyYAML, version 6.0</a>.


External tools:
- Multiple sequence alignments: <a href="https://bioweb.supagro.inra.fr/macse/">MACSE, version 2.06</a>; requires <a href="https://openjdk.org/">Java, OpenJDK version 17.0.2</a>.
- Gene trees: <a href="http://www.iqtree.org/">IQ-TREE, version 2.0.7</a>.
- Reconciled gene trees: <a href="https://github.com/ssolo/ALE">ALE, version 1.0</a>.
- Reconciled gene trees: <a href="https://github.com/BenoitMorel/GeneRax">GeneRax, version 2.1.0</a>.
- Ancestral adjacencies: <a href="https://github.com/WandrilleD/DeCoSTAR">DeCoSTAR, version 1.2</a>.
- Ancestral gene orders: <a href="https://github.com/danydoerr/spp_dcj">SPP_DCJ</a>; requires <a href="https://www.gurobi.com/">gurobi, version 10.0.1</a>.  


HPC scheduler: <a href="https://slurm.schedmd.com/documentation.html">slurm</a>.

## Documentation

### Usage

- Edit paramaters file, <a href="https://yaml.org/">YAML</a> format.
- Run sequentially on slurm for HPC computations or within virtual environment for AGO commands.

### Implementation

See [AGO manual](doc/manual.md).

## Examples

Reconstructing the X chromosome gene order of *Anopheles* mosquitoes genomes using different methods.
- [Anopheles example parameters file, GeneRax](example/anopheles_X_GeneRax.yaml).
- [Anopheles example parameters file, IQ-TREE+ALE](example/anopheles_X_ALE.yaml).
- [Anopheles example parameters file, IQ-TREE+ecceTERA](example/anopheles_X_ecceTERA.yaml).

README in example directory

### Data

Make data available on zenodo and provide documentation about how the data was obtained.


