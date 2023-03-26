#!/bin/bash

python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 'Anopheles_gambiae_PEST Anopheles_atroparvus_EBRO Anopheles_funestus_FUMOZ Anopheles_albimanus_STECLA' 1 2 >  statistics_assembled.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 'Anopheles_gambiae_PEST Anopheles_atroparvus_EBRO Anopheles_funestus_FUMOZ Anopheles_albimanus_STECLA' 2 2 >> statistics_assembled.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 'Anopheles_gambiae_PEST Anopheles_atroparvus_EBRO Anopheles_funestus_FUMOZ Anopheles_albimanus_STECLA' 1 3 >> statistics_assembled.txt
python ../../scripts/VectorBase_utils.py stats genes_20230311.txt X 'Anopheles_gambiae_PEST Anopheles_atroparvus_EBRO Anopheles_funestus_FUMOZ Anopheles_albimanus_STECLA' 2 3 >> statistics_assembled.txt
