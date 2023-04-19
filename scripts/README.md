# AGO scripts

## Data manipulation scripts

`data_utils.py`:
- Auxiliary functions to manipulate AGO data files.

`newick_utils.py`:
- Auxiliary functions to manipulate Newick and NHX trees.
- USAGE:
  - Creates a species file from a species tree: `python newick_utils.py species <input: Newick species tree file> <output: species file>`
  - Removes ancestral species names from a species tree: `python newick_utils.py unlabel <input: Newick species tree file> <output: Newick species tree file with unlabeled ancestral nodes>`

`gene_orders_utils.py`:
- Creates a gene order FASTA-like files from gene adjacencies for a given species.
- USAGE: `python gene_orders_utils.py <input: DeCoSTAR genes file> <input file: gene adjacencies> <output: output directory> <output: gene order file>`

`recPhyloXML_utils.py`:
- Auxiliary functions to manipulate recPhyloXML files.

`recPhyloXML_statistics.py`:
- Creates CSV files describing reconciliation statistics for an AGO dataset.
- USAGE: `python recPhyloXML_statistics.py <input: AGO reconciliations file> <output: statistics per species CSV file> <output: statistics per gene family CSV file>`

## ALE scripts

`ale_splitter.py`:
- Extracts reconciliations and species tree from the ALE results file.
- Cloned from https://github.com/AADavin/ALEtutorial
- USAGE: `python ale_splitter.py -i <ALE results file> -stfr`

`ALEtoRecXML.py, ReconciledTree.py`:
- Creates recPhyloXML files from the output of ALE.
- Cloned from https://github.com/WandrilleD/recPhyloXML
- USAGE: `python ALEtoRecPhyloXML.py -g <input: ALE NHX reconciliation file> -o <output: ALE recPhyloXML file> -s <input: species name / gene name separator (|)> -st <input: ALE species tree file>`
   
`ALE_reformat.py`: 
- Reformats the reconciliations recPhyloXML files created by ALE by renaming ancestral species and gene names to be consistent with AGO data.
- USAGE: `python ALE_reformat.py <input: AGO species tree file> <input: ALE species tree file> <input: ALE recPhyloXML file> <output: AGO recPhyloXML file>` 

## GeneRax scripts

`GeneRax_create_input_files.py`:
- Creates, from AGO data, the input files required by GeneRax.
- USAGE: `python GeneRax_create_input_files.py <input: AGO gene families file> <input: AGO gene orders file> <input: AGO alignments file> <input: alignments files suffix> <input: substitution model> <output: GeneRax gene families file> <output: GeneRax genes/species map file>`

`GeneRax_reformat.py`:
- Reformats GeneRax recPhyloXML recociliations files to be consistent with DeCoSTAR expected format.
- USAGE: `python GeneRax_reformat.py <input: GeneRax gene families file> <input: GeneRax results directory> <input: output recPhyloXML files suffix (.recPhyloXML)>`

## DeCoSTAR scripts

`DeCoSTAR_create_input_files.py`:
- Creates, from AGO data, the input files required by DeCoSTAR.
- USAGE: `python DeCoSTAR_create_input_files.py <input: AGO gene orders file> <input: AGO reconciliations file> <input: AGO gene families file> <output: DeCoSTAR gene adjacencies file> <output: DeCoSTAR gene trees distribution file>`

`DeCoSTAR_reformat.py`:
- Reformats DeCoSTAR results files to be consistent with AGO data.
- USAGE: 
```
python DeCoSTAR_reformat.py <input: AGO species file> <input: DeCoSTAR species file> <input: already.reconciled tag (true/false)> <input: AGO gene families file>
<input: AGO gene trees (if already.reconcilied=false) or reconciliations (if already.reconcilied=true) file>
<input: DeCoSTAR gene trees distribution file> <input: DeCoSTAR results genes file> <input: DeCoSTAR results adjacencies file>
<output: AGO-compatible reformated DeCoSTAR results genes file> <output: directory where AGO-compatible adjacencies files (one per species) are written>
```

`DeCoSTAR_statistics.py`:
- Creates CSV files about gene adjacncies generated by DeCoSTAR.
- USAGE: `python DeCoSTAR_statistics.py <input: AGO species file> <input: AGO-compatible DeCoSTAR results genes file> <input: AGO adjacencies file> <input: list of weight thresholds for statistics> <output: DeCoSTAR per-species statistics CSV file>`

## SPP_DCJ scripts

`SPPDCJ_create_input_files.py,SPPDCJ_make_linearizable.py`:
- Scripts to create the input files to SPP_DCJ.
- USAGE:
  - `python SPPDCJ_create_input_files.py <input: AGO adjacencies file> <input: AGO species tree file> <input: list of species to consider ('all' if all species)> <input: minimum adjacency weight threshold to consider an adjacency (e.g. 0.5)> <output: SPP_DCJ species tree file> <output: SPP_DCJ adjacencies file>`
  - `python SPPDCJ_make_linearizable.py <input: SPP_DCJ adjacencies file> <output: SPP_DCJ complemented adjacencies file> <output: SPP_DCJ ILP creation log file>`1

`SPPDCJ_adjs_to_component.py`: 
- Decomposes the adjacency set from the input file into components and outputs these into genome-specific tab-separated (TSV) files.
- USAGE: `python SPPDCJ_adjs_to_components.py -p -o <output: SPP_DCJ statistics files directory> <input: SPP_DCJ adjacencies file> <output: log file>`

`SPPDCJ_reformat.py`:
- Reformats the SPP_DCJ adjacencies into AGO adjacencies.
- USAGE: `python SPPDCJ_reformat.py <input: AGO adjacencies file> <input: SPP_DCJ results adjacencies file> <output: directory for SPP_DCJ results>`

`SPPDCJ_statistics.py`:
- Creates a CSV statistics file on the result of solving the SPP_DCJ ILP.
- USAGE: `python SPPDCJ_statisticst.py <input: AGO adjacencies file> <input: SPP_DCJ results adjacencies file> <output: statistics CSV file>`
