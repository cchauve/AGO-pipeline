# Anopheles data from VectorBase

The file 'genes_20230311.txt' was downloaded from VectorBase (https://vectorbase.org/vectorbase/app/) on 2023-03-11

Genes assigned to no orthology group (NA) or to no chrn=omosme (UNKN) or to the Y chromosome (Y_unplaced) are discarded.
Genes included into another gene are discarded.

```
cd /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase
gunzip genes_20230311.txt.gz
./get_statistics.sh
```

```
Target ['X'] Min size 3 Min size on target 2
Filter          ambiguous:711   included:5716
All             15857
Small1          5837
Absent          11
Off target      9091
Ambiguous       288
Small2          24
On target       606     606
```

```
python ../../scripts/VectorBase_utils.py build genes_20230311.txt X 2 3 /home/chauvec/projects/ctb-chauvec/SPP-PIPELINE/data/VectorBase
```

```
Target ['2', '2L', '2R'] Min size 3 Min size on target 2
Filter          ambiguous:711   included:5716
All             15857
Small1          5837
Absent          11
Off target      2743
Ambiguous       6778
Small2          109
On target       379     379
```

```
Target ['3', '3L', '3R'] Min size 3 Min size on target 2
Filter          ambiguous:711   included:5716
All             15857
Small1          5837
Absent          11
Off target      1711
Ambiguous       6761
Small2          115
On target       1422    1422
```

```
Target ['2', '3', '2L', '2R', '3L', '3R'] Min size 3 Min size on target 2
Filter          ambiguous:711   included:5716
All             15857
Small1          5837
Absent          11
Off target      867
Ambiguous       559
Small2          238
On target       8345    8345

Target ['2', '3', '2L', '2R', '3L', '3R'] Min size 4 Min size on target 4
Filter          ambiguous:711   included:5716
All             15857
Small1          6186
Absent          5
Off target      835
Ambiguous       552
Small2          2263
On target       6016    6016
```

```
gzip genes_20230311.txt
```
