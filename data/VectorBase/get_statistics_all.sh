#!/bin/bash

python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 1 2 >  statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 2 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 1 3 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 2 3 >> statistics.txt

python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 2L 2R' 1 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 2L 2R' 2 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 2L 2R' 1 3 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 2L 2R' 2 3 >> statistics.txt

python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '3 3L 3R' 1 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '3 3L 3R' 2 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '3 3L 3R' 1 3 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '3 3L 3R' 2 3 >> statistics.txt

python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 1 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 2 2 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 1 3 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 2 3 >> statistics.txt

python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 3 5 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 4 5 >> statistics.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt '2 3 2L 2R 3L 3R' 4 4 >> statistics.txt
