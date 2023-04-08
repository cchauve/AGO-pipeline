# AGO Manual

## Data Formats

### Species Tree

The species tree is to be a rooted species tree in newick format. The species names are to be the same names as those used in naming genes (see section on gene names). The species tree is also required to contain distances for each branch length.

### Gene Names

For all non mentioned software gene naming can be as desired.

#### Iqtree
Gene names must contain only alphanumerical,  "\_", or "|". This is because any other "non recognized" charachter will be converted to an underscore and will therefore change the gene name from the input to the output.

#### ALE
Gene names must be written as <specie><seperator><gene> where the seperator is to be specified when run.


For testing purposes we use "|" as separator and ensured that the only non alpha-numeric characters in gene or specie names (other than the separator) were "_" as these are accepted by Iq-tree and no renaming will be done.

## Pipeline

The principle of the pipeline is that all computations are specified in the
parameters file, a file in YAML format.

Scripts that are independent of the tools used as ins `src`.

Scripts specific to tools (such as creating the input files, formatting the
output, computing statistics) are in `scripts`.

The YAML file is designed in blocks, each with a specific purpose. A
quick description is provided below, and we refer to the comments in
the file `parameters/YGOB_test2_NT.yaml` for more details.

#### Block `run`: optional.
Contains miscalleanous variables used in the other blocks.
In the current file, it is used to set all values for parameters of tools
in such a way that only this block needs to ne modified.

#### Block `dir`: required.
Contains the paths to the run experiments
directories for data (`dir.data`), and for each tool `TOOL`,
- auxiliary files (tool-specific input files and Slurm scripts,
  `dir.aux/TOOL/`),
- log files (Slurm log files in `data.log/TOOL/` and AGO log files in
  `data.aux/TOOL.log`),
- results files created by SLurm scripts (`dir.results/TOOL`),
- statistics files (`dir.stats/TOOL/`).   

#### Block `data`: required.
Contains files giving the path to access the
various objects manipulated by AGO. For each object `OBJECT` a path to
access the file must be provided, optional additional files can also
be provided. Three objects are required as input:
- Species tree. Must be in Newick format and internal nodes
  names are ignored.
- Gene families. List of genes per family. Format: one family per
  line, <family ID><TAB><list of gene names separated by ' '>.
- Gene orders. Path for each extant species to a file describing its
  gene order. Format: one species per line, <species name><TAB><path>.

At initialization, the input files are copied in `dir_data` for
record-keeping, but they are used from their original location.  

Other AGO objects, that can either be provided as input or will be
computed by the AGO pipeline, are: 
- Sequences. Path for each gene family to a FASTA file containing the
  sequence of each gene. Format: one family per line,
  <family ID><TAB><path>. 
- Alignments. Path for each gene family to a FASTA file containing an
  MSA of the family genes. Format: one family per line,
  <family ID><TAB><path>.
- Gene trees. Path for each gene family to a file containing a
  gene tree for the family. Format: one family per line,
  <family ID><TAB><path>.
- Reconciled gene trees. Path for each gene family to a file containing a
  reconciled gene tree for the family. Format: one family per line,
  <family ID><TAB><path>.
- Species. List of species, extant and ancestral. Format:
  one species per line, <species name><TAB><['extant','ancestral']>.
  Currently, the ancestral species names are set in reconciliations.
- Adjacencies. Path for each gene species (extant ad ancestral) to a
  file containing adjacencies (possibly conflicting) for the
  species. Format: one species per line, <species name><TAB><path>.  
Assumptions:
- Species names in `data.gene_orders` do match leaves of `data.species_tree`.
- Extant species names in `data.species` do match leaves of `data.species_tree`.
- Extant species names in `data.adjacencies` do match leaves of `data.species_tree`.
- Genes in `data.gene_orders` do match genes in `data.families`.
- Gene in FASTA files from `data.sequences` do match genes in `data.families`.
- Families in `data.sequences` do match families in `data.families`.
- Gene sequences FASTA header of the form ">gene_name\n".

