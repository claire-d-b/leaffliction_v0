#!/bin/bash

s_dir="./images"
z_dir="./directory"
build=$(find . -not -path $s_dir -not -path ./.git -not -path $z_dir -mindepth 1 -maxdepth 1 -type d)
rm -r $build;

rm distribution.csv;
rm features.csv features_validation.csv;
rm features_not_normalized_old.csv features_not_normalized.csv;
rm features_not_normalized_validation_old.csv features_not_normalized_validation.csv;
rm features_*.csv thetas.csv thetas_old*.csv;
rm statistics.csv statistics_old.csv *_color_histogram_multiple.png;
rm categories.csv categories_truth.csv dataset_test.csv dataset_test_truth.csv;
rm output_class_I_old.png output_class_I.png output_class_II.png output_scurve.png;
