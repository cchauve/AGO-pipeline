# Anopheles data from VectorBase

The file `proteins_20230728.txt` was downloaded from VectorBase (https://vectorbase.org/vectorbase/app/) on 2023-07-28
using the search strategy `Anopheles_AGO_genes`. For each gene only the longest transcript was kept.

Genes included into another gene are discarded, as are non-coding genes and genes with no sequence available.

Statistics about genes were generated for all species, focusing on genes assigned to chromosomes:
```
python VectorBase_utils.py stats proteins_20230728.txt statistics_1.tsv all '2R 2L 3R 3L X 2 3 2RL 3RL'
AnophelesmaculipalpisidAnoMacuDA375x.nb_kept_genes      4508
AnophelesaquasalisidAnoAquaMGQ19.nb_kept_genes  	10043
AnophelescruziiidAnoCruzASRS3206.nb_kept_genes  	10230
AnophelesmouchetiidAnoMoucSNF2007.nb_kept_genes 	10909
AnophelesalbimanusSTECLA.nb_kept_genes			11587
AnophelesgambiaePEST.nb_kept_genes      		11853
AnophelesfunestusFUMOZ.nb_kept_genes    		11993
AnophelesatroparvusEBRO.nb_kept_genes   		12230
```

```
python VectorBase_utils.py stats proteins_20230728.txt statistics_2.tsv all '2R 2L 3R 3L X'
AnophelesmaculipalpisidAnoMacuDA375x.nb_kept_genes      389
AnophelesaquasalisidAnoAquaMGQ19.nb_kept_genes  	464
AnophelescruziiidAnoCruzASRS3206.nb_kept_genes  	811
AnophelesmouchetiidAnoMoucSNF2007.nb_kept_genes 	961
AnophelesfunestusFUMOZ.nb_kept_genes    		1037
AnophelesalbimanusSTECLA.nb_kept_genes  		11587
AnophelesgambiaePEST.nb_kept_genes      		11853
AnophelesatroparvusEBRO.nb_kept_genes   		12230
```

```
python VectorBase_utils.py stats proteins_20230728.txt statistics_3.tsv all 'X'
AnophelesmaculipalpisidAnoMacuDA375x.nb_kept_genes      389
AnophelesaquasalisidAnoAquaMGQ19.nb_kept_genes  	464
AnophelescruziiidAnoCruzASRS3206.nb_kept_genes  	811
AnophelesmouchetiidAnoMoucSNF2007.nb_kept_genes 	961
AnophelesalbimanusSTECLA.nb_kept_genes  		1006
AnophelesgambiaePEST.nb_kept_genes      		1020
AnophelesfunestusFUMOZ.nb_kept_genes    		1037
AnophelesatroparvusEBRO.nb_kept_genes   		1122
```

The species `STECLA, PEST, EBRO, FUMOZ` are the only ones quite well
assembled, with `FUMOZ` assembly being not well resolved on the
autosomes.

Creating input data for ortholog groups computation.

First all species and no focus on chromosome assignment.
```
python VectorBase_utils.py genomes proteins_20230728.txt all all ALL_1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        	308094
nb_included_genes       21590
nb_noncoding_genes      11230
nb_missing_coding_seq   129
nb_kept_genes   	275145
    23392 sequences_ALL_1/AnophelesalbimanusSTECLA.fasta
    20878 sequences_ALL_1/AnophelesaquasalisidAnoAquaMGQ19.fasta
    25394 sequences_ALL_1/AnophelesarabiensisDongola.fasta
    25854 sequences_ALL_1/AnophelesatroparvusEBRO.fasta
    21162 sequences_ALL_1/AnopheleschristyiACHKN1017.fasta
    23936 sequences_ALL_1/AnophelescoluzziiNgousso.fasta
    22728 sequences_ALL_1/AnophelescruziiidAnoCruzASRS3206.fasta
    27786 sequences_ALL_1/AnophelesculicifaciesA37.fasta
    21014 sequences_ALL_1/AnophelesdarlingiCoari.fasta
    24852 sequences_ALL_1/AnophelesdirusWRAIR2.fasta
    23564 sequences_ALL_1/AnophelesepiroticusEpiroticus2.fasta
    24502 sequences_ALL_1/AnophelesfarautiFAR1.fasta
    23986 sequences_ALL_1/AnophelesfunestusFUMOZ.fasta
    24686 sequences_ALL_1/AnophelesgambiaePEST.fasta
    29530 sequences_ALL_1/Anophelesmaculatusmaculatus3.fasta
     9082 sequences_ALL_1/AnophelesmaculipalpisidAnoMacuDA375x.fasta
    29660 sequences_ALL_1/AnophelesmelasCM1001059A.fasta
    24878 sequences_ALL_1/AnophelesmerusMAF.fasta
    24846 sequences_ALL_1/AnophelesminimusMINIMUS1.fasta
    22096 sequences_ALL_1/AnophelesmouchetiidAnoMoucSNF2007.fasta
    25672 sequences_ALL_1/AnophelesquadriannulatusSANGWE.fasta
    24768 sequences_ALL_1/AnophelessinensisSINENSIS.fasta
    26024 sequences_ALL_1/AnophelesstephensiSDA500.fasta
```

Second all species with a large number of assigned genes.
```
python VectorBase_utils.py genomes proteins_20230728.txt 'AnophelesaquasalisidAnoAquaMGQ19 AnophelescruziiidAnoCruzASRS3206 AnophelesmouchetiidAnoMoucSNF2007 AnophelesalbimanusSTECLA AnophelesgambiaePEST AnophelesfunestusFUMOZ AnophelesatroparvusEBRO' '2R 2L 3R 3L X 2 3 2RL 3RL'  ALL_2 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        	94300
nb_included_genes       6464
nb_noncoding_genes      5902
nb_missing_coding_seq   124
nb_off_target_genes     2965
nb_kept_genes   	78845
   23174 sequences_ALL_2/AnophelesalbimanusSTECLA.fasta
   20086 sequences_ALL_2/AnophelesaquasalisidAnoAquaMGQ19.fasta
   24460 sequences_ALL_2/AnophelesatroparvusEBRO.fasta
   20460 sequences_ALL_2/AnophelescruziiidAnoCruzASRS3206.fasta
   23986 sequences_ALL_2/AnophelesfunestusFUMOZ.fasta
   23706 sequences_ALL_2/AnophelesgambiaePEST.fasta
   21818 sequences_ALL_2/AnophelesmouchetiidAnoMoucSNF2007.fasta
```

Third, only the 4 well assembled species.
```
python VectorBase_utils.py genomes proteins_20230728.txt 'AnophelesalbimanusSTECLA AnophelesgambiaePEST AnophelesfunestusFUMOZ AnophelesatroparvusEBRO' '2R 2L 3R 3L X 2 3 2RL 3RL'  ALL_3 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        	54678
nb_included_genes       3697
nb_noncoding_genes      2021
nb_missing_coding_seq   1
nb_off_target_genes     1296
nb_kept_genes   	47663
   23174 sequences_ALL_3/AnophelesalbimanusSTECLA.fasta
   24460 sequences_ALL_3/AnophelesatroparvusEBRO.fasta
   23986 sequences_ALL_3/AnophelesfunestusFUMOZ.fasta
   23706 sequences_ALL_3/AnophelesgambiaePEST.fasta
```

Last, the 4 well assembled species and the X chromosome.
```
python VectorBase_utils.py genomes proteins_20230728.txt 'AnophelesalbimanusSTECLA AnophelesgambiaePEST AnophelesfunestusFUMOZ AnophelesatroparvusEBRO' 'X'  ALL_4 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        	54678
nb_included_genes       3697
nb_noncoding_genes      2021
nb_missing_coding_seq   1
nb_off_target_genes     44774
nb_kept_genes   	4185
   2012 sequences_ALL_4/AnophelesalbimanusSTECLA.fasta
   2244 sequences_ALL_4/AnophelesatroparvusEBRO.fasta
   2074 sequences_ALL_4/AnophelesfunestusFUMOZ.fasta
   2040 sequences_ALL_4/AnophelesgambiaePEST.fasta
```

Computing families from VectorBase orthogroups.

```
python VectorBase_utils.py OG_noseq proteins_20230728.txt all all OG_1 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        308094
nb_included_genes       21590
nb_noncoding_genes      11230
nb_missing_coding_seq   129
nb_kept_genes   275145
nb_families     24667
```

```
python VectorBase_utils.py OG_noseq proteins_20230728.txt 'AnophelesaquasalisidAnoAquaMGQ19 AnophelescruziiidAnoCruzASRS3206 AnophelesmouchetiidAnoMoucSNF2007 AnophelesalbimanusSTECLA AnophelesgambiaePEST AnophelesfunestusFUMOZ AnophelesatroparvusEBRO' '2R 2L 3R 3L X 2 3 2RL 3RL' OG_2 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        94300
nb_included_genes       6464
nb_noncoding_genes      5902
nb_missing_coding_seq   124
nb_off_target_genes     2965
nb_kept_genes   78845
nb_families     13790
```

```
python VectorBase_utils.py OG_noseq proteins_20230728.txt 'AnophelesalbimanusSTECLA AnophelesgambiaePEST AnophelesfunestusFUMOZ AnophelesatroparvusEBRO' '2R 2L 3R 3L X 2 3 2RL 3RL' OG_3 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        54678
nb_included_genes       3697
nb_noncoding_genes      2021
nb_missing_coding_seq   1
nb_off_target_genes     1296
nb_kept_genes   47663
nb_families     13418
```

```
python VectorBase_utils.py OG_noseq proteins_20230728.txt 'AnophelesalbimanusSTECLA AnophelesgambiaePEST AnophelesfunestusFUMOZ AnophelesatroparvusEBRO' 'X' OG_4 /home/chauvec/projects/ctb-chauvec/AGO-pipeline/data/VectorBase
nb_genes        54678
nb_included_genes       3697
nb_noncoding_genes      2021
nb_missing_coding_seq   1
nb_off_target_genes     44774
nb_kept_genes   4185
nb_families     1533
```