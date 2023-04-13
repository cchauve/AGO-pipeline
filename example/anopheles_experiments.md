# Reconstructing Anopheles ancestral X chromosome gene orders

```
Mon Apr 10 12:19:06 PDT 2023 - Tue Apr 11 21:12:14 PDT 2023
```

## Data

## GeneRax-based pipeline

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml create example/anopheles_X_GeneRax_header.yaml parameters MACSE GeneRax DeCoSTAR SPPDCJ
        example/anopheles_X_GeneRax.yaml
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt will be computed.
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm MACSE
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
Submitted batch job 65060860
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check MACSE
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/MACSE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
Submitted batch job 65065308
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check GeneRax
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/GeneRax.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_families.csv
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses:transfers
node2:492:41:0:0
AnophelesgambiaePEST:471:6:30:0
AnophelesfunestusFUMOZ:472:2:25:0
node0:495:0:36:0
AnophelesatroparvusEBRO:503:15:43:0
node1:531:39:0:0
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml bash DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > chmod 755 /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh \
	      2> /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.err \
	      1> /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.log
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_X.txt
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
node0:495:0.5   474:449:34:126
node1:531:0.5   462:364:7:341
node2:492:0.5   332:225:1:535
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
Submitted batch job 65067302

```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ_ILP
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
Submitted batch job 
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python scripts/gene_orders_utils.py \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/results/DeCoSTAR/genes_reformatted.txt \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/results/SPPDCJ/ \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_ago_X.txt
```

## ALE-based pipeline

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml create example/anopheles_X_ALE_header.yaml parameters IQ-TREE ALE DeCoSTAR SPPDCJ
        example/anopheles_X_ALE.yaml
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml init
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm IQ-TREE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
Submitted batch job 64806164
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check IQ-TREE
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
Submitted batch job 64917920
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check ALE

```

There were 65 families involving transfers.

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_species.csv
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_families.csv
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_species.csv
```

The families discarded due to transfers included most families with reconciliation events.

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check DeCoSTAR
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats DeCoSTAR
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv; \
	      grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv | sort
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ_ILP
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
Submitted batch job
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ_ILP
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
Submitted batch job 
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python scripts/gene_orders_utils.py \
	      /scratch/chauvec/SPP/anopheles_X_ALE/results/DeCoSTAR/genes_reformatted.txt \
	      /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt \
	      /scratch/chauvec/SPP/anopheles_X_ALE/results/SPPDCJ/ \
	      /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_orders_ago_X.txt
```

## ecceTERA-based pipeline

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline >python src/AGO.py example/anopheles_X_ecceTERA.yaml create example/anopheles_X_ecceTERA_header.yaml parameters DeCoSTAR SPPDCJ
        example/anopheles_X_ecceTERA.yaml
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml init
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check DeCoSTAR
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv; \
	      grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv | sort
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ_ILP
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
Submitted batch job 

```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ_ILP
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
Submitted batch job 
```

```
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ
(AGO_python3) [chauvec@cedar1.cedar.computecanada.ca] AGO-pipeline > python scripts/gene_orders_utils.py \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/results/DeCoSTAR/genes_reformatted.txt \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/results/SPPDCJ/ \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_ago_X.txt
```
