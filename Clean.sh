#!/bin/bash

shared_variable="Apple" # Change to Apple as needed
s_dir="./images"
z_dir="./learnings_$shared_variable.zip"
build=$(find . -not -path $s_dir -not -path ./.git -not -path $z_dir -mindepth 1 -maxdepth 1 -type d)
rm -r $build;

rm distribution.csv;

rm features.csv features_validation.csv
rm features_Test_$shared_variable_*.csv features_Train_$shared_variable_*.csv;
rm features_$shared_variable.csv features_validation_$shared_variable.csv

rm features_not_normalized_old.csv features_not_normalized.csv;
rm features_not_normalized_old_$shared_variable.csv features_not_normalized_$shared_variable.csv;

rm features_not_normalized_validation_old.csv features_not_normalized_validation.csv;
rm features_not_normalized_validation_old_$shared_variable.csv features_not_normalized_validation_$shared_variable.csv;

rm features_*_.csv thetas.csv thetas_old.csv;
rm thetas_$shared_variable.csv thetas_old_$shared_variable.csv;

rm statistics.csv statistics_old.csv *_color_histogram_multiple.png;
rm statistics_$shared_variable.csv statistics_old_$shared_variable.csv;

rm categories.csv categories_truth.csv dataset_test.csv dataset_test_truth.csv;
rm categories_$shared_variable.csv categories_truth_$shared_variable.csv dataset_test_$shared_variable.csv dataset_test_truth_$shared_variable.csv;

rm output_class_I_old.png output_class_I.png output_class_II.png output_scurve.png;
rm output_class_I_old_$shared_variable.png output_class_I_$shared_variable.png output_class_II_$shared_variable.png output_scurve_$shared_variable.png;
