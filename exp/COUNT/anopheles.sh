#!/bin/bash

java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.ML \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_2.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_2_ML.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.Posteriors \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_2.csv \
     Anopheles/X_2_ML.out \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_2_Posteriors.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.AsymmetricWagner \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_2.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_2_AsymmetricWagner.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.AsymmetricWagner \
     -gain 1000 \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_2.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_2_Dollo.out

java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.ML \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_3.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_3_ML.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.Posteriors \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_3.csv \
     Anopheles/X_3_ML.out \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_3_Posteriors.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.AsymmetricWagner \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_3.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_3_AsymmetricWagner.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.AsymmetricWagner \
     -gain 1000 \
     Anopheles/species_tree_4.newick \
     Anopheles/input_count_X_3.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > Anopheles/X_3_Dollo.out
