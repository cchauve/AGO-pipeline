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
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_families.csv
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses
node2:492:41:0
AnophelesgambiaePEST:471:6:30
AnophelesfunestusFUMOZ:472:2:25
node0:495:0:34
AnophelesatroparvusEBRO:503:16:42
node1:529:37:0
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml script DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 64806808
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR.log
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_X.txt
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > grep -c ERROR /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR.log
0
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv; \
	      grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:495:0.5   474:448:33:127
node1:529:0.5   462:368:11:333
node2:492:0.5   331:224:0:536
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
Submitted batch job 64814991
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

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/DeCoSTAR.log
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_X.txt
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > grep -c ERROR /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/DeCoSTAR.log
0
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv; \
	      grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:472:0.5   450:420:4:108
node1:499:0.5   443:355:5:293
node2:483:0.5   330:224:0:518
```