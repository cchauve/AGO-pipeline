# Reconstructing Anopheles ancestral X chromosome gene orders

```
Thu Apr 13 20:41:55 PDT 2023
```

## Data

## GeneRax-based pipeline

We first create a parameters file for a pipeline that uses, in
sequence, MACSE to compute alignments based on nucleotide sequences,
GeneRax to compute reconciled gene tres from these alignments,
DeCoSTAR to compute ancestral adjacencies, and spp_dcj to compute a
set of conflict-free adjacencies defining ancestral gen orders.

To create this pipeline, we first created the pipeline-specific YAML file
[Anopheles example parameters file header, GeneRax pipeline](example/anopheles_X_GeneRax_header.yaml)
from
[header template](parameters/header_template.yaml).

*TODO: explain pipeline choices*

Then we created the pipeline parameters file:

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml create \
	     example/anopheles_X_GeneRax_header.yaml \
	     parameters MACSE GeneRax DeCoSTAR SPPDCJ
        example/anopheles_X_GeneRax.yaml
```

The next step was to initialize the pipeline.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_GeneRax/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt will be computed.
```

Then we ran in sequence the pipeline tools. First MACSE.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm MACSE
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/MACSE/MACSE.sh
Submitted batch job 65060860
	  	    ... wait for the slurm processes to complete ...
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check MACSE
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/MACSE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt
```

This showed that MACSE succeeded to compute an MSA for all gene
families. The next step was GeneRax.

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/GeneRax/GeneRax.sh
Submitted batch job 65065308
	  	    ... wait for the slurm processes to complete ...
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check GeneRax
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/GeneRax.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/reconciliations_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats GeneRax
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_families.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses:transfers
node2:492:41:0:0
AnophelesgambiaePEST:471:6:30:0
AnophelesfunestusFUMOZ:472:2:25:0
node0:495:0:36:0
AnophelesatroparvusEBRO:503:15:43:0
node1:531:39:0:0
```

Again, all expected output files were present and there was no error
in running GeneRax.
  
We can observe that the number of ancestral genes is slightly higher
than the number of extant genes and oe can suspect the well-documented
issue of the reconciliation algorithm having a tendancy to locate
duplications higher in the species tree.
  
Next to illustrate the feature that the AGO pipeline tools can be ran
either through slurm or locally, we ran DeCoSTAR as a bash script,
redirecting the standard output and error output into specific files.

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml bash DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > chmod 755 /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/DeCoSTAR/DeCoSTAR.sh \
	      2> /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.err \
	      1> /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR/DeCoSTAR.log
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/DeCoSTAR/DeCoSTAR.csv; \
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

We can observe that DCoSTAR ran with no problem. But the statistics on
the resulting ancestral adjacencies show that we can expect highly
fragmented ancestral gene orders, as there is a significant level of
conflicting adjacencies and free extremities in the ancestral species.
  
Finally, we cleard the conflict in ancestral adjacencies using spp_dcj.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
Submitted batch job 65067302
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_GeneRax/aux/SPPDCJ/SPPDCJ.sh
Submitted batch job 65069036
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_GeneRax/log/SPPDCJ.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_GeneRax.yaml stats SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_GeneRax/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   231:225.98:224:223.25
node1   405:372.69:357:351.57
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   462:437.18:416:409.72
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
AGO-pipeline > python scripts/gene_orders_utils.py \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/results/DeCoSTAR/genes_reformatted.txt \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/data/adjacencies_ago_X.txt \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/results/SPPDCJ/ \
	      /scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_ago_X.txt
```

One can look at the gene order files (whose paths are given in
`/scratch/chauvec/SPP/anopheles_X_GeneRax/data/gene_orders_ago_X.txt`)
to analyze the resulting gene orders.  The spp_dcj statistics show
that actually very few adjacencies needed to be discarded to clear all
conflicts in ancestral species`node2`, unlike in `node0` and `node1`,
but in both cases the weight of the discarded adjacencies is quite
low.

## ALE-based pipeline

We reuse the alignments obtained with MACSE for the previous experiment.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml create \
	      example/anopheles_X_ALE_header.yaml \
	      parameters IQ-TREE ALE DeCoSTAR SPPDCJ
        example/anopheles_X_ALE.yaml
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_ALE/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt -> /scratch/chauvec/SPP/anopheles_X_ALE/data/alignments_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/reconciliations_X.txt will be computed.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt will be computed.
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm IQ-TREE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/IQ-TREE/IQ-TREE.sh
Submitted batch job 65075228
	  	    ... wait for the slurm processes to complete ...
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check IQ-TREE
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/IQ-TREE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/ALE/ALE.sh
Submitted batch job 65078272
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check ALE
        ERRORS: 64
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/ALE.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/reconciliations_X.txt
```

