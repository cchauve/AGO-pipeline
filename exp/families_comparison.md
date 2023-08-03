# Gene families for Anopheles data

# Data

Genes data was retrieved from https://vectorbase.org/ for 23 reference species of *Anopheles* mosquito, as described in [VectorBase/README](../data/VectorBase/README.md).

Out of these 23 species, 7 were selected due to having genes assigned to chromosomes, indicating a complete or near-complete assembly.
A genome is fully assembled if most of its genes are assigned to any of the chromosomes `2R,2L,3R,3L,X`.
A genome is nearly completely assembled if most of its genes are assigned to any of the chromosomes `2,3,2RL,3RL,2R,2L,3R,3L,X`.
The 7 species are shown below with the three associated numbers being respectively
(1) number of genes assigned to `2,3,2RL,3RL,2R,2L,3R,3L,X`,
(2) number of genes assigned to `2R,2L,3R,3L,X`,
(4) number of genes associated to `X`.
```
Anopheles aquasalis idAnoAquaMG-Q 19	10043	464	464
Anopheles cruzii idAnoCruzAS RS32 06	10230	811	811
Anopheles moucheti idAnoMoucSN F20 07	10909	861	961
Anopheles albimanus STECLA   		11587	1037	1006
Anopheles gambiae PEST			11853	11587	1020
Anopheles funestus FUMOZ		11993	11853	1037
Anopheles atroparvus EBRO		12230	12230	1122
```
The three species `PEST,FUMOZ,EBRO` are fully assembled, the four other species are nearly assembled;
the four species `PEST,FUMOZ,EBRO,STECLA` seem to have a fully assembled `X` chromosome and these are
the species already considered in the AGO paper.
More details on these species are available at:
- https://vectorbase.org/vectorbase/app/record/dataset/TMPTX_aaquidAnoAquaMGQ_19
- https://vectorbase.org/vectorbase/app/record/dataset/TMPTX_acruidAnoCruzAS_RS32_06
- https://vectorbase.org/vectorbase/app/record/dataset/TMPTX_amouidAnoMoucSN_F20_07
- https://vectorbase.org/vectorbase/app/record/dataset/TMPTX_aalbSTECLA
- https://vectorbase.org/vectorbase/app/record/dataset/NCBITAXON_180454
- https://vectorbase.org/vectorbase/app/record/dataset/TMPTX_afunFUMOZ
- https://vectorbase.org/vectorbase/app/record/dataset/TMPTX_aatrEBRO

**Remark.** There was no preliminary analysis of the retrieved protein sequences in terms of structure (stop codons).

From of these data, three datasets were considered:
- **Dataset 2**: 7 species and all genes assigned to chromosomes;
- **Dataset 3**: species `PEST,FUMOZ,EBRO,STECLA` and all genes assigned to chromosomes;
- **Dataset 4**: species `PEST,FUMOZ,EBRO,STECLA` and all genes assigned to the `X` chromosome.  

Dataset 1 is composed of the 23 species and all genes, but was not analyzed.

# Methods

