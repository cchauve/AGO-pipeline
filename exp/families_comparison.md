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
Anopheles aquasalisid AnoAqua MGQ19	10043	464	464
Anopheles cruziiidAno Cruz ASRS3206	10230	811	811
Anopheles mouchetiid AnoMouc SNF2007	10909	861	961
Anopheles albimanus STECLA   		11587	1037	1006
Anopheles gambiae PEST			11853	11587	1020
Anopheles funestus FUMOZ		11993	11853	1037
Anopheles atroparvus EBRO		12230	12230	1122
```
The three species `PEST,FUMOZ,EBRO` are fully assembled, the four other species are nearly assembled;
the four species `PEST,FUMOZ,EBRO,STECLA` seem to have a fully assembled `X` chromosome and these are
the species already considered in the AGO paper.

**Remark.** There was no preliminary analysis of the retrieved protein sequences in terms of structure (stop codons).

From of these data, three datasets were considered:
- **Dataset 2**: 7 species and all genes assigned to chromosomes;
- **Dataset 3**: species `PEST,FUMOZ,EBRO,STECLA` and all genes assigned to chromosomes;
- **Dataset 4**: species `PEST,FUMOZ,EBRO,STECLA` and all genes assigned to the `X` chromosome.  

Dataset 1 is composed of the 23 species and all genes, but was not analyzed.

# Methods

For each dataset, three different sets of gene families were obtained:
- **VectorBase.OG**: gene families defined by the OrthoMCL orthogroups pre-computed on VectorBase. These orthogroups were computed using the dataset of all vector genomes on VectorBase, thus encompassing the full taxonomic spectrum of *Arthroproda*, which is much larger than the *Anopheles* taxonomic range.
- **OMA**: orthogroups computed using OMA standalone (https://omabrowser.org/standalone/) with default parameters. The OMA orthogroups are expected to contain at most one gene per species, so are not duplication-aware. The hierarchical groups (HOG) contain paralogous genes, although I do not know if this includes ancient duplications; moreover their computation does require a species tree, that was not known for Dataset 2, so the HOG are not considered for now (they should be used instead of ortholog groups).
- **PO**: orthogroups computed using proteinortho (https://gitlab.com/paulklemm_PHD/proteinortho) with default parameters (so no synteny).

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
  - 'z2o` (zero-to-one): isolated node from the second gene families set;
  - 'o2z` (one-to-zero): isolated node from the first gene families set;  
  - 'm2o` (many-to-one): several nodes from the first gene families set and one node from the second gene families set;
  - 'o2m` (one-to-many): one node from the first gene families set and several nodes from the second gene families set;
  - 'm2m` (many-to-many): several nodes from the first gene families set and several nodes from the second gene families set;  

The larger the class of `o2o` components is, the more the two gene families sets do agree.
Components of types `z2o` and `o2z` correspond to genes that are present in only one gene families set.
Components of type `o2m` correspond to families of the first set that are **split** into several families in the second.
Conversely, components of type `m2o` correspond to families of the first set that are **fusions** of several families in the second.
Last components of type `m2m` correspond to **scrambled** families, i.e. sets of more than one family in both sets that share (transitively) common genes.

For each type of component, the results shown below are formatted as
`<type>:<nb families in first set>:<nb families in econd set>:<nb genes in first set>:<nb genes in second set>`.

# Results

## 7 species, all chromosomes (Dataset 2)

### OMA versus PO
```
Size distribution 1:	2:1920 3:1042 4:865 5:1374 6:3008 7:4770
Size distribution 2:	2:1094 3:588 4:509 5:932 6:2513 7:5304 8:432 9:106 10:55 11:60 12:61 13:20 14:13 15:7 16:5 17:4 18:1 19:3 21:1 22:1 25:1 29:1 33:1 42:1
Component types:	o2o:10180:59255:60792 z2o:210:0:450 o2z:326:720:0 o2m:62:339:350 m2o:837:6525:6651 m2m:143:1895:1905
```

### OMA versus VectoBase.OG
```
Size distribution 1:	2:1920 3:1042 4:865 5:1374 6:3008 7:4770
Size distribution 2:	1:3506 2:546 3:396 4:405 5:648 6:1848 7:4276 8:907 9:279 10:145 11:88 12:77 13:133 14:133 15:65 16:38 17:32 18:15 19:21 20:29 21:19 22:26 23:17 24:9 25:13 26:8 27:5 28:8 29:6 30:4 31:11 32:2 33:3 34:6 35:5 36:5 37:5 38:5 39:1 40:2 41:5 42:5 44:3 45:3 46:1 48:2 49:3 50:1 51:1 54:1 55:1 57:1 59:2 64:1 66:1 68:1 72:1 77:1 86:1 97:2 103:1 107:1 117:1 119:1 162:1 191:1
Component types:	o2o:7844:47183:50283 z2o:3421:0:3837 o2z:0:0:0 o2m:178:813:942 m2o:1258:14467:16294 m2m:344:6271:7489
```

### PO versus VectoBase.OG
```
Size distribution 1:	2:1094 3:588 4:509 5:932 6:2513 7:5304 8:432 9:106 10:55 11:60 12:61 13:20 14:13 15:7 16:5 17:4 18:1 19:3 21:1 22:1 25:1 29:1 33:1 42:1
Size distribution 2:	1:3506 2:546 3:396 4:405 5:648 6:1848 7:4276 8:907 9:279 10:145 11:88 12:77 13:133 14:133 15:65 16:38 17:32 18:15 19:21 20:29 21:19 22:26 23:17 24:9 25:13 26:8 27:5 28:8 29:6 30:4 31:11 32:2 33:3 34:6 35:5 36:5 37:5 38:5 39:1 40:2 41:5 42:5 44:3 45:3 46:1 48:2 49:3 50:1 51:1 54:1 55:1 57:1 59:2 64:1 66:1 68:1 72:1 77:1 86:1 97:2 103:1 107:1 117:1 119:1 162:1 191:1
Component types:	o2o:7859:49365:51447 z2o:3509:0:3989 o2z:0:0:0 o2m:242:1490:1711 m2o:824:11014:12098 m2m:437:8279:9600
```

