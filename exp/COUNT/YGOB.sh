#!/bin/bash

java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.ML \
     YGOB/species_tree.newick \
     YGOB/input_count.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > YGOB/ML.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.Posteriors \
     YGOB/species_tree.newick \
     YGOB/input_count.csv \
     YGOB/ML.out \
    | sed 's/node /node_/g' | sed "s/'//g" > YGOB/Posteriors.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.AsymmetricWagner \
     -gain 1 \
     YGOB/species_tree.newick \
     YGOB/input_count.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > YGOB/AsymetricWagner.out
#java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.DolloDisplay \
#     YGOB/species_tree.newick \
#     YGOB/input_count.csv \
#    | sed 's/node /node_/g' | sed "s/'//g" > YGOB/Dollo.out
