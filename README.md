# AGO, a Pipeline for Ancestral Gene Orders Reconstruction

### Evan Cribbie, Cedric Chauve.
### Contact: cedric.chauve@sfu.ca

## Overview

- Reconstructing ancestral gene orders from homologous gene families.
- Multiple steps, multiple tools.
- HPC: slurm

## Installation

Python version 3.8.10. Virtual environment (https://docs.python.org/3.8/library/venv.html).
Packages:
- ete3:3.1.2
- matplotlib:3.7.0
- networkx:3.1
- numpy:1.24.2
- pandas:1.5.3
- PyYAML:6.0


External tools:
- Multiple sequence alignments: <a href="https://bioweb.supagro.inra.fr/macse/">MACSE, version 2.06</a>; requires <a href="https://openjdk.org/">Java, OpenJDK version 17.0.2</a>.
- Gene trees: <a href="http://www.iqtree.org/">IQ-TREE, version 2.0.7</a>.
- Reconciliations: <a href="https://github.com/ssolo/ALE">ALE, version 1.0</a>.
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

## Example

Reconstructing the X chromosome gene order of *Anopheles* mosquitoes genomes using different methods.
- GeneRax: [Anopheles example parameters file](example/anopheles_X_GeneRax.yaml).
- IQ-TREE+ALE: [Anopheles example parameters file](example/anopheles_X_ALE.yaml).
- IQ-TREE+ecceTERA: [Anopheles example parameters file](example/anopheles_X_ecceTERA.yaml).

**TO REWRITE**


### Data

Make data available on zenodo and provide documentation about how the data was obtained.


### Initalization


```
> python src/AGO.py example/anopheles_X.yaml init
        <DATA_DIR>/species_tree_4.newick -> <EXP_DIR>/data/species_tree_4.newick.
        <DATA_DIR>/species_4.txt -> <EXP_DIR>/data/species_4.txt.
        <DATA_DIR>/families_X_4.txt -> <EXP_DIR>/data/families_X_4.txt.
        <DATA_DIR>/sequences_X_4.txt -> <EXP_DIR>/data/sequences_X_4.txt.
        <DATA_DIR>/gene_orders_X_4.txt -> <EXP_DIR>/data/gene_orders_X_4.txt.
        <EXP_DIR>/data/alignments_X_4.txt will be computed.
        <EXP_DIR>/data/reconciliations_X_4.txt will be computed.
        <EXP_DIR>/data/adjacencies_X_4.txt will be computed.
> wc -l <EXP_DIR>/data/families_X_4.txt
451 <EXP_DIR>/data/families_X_4.txt
```

### Multiple Sequences Alignments

```
> python src/AGO.py example/anopheles_X.yaml script MACSE
        <EXP_DIR>/aux/MACSE/MACSE.sh
> sbatch <EXP_DIR>/aux/MACSE/MACSE.sh
Submitted batch job 64349391
```

```
> python src/AGO.py example/anopheles_X.yaml check MACSE
        <EXP_DIR>/log/MACSE.log
        <EXP_DIR>/data/alignments_X_4.txt
> grep -c "ERROR" <EXP_DIR>/log/MACSE.log
0
```

### Reconciled Gene Trees

```
> python src/AGO.py example/anopheles_X.yaml script GeneRax
        <EXP_DIR>/aux/GeneRax/GeneRax.sh
> sbatch <EXP_DIR>/aux/GeneRax/GeneRax.sh
Submitted batch job 64566124
```

```
> python src/AGO.py example/anopheles_X.yaml check GeneRax
        <EXP_DIR>/log/GeneRax.log
        <EXP_DIR>/data/reconciliations_X_4.txt
> grep -c "ERROR" <EXP_DIR>/log/GeneRax.log
0
> wc -l <EXP_DIR>/data/reconciliations_X_4.txt
451 <EXP_DIR>/data/reconciliations_X_4.txt
> python src/AGO.py example/anopheles_X.yaml stats GeneRax
        <EXP_DIR>/statistics/GeneRax/GeneRax_species.csv
        <EXP_DIR>/statistics/GeneRax/GeneRax_families.csv
> cat <EXP_DIR>/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses
node2:492:41:0
AnophelesgambiaePEST:471:6:30
AnophelesfunestusFUMOZ:472:2:25
node0:495:0:34
AnophelesatroparvusEBRO:503:16:42
node1:529:37:0
AnophelesalbimanusSTECLA:489:8:11
```

### Ancestral Adjancecies

```
> python src/AGO.py example/anopheles_X.yaml script DeCoSTAR
        <EXP_DIR>/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch <EXP_DIR>/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 64567288
```

```
> python src/AGO.py example/anopheles_X.yaml check DeCoSTAR
        <EXP_DIR>/log/DeCoSTAR.log
        <EXP_DIR>/data/adjacencies_X_4.txt
> grep -c "ERROR" <EXP_DIR>/log/DeCoSTAR.log
0
> python src/AGO.py example/anopheles_X.yaml stats DeCoSTAR
        <EXP_DIR>/statistics/DeCoSTAR/DeCoSTAR.csv
        <EXP_DIR>/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
> grep node <EXP_DIR>/statistics/DeCoSTAR/DeCoSTAR.csv
#node2
node2:492:0.1   335:230:4:528
node2:492:0.2   335:230:4:528
node2:492:0.3   335:230:4:528
node2:492:0.4   334:228:2:530
node2:492:0.5   331:224:0:536
node2:492:0.6   331:223:0:538
node2:492:0.7   329:222:0:540
node2:492:0.8   329:222:0:540
node2:492:0.9   329:222:0:540
node2:492:1.0   329:222:0:540
#node1
node1:529:0.1   476:403:43:295
node1:529:0.2   476:403:43:295
node1:529:0.3   475:402:42:296
node1:529:0.4   466:380:21:319
node1:529:0.5   462:368:11:333
node1:529:0.6   453:356:5:351
node1:529:0.7   448:349:2:362
node1:529:0.8   446:347:2:366
node1:529:0.9   444:346:2:368
node1:529:1.0   444:346:2:368
#node0
node0:495:0.1   476:459:40:112
node0:495:0.2   476:459:40:112
node0:495:0.3   476:459:40:112
node0:495:0.4   476:457:39:115
node0:495:0.5   474:448:33:127
node0:495:0.6   469:436:28:146
node0:495:0.7   459:413:6:170
node0:495:0.8   451:404:3:185
node0:495:0.9   450:403:2:186
node0:495:1.0   450:403:2:186
```

### Ancestral Gene Orders

```
> python src/AGO.py example/anopheles_X.yaml script SPPDCJ_ILP
        <EXP_DIR>/aux/SPPDCJ_ILP/SPPDCJ_ILP_all.sh
> sbatch  <EXP_DIR>/aux/SPPDCJ_ILP/SPPDCJ_ILP_all.sh
Submitted batch job 64569034
```

```
> python src/AGO.py example/anopheles_X.yaml check SPPDCJ_ILP
        <EXP_DIR>/log/SPPDCJ_ILP_all.log
        No output file is created
> cat <EXP_DIR>/log/SPPDCJ_ILP_all.log
#status tool    index   message
SUCCESS SPPDCJ_ILP              <EXP_DIR>/results/SPPDCJ_ILP/all_0.5_0.5_0.25.idmap
SUCCESS SPPDCJ_ILP              <EXP_DIR>/results/SPPDCJ_ILP/all_0.5_0.5_0.25.ilp
> grep telomere <EXP_DIR>/log/SPPDCJ_ILP/SPPDCJ_ILP_all.err
INFO    2023-04-05 13:54:33,494 identified 214 candidate telomeres in genome node2
INFO    2023-04-05 13:54:33,495 identified 210 candidate telomeres in genome node1
INFO    2023-04-05 13:54:33,496 identified 2 candidate telomeres in genome AnophelesalbimanusSTECLA
INFO    2023-04-05 13:54:33,496 identified 116 candidate telomeres in genome node0
INFO    2023-04-05 13:54:33,496 identified 2 candidate telomeres in genome AnophelesatroparvusEBRO
INFO    2023-04-05 13:54:33,497 identified 2 candidate telomeres in genome AnophelesgambiaePEST
INFO    2023-04-05 13:54:33,497 identified 2 candidate telomeres in genome AnophelesfunestusFUMOZ
> python src/AGO.py example/anopheles_X.yaml stats SPPDCJ_ILP
        <EXP_DIR>/statistics/SPPDCJ_ILP/components_all.log
```

```
> python src/AGO.py example/anopheles_X.yaml script SPPDCJ
        <EXP_DIR>/aux/SPPDCJ/SPPDCJ_all.sh
> sbatch <EXP_DIR>/aux/SPPDCJ/SPPDCJ_all.sh
Submitted batch job 64365862
```

```
> python src/AGO.py example/anopheles_X.yaml check SPPDCJ
        <EXP_DIR>/log/SPPDCJ_all.log
        <EXP_DIR>/data/adjacencies_ago_X_4.txt
> python src/AGO.py example/anopheles_X.yaml stats SPPDCJ
        <EXP_DIR>/statistics/SPPDCJ/SPPDCJ_species.csv
> cat <EXP_DIR>/statistics/SPPDCJ/SPPDCJ_species.csv
#species        <number of adjacencies>:<total weight>:<kept adjacencies>:<kept weight>
node2   231:225.73899999999998:224:223.24099999999999
node1   404:372.4:357:350.543
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   460:436.963:416:409.47600000000006
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
> python scripts/gene_orders_utils.py \
       <EXP_DIR>/results/DeCoSTAR/genes_reformatted.txt \
       <EXP_DIR>/data/adjacencies_ago_X_4.txt \
       <EXP_DIR>/results/SPPDCJ/ \
       <EXP_DIR>/data/gene_orders_ago_X_4.txt
```