## 4 species, all chromosomes (Dataset 3)

### OMA versus PO
```
Size distribution 1:	2:2386 3:3255 4:5941
Size distribution 2:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Component types:	o2o:9790:34126:35504 z2o:223:0:476 o2z:855:1860:0 o2m:11:34:49 m2o:348:1834:1726 m2m:52:447:450
```
### OMA versus VectoBase.OG
```
Size distribution 1:	2:2386 3:3255 4:5941
Size distribution 2:	1:3504 2:856 3:1766 4:5153 5:956 6:335 7:202 8:215 9:106 10:51 11:44 12:48 13:24 14:29 15:14 16:12 17:8 18:9 19:10 20:7 21:7 22:10 23:8 24:4 25:3 26:4 27:2 28:1 29:2 30:2 31:2 32:3 33:2 34:1 35:1 37:1 38:4 43:1 44:1 56:1 60:2 61:1 63:1 73:1 75:1 83:1 84:1 131:1
Component types:	o2o:8095:28113:31181 z2o:3557:0:4079 o2z:0:0:0 o2m:163:481:590 m2o:946:7300:8716 m2m:214:2407:3097
```

### PO versus VectoBase.OG
```
Size distribution 1:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Size distribution 2:	1:3504 2:856 3:1766 4:5153 5:956 6:335 7:202 8:215 9:106 10:51 11:44 12:48 13:24 14:29 15:14 16:12 17:8 18:9 19:10 20:7 21:7 22:10 23:8 24:4 25:3 26:4 27:2 28:1 29:2 30:2 31:2 32:3 33:2 34:1 35:1 37:1 38:4 43:1 44:1 56:1 60:2 61:1 63:1 73:1 75:1 83:1 84:1 131:1
Component types:	o2o:7753:28651:30829 z2o:3999:0:5277 o2z:0:0:0 o2m:168:588:739 m2o:697:5986:6932 m2m:280:2980:3886
```

## 4 species, X chromosome (Dataset 4)

### OMA versus PO
```
Size distribution 1:	2:238 3:317 4:440
Size distribution 2:	2:202 3:268 4:491 5:6 6:2
Component types:	o2o:917:3021:3072 z2o:27:0:57 o2z:35:74:0 o2m:3:9:12 m2o:19:83:73 m2m:0:0:0
```

### OMA versus VectoBase.OG
```
Size distribution 1:	2:238 3:317 4:440
Size distribution 2:	1:564 2:131 3:225 4:512 5:49 6:26 7:6 8:12 9:1 10:2 11:1 13:3 18:1
Component types:	o2o:845:2789:3064 z2o:589:0:673 o2z:0:0:0 o2m:17:47:55 m2o:49:299:337 m2m:8:52:56
```

### PO versus VectoBase.OG
```
Size distribution 1:	2:202 3:268 4:491 5:6 6:2
Size distribution 2:	1:564 2:131 3:225 4:512 5:49 6:26 7:6 8:12 9:1 10:2 11:1 13:3 18:1
Component types:	o2o:826:2795:3018 z2o:605:0:709 o2z:0:0:0 o2m:13:40:46 m2o:42:264:292 m2m:16:115:120
```

## OMA only

### 7 species, all chromosomes versus 4 species, all chromosomes (Dataset 2, Dataset 3)
```
Size distribution 1:	1:361 2:2388 3:3261 4:5741
Size distribution 2:	2:2386 3:3255 4:5941
Component types:	o2o:11204:36910:37292 z2o:0:0:0 o2z:0:0:0 o2m:14:40:57 m2o:168:483:487 m2m:75:451:465
```

### 4 species, all chromosomes versus 4 species, X chromosomes (Dataset 3, Dataset 4)
```
Size distribution 1:	1:17 2:243 3:313 4:434
Size distribution 2:	2:238 3:317 4:440
Component types:	o2o:983:3144:3153 z2o:0:0:0 o2z:0:0:0 o2m:0:0:0 m2o:12:34:34 m2m:0:0:0
```

## PO only

### 7 species, all chromosomes versus 4 species, all chromosomes (Dataset 2, Dataset 3)
```
Size distribution 1:	1:83 2:1047 3:2402 4:6215 5:459 6:99 7:76 8:24 9:13 10:2 11:2 12:2 13:3 23:1
Size distribution 2:	2:1115 3:2446 4:6318 5:471 6:97 7:27 8:12 9:6 10:2 11:2 12:2 23:1
Component types:	o2o:10070:36572:36622 z2o:20:0:40 o2z:0:0:0 o2m:125:842:854 m2o:62:308:308 m2m:43:379:381
```

### 4 species, all chromosomes versus 4 species, X chromosomes (Dataset 3, Dataset 4)
```
Size distribution 1:	1:19 2:129 3:257 4:481 5:6 6:1
Size distribution 2:	2:202 3:268 4:491 5:6 6:2
Component types:	o2o:879:2978:3026 z2o:76:0:155 o2z:0:0:0 o2m:4:13:16 m2o:4:11:11 m2m:1:6:6
```
