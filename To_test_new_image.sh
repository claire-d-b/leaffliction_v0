#!/bin/bash

shared_variable="Apple" # Change to Apple as needed

# ********** APPLE OR GRAPE **********

# Grape version :
echo "processing train pictures' transformations...";
for subdir in To_test/Train*/; do
    if [[ "$subdir" == *$shared_variable* ]]; then
        echo "$subdir"
        ./Transformation.py "$subdir" &
    fi
done
wait

./train.py;

mv features.csv dataset_test_truth.csv;
mv features_validation.csv dataset_test.csv;
mv thetas.csv thetas_old.csv;
mv output_class_I.png output_class_I_old.png;
mv statistics.csv statistics_old.csv;
mv features_not_normalized.csv features_not_normalized_old.csv
mv features_not_normalized_validation.csv features_not_normalized_validation_old.csv;

unzip -oq learnings_$shared_variable.zip -d .

mv dataset_test_truth.csv dataset_test_truth_$shared_variable.csv;
mv dataset_test.csv dataset_test_$shared_variable.csv;

./predict.py;

./compare.py;