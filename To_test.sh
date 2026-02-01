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

# echo "processing train pictures' augmentations..."
# for subdir in To_test/Train*/; do
#     if [[ "$subdir" == *$shared_variable* ]]; then
#         echo "$subdir"
#         ./Augmentation.py "$subdir" &
#     fi
# done
# wait

./train.py;

mv features.csv dataset_test_truth.csv;
mv features_validation.csv dataset_test.csv;
mv thetas.csv thetas_old.csv;
mv output_class_I.png output_class_I_old.png;
mv statistics.csv statistics_old.csv;
mv features_not_normalized.csv features_not_normalized_old.csv
mv features_not_normalized_validation.csv features_not_normalized_validation_old.csv;

echo "processing test pictures' transformations...";
for subdir in To_test/Test*/; do
    if [[ "$subdir" == *$shared_variable* ]]; then
        echo "$subdir"
        ./Transformation.py "$subdir" &
    fi
done
wait

# echo "processing test pictures' augmentations..."
# for subdir in To_test/Test*/; do
#     if [[ "$subdir" == *$shared_variable* ]]; then
#         echo "$subdir"
#         ./Augmentation.py "$subdir" &
#     fi
# done
# wait

if [[ $(uname -s) == "Darwin" ]]; then
    sed -i '' 's/"Train_"/"Test_"/g' train.py
else
    sed -i 's/"Train_"/"Test_"/g' train.py
fi;

./train.py;

mv thetas.csv thetas_$shared_variable.csv;
mv thetas_old.csv thetas_old_$shared_variable.csv;

mv statistics.csv statistics_$shared_variable.csv;
mv statistics_old.csv statistics_old_$shared_variable.csv;

mv output_class_I.png output_class_I_$shared_variable.png
mv output_class_I_old.png output_class_I_old_$shared_variable.png;

mv features_not_normalized.csv features_not_normalized_$shared_variable.csv
mv features_not_normalized_old.csv features_not_normalized_old_$shared_variable.csv
mv features_not_normalized_validation.csv features_not_normalized_validation_$shared_variable.csv
mv features_not_normalized_validation_old.csv features_not_normalized_validation_old_$shared_variable.csv

mv dataset_test_truth.csv dataset_test_truth_$shared_variable.csv;
mv dataset_test.csv dataset_test_$shared_variable.csv;

./predict.py;

mv output_class_II.png output_class_II_$shared_variable.png
mv output_scurve.png output_scurve_$shared_variable.png

mv features.csv features_$shared_variable.csv;
mv features_validation.csv features_validation_$shared_variable.csv

mv categories.csv categories_$shared_variable.csv
mv categories_truth.csv categories_truth_$shared_variable.csv

./compare.py;

if [[ $(uname -s) == "Darwin" ]]; then
    sed -i '' 's/"Test_"/"Train_"/g' train.py
else
    sed -i 's/"Test_"/"Train_"/g' train.py

fi;

zip -rq learnings_$shared_variable.zip ./To_test/ thetas_$shared_variable.csv thetas_old_$shared_variable.csv