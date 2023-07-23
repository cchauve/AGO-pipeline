# Experiments using gene content inferred with parsimony

## Anopheles dataset

Creating input files
```
cp ../../data/VectorBase/species_tree_4.newick Anopheles/
python scripts/Count_create_input_files.py ../../data/VectorBase/gene_orders_X_2.txt ../../data/VectorBase/families_X_2.txt Anopheles/input_count_X_2.csv
python scripts/Count_create_input_files.py ../../data/VectorBase/gene_orders_X_3.txt ../../data/VectorBase/families_X_3.txt Anopheles/input_count_X_3.csv
```
Running count
```
./anopheles.sh
```

## YGOB dataset

```
cp ../../data/YGOB/species_tree.newick YGOB/
python scripts/Count_create_input_files.py ../../data/YGOB/gene_orders.txt ../../data/YGOB/families.txt YGOB/input_count.csv
```
Running count
```
./YGOB.sh
```