There were 64 families involving transfers. They will be discarded from further steps.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats ALE
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_species.csv
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_families.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ALE/statistics/ALE/ALE_species.csv
#species:genes:duplications:losses:transfers
node2:388:1:0:0
AnophelesgambiaePEST:394:6:0:0
AnophelesfunestusFUMOZ:390:2:0:0
node0:388:0:0:0
AnophelesatroparvusEBRO:390:2:0:0
node1:388:0:0:0
```

Very few gene duplication/loss events are left in the non-discarded families.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 65079928
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv
AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv; \
	      grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ALE/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:392:0.5        392:391:0:2
AnophelesatroparvusEBRO:390:0.5 390:389:0:2
AnophelesfunestusFUMOZ:390:0.5  390:389:0:2
AnophelesgambiaePEST:394:0.5    394:393:0:2
node0:388:0.5   367:338:0:100
node1:388:0.5   340:267:0:242
node2:388:0.5   235:159:0:458
```

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
Submitted batch job 65081116
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ALE/aux/SPPDCJ/SPPDCJ.sh
Submitted batch job 
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ALE/log/SPPDCJ.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ALE.yaml stats SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ALE/statistics/SPPDCJ/SPPDCJ_species.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ALE/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   159:158.52:159:158.52
node1   267:266.52:267:266.52
AnophelesalbimanusSTECLA        391:391.0:391:391.0
node0   339:337.52:338:337.52
AnophelesatroparvusEBRO 389:389.0:389:389.0
AnophelesgambiaePEST    393:393.0:393:393.0
AnophelesfunestusFUMOZ  389:389.0:389:389.0
AGO-pipeline > python scripts/gene_orders_utils.py \
	      /scratch/chauvec/SPP/anopheles_X_ALE/results/DeCoSTAR/genes_reformatted.txt \
	      /scratch/chauvec/SPP/anopheles_X_ALE/data/adjacencies_ago_X.txt \
	      /scratch/chauvec/SPP/anopheles_X_ALE/results/SPPDCJ/ \
	      /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_orders_ago_X.txt
```

## ecceTERA-based pipeline

We reuse the gene trees obtained with IQ-TREE for the previous experiment.

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml create \
	     example/anopheles_X_ecceTERA_header.yaml parameters DeCoSTAR SPPDCJ
        example/anopheles_X_ecceTERA.yaml
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/sequences_X_4.txt.
        /scratch/chauvec/SPP/anopheles_X_GeneRax/data/alignments_X.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/alignments_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ALE/data/gene_trees_X.txt -> /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_trees_X.txt.
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt will be computed.
```

```
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
(AGO_python3) [chauvec@cedar5.cedar.computecanada.ca] AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/DeCoSTAR/DeCoSTAR.sh
Submitted batch job 65083109
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check DeCoSTAR
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/DeCoSTAR.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
AGO-pipeline > head -1 /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv; \
	      grep -P ':0.5\t' /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/DeCoSTAR/DeCoSTAR.csv | sort
#species:nb_genes_in_adj:min_weight     nb_genes_in_adj:nb_adjacencies:nb_ext_in_conflict:nb_free_ext
AnophelesalbimanusSTECLA:489:0.5        489:488:0:2
AnophelesatroparvusEBRO:503:0.5 503:502:0:2
AnophelesfunestusFUMOZ:472:0.5  472:471:0:2
AnophelesgambiaePEST:471:0.5    471:470:0:2
node0:472:0.5   453:422:5:105
node1:498:0.5   444:356:5:289
node2:483:0.5   329:224:0:518
```

```
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ_ILP
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ_ILP/SPPDCJ_ILP.sh
Submitted batch job 65083739
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ_ILP
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/SPPDCJ_ILP.log
        OUTPUT: No output file is created
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml slurm SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
AGO-pipeline > sbatch /scratch/chauvec/SPP/anopheles_X_ecceTERA/aux/SPPDCJ/SPPDCJ.sh
Submitted batch job 65084100
	  	    ... wait for the slurm processes to complete ...
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml check SPPDCJ
        ERRORS: 0
        LOG:    /scratch/chauvec/SPP/anopheles_X_ecceTERA/log/SPPDCJ.log
        OUTPUT: /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt
AGO-pipeline > python src/AGO.py example/anopheles_X_ecceTERA.yaml stats SPPDCJ
        /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
AGO-pipeline > cat /scratch/chauvec/SPP/anopheles_X_ecceTERA/statistics/SPPDCJ/SPPDCJ_species.csv
#species        number of adjacencies:total weight:kept adjacencies:kept weight
node2   225:222.61:224:222.26
node1   369:356.18:351:347.5
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   424:418.81:418:415.99
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
AGO-pipeline > python scripts/gene_orders_utils.py \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/results/DeCoSTAR/genes_reformatted.txt \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/adjacencies_ago_X.txt \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/results/SPPDCJ/ \
	      /scratch/chauvec/SPP/anopheles_X_ecceTERA/data/gene_orders_ago_X.txt
```
