Anopheles data, for the 4 assembled species and the X chromosome.

```
> date
Wed Apr  5 13:32:45 PDT 2023
```

The parameters file is `parameters/Anopheles_GeneRax_NT.yaml`.
The output root directory is `/scratch/chauvec/SPP`.

```
> source AGO_python3/bin/activate
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml init
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_tree_4.newick -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/species_tree_4.newick.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/species_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/species_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/families_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/sequences_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/sequences_X_4.txt.
        /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase/gene_orders_X_4.txt -> /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/gene_orders_X_4.txt.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/alignments_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt will be computed.
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies_X_4.txt will be computed.
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/families_X_4.txt
```

### MACSE

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/MACSE/MACSE.sh
sbatch: NOTE: Your memory request of 8192M was likely submitted as 8G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64349391
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check MACSE
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/alignments_X_4.txt
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/MACSE.log
0
```

### GeneRax

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/GeneRax/GeneRax.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64358662
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt
> grep -c "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/GeneRax.log
0
> wc -l /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt
451 /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/reconciliations_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats GeneRax
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_species.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_families.csv
> m /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/GeneRax/GeneRax_species.csv
#species:genes:duplications:losses
node2:492:41:0
AnophelesgambiaePEST:471:6:30
AnophelesfunestusFUMOZ:472:2:25
node0:495:0:34
AnophelesatroparvusEBRO:503:16:42
node1:529:37:0
AnophelesalbimanusSTECLA:489:8:11
```

### DeCoSTAR

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/DeCoSTAR/DeCoSTAR.sh
sbatch: NOTE: Your memory request of 4096M was likely submitted as 4G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64273185
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/DeCoSTAR.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies_X_4.txt
> grep "ERROR" /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/DeCoSTAR.log
0
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats DeCoSTAR
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/DeCoSTAR/DeCoSTAR.csv
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/DeCoSTAR/DeCoSTAR_0.5_conflicts.txt
> grep node /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/DeCoSTAR/DeCoSTAR.csv
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

### SPPDCJ

```
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_all.sh
> sbatch  /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ_ILP/SPPDCJ_ILP_all.sh
sbatch: NOTE: Your memory request of 262144M was likely submitted as 256G. Please note that Slurm interprets memory requests denominated in G as multiples of 1024M, not 1000M.
Submitted batch job 64363355
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP_all.log
        No output file is created
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP_all.log
#status tool    index   message
SUCCESS SPPDCJ_ILP              /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/SPPDCJ_ILP/all_0.5_0.5_0.25.idmap
SUCCESS SPPDCJ_ILP              /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/SPPDCJ_ILP/all_0.5_0.5_0.25.ilp
> grep telomere /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_ILP/SPPDCJ_ILP_all.err
INFO    2023-04-05 13:54:33,494 identified 214 candidate telomeres in genome node2
INFO    2023-04-05 13:54:33,495 identified 210 candidate telomeres in genome node1
INFO    2023-04-05 13:54:33,496 identified 2 candidate telomeres in genome AnophelesalbimanusSTECLA
INFO    2023-04-05 13:54:33,496 identified 116 candidate telomeres in genome node0
INFO    2023-04-05 13:54:33,496 identified 2 candidate telomeres in genome AnophelesatroparvusEBRO
INFO    2023-04-05 13:54:33,497 identified 2 candidate telomeres in genome AnophelesgambiaePEST
INFO    2023-04-05 13:54:33,497 identified 2 candidate telomeres in genome AnophelesfunestusFUMOZ
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats SPPDCJ_ILP
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/SPPDCJ_ILP/components_all.log
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml script SPPDCJ
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ/SPPDCJ_all.sh
> sbatch /scratch/chauvec/SPP/Anopheles_GeneRax_NT/aux/SPPDCJ/SPPDCJ_all.sh
Submitted batch job 64365862
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml check SPPDCJ
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/log/SPPDCJ_all.log
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies_ago_X_4.txt
> python src/AGO.py parameters/Anopheles_GeneRax_NT.yaml stats SPPDCJ
        /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/SPPDCJ/SPPDCJ_species.csv
> cat /scratch/chauvec/SPP/Anopheles_GeneRax_NT/statistics/SPPDCJ/SPPDCJ_species.csv
#species        <number of adjacencies>:<total weight>:<kept adjacencies>:<kept weight>
node2   231:225.73899999999998:224:223.24099999999999
node1   404:372.4:357:350.543
AnophelesalbimanusSTECLA        488:488.0:488:488.0
node0   460:436.963:416:409.47600000000006
AnophelesatroparvusEBRO 502:502.0:502:502.0
AnophelesgambiaePEST    470:470.0:470:470.0
AnophelesfunestusFUMOZ  471:471.0:471:471.0
```

Creating FASTA format gene orders files.

```
python scripts/gene_orders_utils.py \
       /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/DeCoSTAR/genes_reformatted.txt \
       /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/adjacencies_ago_X_4.txt \
       /scratch/chauvec/SPP/Anopheles_GeneRax_NT/results/SPPDCJ/ \
       /scratch/chauvec/SPP/Anopheles_GeneRax_NT/data/gene_orders_ago_X_4.txt
```
