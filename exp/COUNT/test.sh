#!/bin/bash

java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.ML dev/species_tree.newick dev/family_content.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > dev/test_ML.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.Posteriors dev/species_tree.newick dev/family_content.csv dev/test_ML.out \
    | sed 's/node /node_/g' | sed "s/'//g" > dev/test_Posteriors.out
java -Xmx2048M -cp ./bin/Count.jar ca.umontreal.iro.evolution.genecontent.AsymmetricWagner dev/species_tree.newick dev/family_content.csv \
    | sed 's/node /node_/g' | sed "s/'//g" > dev/test_AsymmetricWagner.out