For each dataset, three different sets of gene families were obtained:
- **VectorBase.OG**: gene families defined by the OrthoMCL orthogroups pre-computed on VectorBase. These orthogroups were computed using the dataset of all vector genomes on VectorBase, thus encompassing the full taxonomic spectrum of *Arthroproda*, which is much larger than the *Anopheles* taxonomic range.
- **OMA.OG**: orthogroups computed using OMA standalone (https://omabrowser.org/standalone/) with default parameters. The OMA orthogroups are expected to contain at most one gene per species, so are not duplication-aware.
- **OMA.HOG**. hierarchical groups (HOG) computed using OMA standalone, that include paralogous genes.
- **PO**: orthogroups computed using proteinortho (https://gitlab.com/paulklemm_PHD/proteinortho) with default parameters (so no synteny).

The OMA.OG/OMA.HOG/PO/VectorBase.OG results for the three considered datasets are available at:
- `OMA_20230728/exp_[2,3,4]/families_[OG,HOG].txt` (reformatted families);
- `proteinortho_20230728/exp_[2,3,4]/families.txt` (reformatted families);
- `[OMA_20230728,proteinortho_20230728]/exp_[2,3,4]/results/` (original results, in original format);
- `../data/VectorBase/families_OG_[2,3,4].txt`.


The purpose of the analysis is to assess how consistent the obtained gene families are both between methods, and for a given method, between datasets.

To assess the between-methods consistency, I compared
- for each of the three datasets the results of every pair of gene families computation methods;
- for methods OMA and PO, the results on the pairs of data sets (2,3) and (3,4), that represents respectively a species refinement and a location refinement.

For the second part, as the first gene families set is larger than the second, it was filtered to keep only the genes present in the second dataset, discarding families that become empty after this filtering. This ensures that in all cases the compared gene families sets are roughly o the same gene set (not exactly as each method has some internal filterings that discards a few genes).

For each pair of gene families datasets as defined above, I recorded simple statistics.  


The first two ones are the distributions of the size of the gene families for each gene families set, formatted as
`<family size>:<nb of families>`.


The second one is defined as follows:
- a bipartite graph was built with nodes being respectively the gene families of each families set and edge was created between two nodes if they share a common gene;
- the connected components of this graph were classified as:
  - `o2o` (one-to-one): component with one node of each part;
  - `z2o` (zero-to-one): isolated node from the second gene families set;
  - `o2z` (one-to-zero): isolated node from the first gene families set;  
  - `m2o` (many-to-one): several nodes from the first gene families set and one node from the second gene families set;
  - `o2m` (one-to-many): one node from the first gene families set and several nodes from the second gene families set;
  - `m2m` (many-to-many): several nodes from the first gene families set and several nodes from the second gene families set;  

The larger the class of `o2o` components is, the more the two gene families sets do agree.  
Components of types `z2o` and `o2z` correspond to genes that are present in only one gene families set.  
Components of type `o2m` correspond to families of the first set that are **split** into several families in the second.  
Conversely, components of type `m2o` correspond to families of the first set that are **fusions** of several families in the second.  
Last components of type `m2m` correspond to **scrambled** families, i.e. sets of more than one family in both sets that share (transitively) common genes.  

For each type of component, the results shown below are formatted as
`<type>:<nb of components>:<nb genes in first set>:<nb genes in second set>`.

# Results

## 7 species, all chromosomes
### OMA.OG versus PO
```
Size distribution 1:	2:1920 3:1042 4:865 5:1374 6:3008 7:4770
Size distribution 2:	2:1094 3:588 4:509 5:932 6:2513 7:5304 8:432 9:106 10:55 11:60 12:61 13:20 14:13 15:7 16:5 17:4 18:1 19:3 21:1 22:1 25:1 29:1 33:1 42:1
Component types:	o2o:10179:59249:60787 z2o:210:0:450 o2z:326:720:0 o2m:62:339:350 m2o:837:6525:6651 m2m:143:1901:1910
```
### OMA.OG versus VectoBase.OG
```
Size distribution 1:	2:1920 3:1042 4:865 5:1374 6:3008 7:4770
Size distribution 2:	1:3506 2:546 3:396 4:405 5:648 6:1848 7:4276 8:907 9:279 10:145 11:88 12:77 13:133 14:133 15:65 16:38 17:32 18:15 19:21 20:29 21:19 22:26 23:17 24:9 25:13 26:8 27:5 28:8 29:6 30:4 31:11 32:2 33:3 34:6 35:5 36:5 37:5 38:5 39:1 40:2 41:5 42:5 44:3 45:3 46:1 48:2 49:3 50:1 51:1 54:1 55:1 57:1 59:2 64:1 66:1 68:1 72:1 77:1 86:1 97:2 103:1 107:1 117:1 119:1 162:1 191:1
Component types:	o2o:7844:47183:50283 z2o:3421:0:3837 o2z:0:0:0 o2m:178:813:942 m2o:1258:14467:16294 m2m:344:6271:7489
```
### OMA.HOG versus PO
```
Size distribution 1:	2:1389 3:759 4:743 5:1213 6:2722 7:4829 8:454 9:55 10:38 11:20 12:19 13:16 14:9 15:10 16:5 17:2 18:3 19:1 20:3 21:1 22:4 23:1 24:4 25:1 30:1 33:1 34:2 35:1 36:1 46:1 50:1 52:2
Size distribution 2:	2:1094 3:588 4:509 5:932 6:2513 7:5304 8:432 9:106 10:55 11:60 12:61 13:20 14:13 15:7 16:5 17:4 18:1 19:3 21:1 22:1 25:1 29:1 33:1 42:1
Component types:	o2o:10267:61899:62036 z2o:199:0:432 o2z:243:622:0 o2m:115:1017:896 m2o:548:4392:4346 m2m:151:2638:2438
```
### OMA.HOG versus VectoBase.OG
```
Size distribution 1:	2:1389 3:759 4:743 5:1213 6:2722 7:4829 8:454 9:55 10:38 11:20 12:19 13:16 14:9 15:10 16:5 17:2 18:3 19:1 20:3 21:1 22:4 23:1 24:4 25:1 30:1 33:1 34:2 35:1 36:1 46:1 50:1 52:2
Size distribution 2:	1:3506 2:546 3:396 4:405 5:648 6:1848 7:4276 8:907 9:279 10:145 11:88 12:77 13:133 14:133 15:65 16:38 17:32 18:15 19:21 20:29 21:19 22:26 23:17 24:9 25:13 26:8 27:5 28:8 29:6 30:4 31:11 32:2 33:3 34:6 35:5 36:5 37:5 38:5 39:1 40:2 41:5 42:5 44:3 45:3 46:1 48:2 49:3 50:1 51:1 54:1 55:1 57:1 59:2 64:1 66:1 68:1 72:1 77:1 86:1 97:2 103:1 107:1 117:1 119:1 162:1 191:1
Component types:	o2o:7894:48987:51190 z2o:3387:0:3798 o2z:0:0:0 o2m:194:991:1117 m2o:1047:12947:14090 m2m:371:7643:8650
```
### PO versus VectoBase.OG
```
Size distribution 1:	2:1094 3:588 4:509 5:932 6:2513 7:5304 8:432 9:106 10:55 11:60 12:61 13:20 14:13 15:7 16:5 17:4 18:1 19:3 21:1 22:1 25:1 29:1 33:1 42:1
Size distribution 2:	1:3506 2:546 3:396 4:405 5:648 6:1848 7:4276 8:907 9:279 10:145 11:88 12:77 13:133 14:133 15:65 16:38 17:32 18:15 19:21 20:29 21:19 22:26 23:17 24:9 25:13 26:8 27:5 28:8 29:6 30:4 31:11 32:2 33:3 34:6 35:5 36:5 37:5 38:5 39:1 40:2 41:5 42:5 44:3 45:3 46:1 48:2 49:3 50:1 51:1 54:1 55:1 57:1 59:2 64:1 66:1 68:1 72:1 77:1 86:1 97:2 103:1 107:1 117:1 119:1 162:1 191:1
Component types:	o2o:7859:49365:51447 z2o:3509:0:3989 o2z:0:0:0 o2m:242:1490:1711 m2o:824:11014:12098 m2m:437:8279:9600
```

## 4 species, all chromosomes
### OMA.OG versus PO
```
Size distribution 1:	2:2386 3:3255 4:5941
Size distribution 2:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Component types:	o2o:9790:34126:35504 z2o:223:0:476 o2z:855:1860:0 o2m:11:34:49 m2o:348:1834:1726 m2m:52:447:450
```
### OMA.OG versus VectoBase.OG
```
Size distribution 1:	2:2386 3:3255 4:5941
Size distribution 2:	1:3504 2:856 3:1766 4:5153 5:956 6:335 7:202 8:215 9:106 10:51 11:44 12:48 13:24 14:29 15:14 16:12 17:8 18:9 19:10 20:7 21:7 22:10 23:8 24:4 25:3 26:4 27:2 28:1 29:2 30:2 31:2 32:3 33:2 34:1 35:1 37:1 38:4 43:1 44:1 56:1 60:2 61:1 63:1 73:1 75:1 83:1 84:1 131:1
Component types:	o2o:8095:28113:31181 z2o:3557:0:4079 o2z:0:0:0 o2m:163:481:590 m2o:946:7300:8716 m2m:214:2407:3097
```
### OMA.HOG versus PO
```
Size distribution 1:	2:1934 3:2830 4:5854 5:493 6:61 7:23 8:12 9:11 10:7 11:6 12:1 13:5 14:2 15:3 16:2 17:2 20:1 25:1 26:1 30:2 31:1 32:2 33:1
Size distribution 2:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Component types:	o2o:9823:35555:35845 z2o:217:0:461 o2z:744:1810:0 o2m:34:302:243 m2o:229:1185:1083 m2m:64:720:573
```
### OMA.HOG versus VectoBase.OG
```
Size distribution 1:	2:1934 3:2830 4:5854 5:493 6:61 7:23 8:12 9:11 10:7 11:6 12:1 13:5 14:2 15:3 16:2 17:2 20:1 25:1 26:1 30:2 31:1 32:2 33:1
Size distribution 2:	1:3504 2:856 3:1766 4:5153 5:956 6:335 7:202 8:215 9:106 10:51 11:44 12:48 13:24 14:29 15:14 16:12 17:8 18:9 19:10 20:7 21:7 22:10 23:8 24:4 25:3 26:4 27:2 28:1 29:2 30:2 31:2 32:3 33:2 34:1 35:1 37:1 38:4 43:1 44:1 56:1 60:2 61:1 63:1 73:1 75:1 83:1 84:1 131:1
Component types:	o2o:8093:29101:31464 z2o:3521:0:4035 o2z:0:0:0 o2m:178:617:732 m2o:848:6889:7871 m2m:235:2965:3561
```
### PO versus VectoBase.OG
```
Size distribution 1:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Size distribution 2:	1:3504 2:856 3:1766 4:5153 5:956 6:335 7:202 8:215 9:106 10:51 11:44 12:48 13:24 14:29 15:14 16:12 17:8 18:9 19:10 20:7 21:7 22:10 23:8 24:4 25:3 26:4 27:2 28:1 29:2 30:2 31:2 32:3 33:2 34:1 35:1 37:1 38:4 43:1 44:1 56:1 60:2 61:1 63:1 73:1 75:1 83:1 84:1 131:1
Component types:	o2o:7753:28651:30829 z2o:3999:0:5277 o2z:0:0:0 o2m:168:588:739 m2o:697:5986:6932 m2m:280:2980:3886
```

## 4 species, X chromosome
### OMA.OG versus PO
```
Size distribution 1:	2:238 3:317 4:440
Size distribution 2:	2:202 3:268 4:491 5:6 6:2
Component types:	o2o:917:3021:3072 z2o:27:0:57 o2z:35:74:0 o2m:3:9:12 m2o:19:83:73 m2m:0:0:0
```
### OMA.OG versus VectoBase.OG
```
Size distribution 1:	2:238 3:317 4:440
Size distribution 2:	1:564 2:131 3:225 4:512 5:49 6:26 7:6 8:12 9:1 10:2 11:1 13:3 18:1
Component types:	o2o:845:2789:3064 z2o:589:0:673 o2z:0:0:0 o2m:17:47:55 m2o:49:299:337 m2m:8:52:56
```
### OMA.HOG versus PO
```
Size distribution 1:	2:224 3:293 4:467 5:5 11:1
Size distribution 2:	2:202 3:268 4:491 5:6 6:2
Component types:	o2o:920:3080:3082 z2o:27:0:57 o2z:34:74:0 o2m:3:9:12 m2o:16:68:63 m2m:0:0:0
```
### OMA.HOG versus VectoBase.OG
```
Size distribution 1:	2:224 3:293 4:467 5:5 11:1
Size distribution 2:	1:564 2:131 3:225 4:512 5:49 6:26 7:6 8:12 9:1 10:2 11:1 13:3 18:1
Component types:	o2o:844:2829:3068 z2o:586:0:670 o2z:0:0:0 o2m:18:55:63 m2o:47:287:320 m2m:9:60:64
```
### PO versus VectoBase.OG
```
Size distribution 1:	2:202 3:268 4:491 5:6 6:2
Size distribution 2:	1:564 2:131 3:225 4:512 5:49 6:26 7:6 8:12 9:1 10:2 11:1 13:3 18:1
Component types:	o2o:826:2795:3018 z2o:605:0:709 o2z:0:0:0 o2m:13:40:46 m2o:42:264:292 m2m:16:115:120
```

## OMA.OG only
### 7 species, all chromosomes versus 4 species, all chromosomes
```
Size distribution 1:	1:361 2:2389 3:3260 4:5741
Size distribution 2:	2:2386 3:3255 4:5941
Component types:	o2o:11202:36904:37286 z2o:0:0:0 o2z:0:0:0 o2m:14:40:57 m2o:168:483:487 m2m:75:456:471
```
### 4 species, all chromosomes versus 4 species, X chromosomes
```
Size distribution 1:	1:17 2:243 3:313 4:434
Size distribution 2:	2:238 3:317 4:440
Component types:	o2o:983:3144:3153 z2o:0:0:0 o2z:0:0:0 o2m:0:0:0 m2o:12:34:34 m2m:0:0:0
```

## OMA.HOG only
### 7 species, all chromosomes versus 4 species, all chromosomes
```
Size distribution 1:	1:210 2:1806 3:2875 4:5823 5:474 6:66 7:23 8:14 9:9 10:6 11:9 12:4 13:5 14:2 15:3 16:3 17:1 20:1 22:1 25:1 26:1 30:1 32:1 33:1
Size distribution 2:	2:1934 3:2830 4:5854 5:493 6:61 7:23 8:12 9:11 10:7 11:6 12:1 13:5 14:2 15:3 16:2 17:2 20:1 25:1 26:1 30:2 31:1 32:2 33:1
Component types:	o2o:10918:38239:38315 z2o:0:0:0 o2z:0:0:0 o2m:56:278:292 m2o:117:520:532 m2m:45:420:433
```
### 4 species, all chromosomes versus 4 species, X chromosomes
```
Size distribution 1:	1:10 2:224 3:291 4:465 5:5 11:1
Size distribution 2:	2:224 3:293 4:467 5:5 11:1
Component types:	o2o:982:3207:3209 z2o:0:0:0 o2z:0:0:0 o2m:0:0:0 m2o:6:16:16 m2m:1:4:6
```

## PO only
### 7 species, all chromosomes versus 4 species, all chromosomes
```
Size distribution 1:	1:83 2:1047 3:2402 4:6215 5:459 6:99 7:76 8:24 9:13 10:2 11:2 12:2 13:3 23:1
Size distribution 2:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Component types:	o2o:10070:36572:36622 z2o:20:0:40 o2z:0:0:0 o2m:125:842:854 m2o:62:308:308 m2m:43:379:381
```
### 4 species, all chromosomes versus 4 species, X chromosomes
```
Size distribution 1:	1:19 2:129 3:257 4:481 5:6 6:1
Size distribution 2:	2:202 3:268 4:491 5:6 6:2
Component types:	o2o:879:2978:3026 z2o:76:0:155 o2z:0:0:0 o2m:4:13:16 m2o:4:11:11 m2m:1:6:6
```

## Summary

### Comparison between methods.

The `VectorBase.OG` families with many families of size 1, together
with a few families of larger size than in the other methods, likely
caused by a single-linkage clustering due to the fact that the
families are computed for a much larger set of spcies (all vector
species in VectorBase).

Moreover, the agreement in terms of one-to-one (`o2o`) families with
the other methods is significantly lower, and we observe a large
number of families in the classes many-to-one (i.e. larger families in
`VectorBase.OG`) or many-to-many (`m2o,m2m`).

The comparison between `OMA` and proteinortho (`PO`) shows a much
larger agreement. The main differences are in families belonging to
the `m2o` class, suggesting that generally `PO` families are refined
`OMA` families. For the `X` chromosome dataset, the agreement is
almost perfect.

### Comparison between datasets, per method.

Generally both `OMA` and `PO` are quite internally consistent, with
`OMA.HOG` being the most consistent method. The `PO` families are
slightly less consistent. The differences are unsignificant for the
`X` chromosome dataset.

## Conclusion

The choice of method is between `OMA.HOG` and `PO`, and either, or the
subset of `o2o` families, would be a good choice.