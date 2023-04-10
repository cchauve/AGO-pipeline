# Reconstructing Anopheles ancestral X chromosome gene orders

```
[chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > source AGO_python3/bin/activate
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > date
Mon Apr 10 12:19:06 PDT 2023
```

## Data

## GeneRax-based pipeline

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt will be computed.
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > wc -l /scratch/chauvec/SPP/anopheles_X_GeneRax/data/families_X_4.txt
451 /scratch/chauvec/SPP/anopheles_X_GeneRax/data/families_X_4.txt
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml script MACSE
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
Submitted batch job 64800694
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check MACSE
        /scratch/chauvec/SPP/anopheles_X_GeneRax/log/MACSE.log
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > grep -c ERROR /scratch/chauvec/SPP/anopheles_X_GeneRax/log/MACSE.log
0
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml script GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
Submitted batch job 64806136
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/log/GeneRax.log
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > grep -c ERROR /scratch/chauvec/SPP/anopheles_X_GeneRax/log/GeneRax.log
0
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml script DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 64806808
```


## ALE-based pipeline

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_ALE/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/alignments_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/reconciliations_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt will be computed.
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > cp /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt /scratch/chauvec/SPP/anopheles_X_ALE/data/
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml script IQ-TREE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
Submitted batch job 64806164
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check IQ-TREE
        /scratch/chauvec/SPP/anopheles_X_ALE/log/IQ-TREE.log
        /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > grep -c ERROR /scratch/chauvec/SPP/anopheles_X_ALE/log/IQ-TREE.log
0
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml script ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
Submitted batch job 64806848
```

## ecceTERA-based pipeline

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/alignments_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_trees_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt will be computed.
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > cp /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > cp /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml script DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 64806886
```