AGO works in a sequential way, with objects being generated in the
following order from the input (`data.species_tree`, `data.families`,
`data.gene_orders`): `data.alignments`, `data.reconciliations` (might
require `data.gene_trees` as an optional step), `data.adjacencies`.
Exactly one of `data.sequences`, `data.alignments`, `data.gene_trees`,
`data.reconciliations`, `data.adjacencies` must be provided as input,
and all other objects that follow in the AGO order must then be
specified and will be computed.

#### Block `slurm`: required.
Slurm parameters; `slurm.account` is required
and describes the account used to run the Slurm scripts.

#### Block `log`: required.

Contains properties for log files:
- `log.ext`: extensions for log files (both AGO and Slurm), Slurm
  error files and statistics files.
- `log.msg`: messages shown in AGO log files. 

#### Block `tools`: required.

This is the main block, that contains a sub-block for each tool that
will be run.

The principle is that each tool `TOOL` takes as input some of the data
described in the block `data`, that was either provided as input or
computed by tools of previous steps and generates:
- results, generated by a Slurm script, and stored in `dir.results/TOOL`,
- optionally, one of the data object file that will be used in a
  following step.

For each tool, the following sub-blocks are required:
- `tools.TOOL.name`: name of the tool used in directories and files
  names.
- `tools.TOOL.input`: input to the tool.
  - `tools.TOOL.input.file`, required: AGO object file(s) used as input.
  - `tools.TOOL.input.script`: optional. Command to create the tool input
    files from the specified AGO object file(s). This is defined by a list
    of strings that is concatenated and executed to create the input
    file(s).
  - Other optional fields can be added if needed.
- `tools.TOOL.output.file: required only if the step generates an AGO
  object file, specified in this field.
  
- `tools.TOOL.slurm`: required. Contains all informations to create
  the Slurm script that will run the tool. This includes.

  - `tools.TOOL.slurm.options`: non-array related Slurm parameters.
  - `tools.TOOL.slurm.modules`: modules to load . Can be omitted if none.

  - `tools.TOOL.slurm.array`: required if Slurm runs an array of jobs
    or if the creation of the output file requires an array-like
    process that iterates over many files created by Slurm. If Slurm
    runs an array of jobs, a sub-block `tools.TOOL.slurm.array.input`
    is required that describes how to create the individual job
    commands. If the output file requires to iterate over results
    files created by Slurm over the objects defined in
    `tools.TOOL.input.file`, a sub-block
    `tools.TOOL.slurm.array.results` is equired. Each block contains
    three fields that describe how to iterate over an AGO object file:
    `file` links to the file path, `field` defines which field in this
    file is the index to iterate over, `var` is the name of the
    environment variable created by this iteration.

  - `tools.TOOL.slurm.results`: required. Describes the expected results files
    generated by the Slurm job and that will be (1) checked to detect
    Slurm jobs that have failed, and (2) recorded in the output file,
    if one is created. The sub-block `files` describes the files
    linked to `tools.TOOL.slurm.array.results`, whlie the sub-block
    `other` defines the other results files.

  - `tools.TOOL.slurm.cmd`: required. Defines the command to be
    written in the Slurm script. This is defined by a list of strings
    that is concatenated and executed.

 `tools.TOOL.stats`: optional. Defines the statistics files that can
 be generated from the result of `TOOL` and the command to create such
 statistics files (sub-block `cmd`, required).  

For each tool `TOOL`, the Slurm script and input files are created by the command
```
python AGO.py <YAML parameters file> script TOOL
```
The created Slurm script can then be run with `sbatch`.

The expected AGO object output output file and log file are created
from the Slurm results by
```
python AGO.py <YAML parameters file> check TOOL
```

Finally, statistics can be computed with 
```
python AGO.py <YAML parameters file> stats TOOL
```

Each of these commands ends by showing the path to the files it
created.

