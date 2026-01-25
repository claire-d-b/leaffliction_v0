#!/bin/bash

# ********** APPLE OR GRAPE **********

# Grape version :
echo "processing train pictures' transformations...";
for subdir in To_test/Train*/; do
    if [[ "$subdir" == *"Apple"* ]]; then
        echo "$subdir"
        ./Transformation.py "$subdir" &
    fi
done
wait

# echo "processing train pictures' augmentations..."
# for subdir in To_test/Train*/; do
#     if [[ "$subdir" == *"Apple"* ]]; then
#         echo "$subdir"
#         ./Augmentation.py "$subdir" &
#     fi
# done
# wait

./train.py;

mv features.csv dataset_test_truth.csv;
mv features_validation.csv dataset_test.csv;
mv thetas_Apple.csv thetas_Apple_old.csv; # CHANGE BY APPLE IF NECESSARY
mv output_class_I.png output_class_I_old.png;
mv statistics.csv statistics_old.csv;
mv features_not_normalized.csv features_not_normalized_old.csv
mv features_not_normalized_validation.csv features_not_normalized_validation_old.csv;

echo "processing test pictures' transformations...";
for subdir in To_test/Test*/; do
    if [[ "$subdir" == *"Apple"* ]]; then
        echo "$subdir"
        ./Transformation.py "$subdir" &
    fi
done
wait

# echo "processing test pictures' augmentations..."
# for subdir in To_test/Test*/; do
#     if [[ "$subdir" == *"Apple"* ]]; then
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

./predict.py;
./compare.py;

if [[ $(uname -s) == "Darwin" ]]; then
    sed -i '' 's/"Test_"/"Train_"/g' train.py
else
    sed -i 's/"Test_"/"Train_"/g' train.py

fi;