#!/usr/bin/env python3

from utils import load, get_max
from matplotlib.pyplot import savefig, clf, close, figure, axhline, scatter
from matplotlib.pyplot import legend, gca
from pandas import DataFrame, read_csv, concat
from seaborn import pairplot
from math import e
from glob import glob
import csv
import ast
import random
from numpy import number, dot, array, argmax
from sys import argv
from Transformation import process_input_transformation
from pathlib import Path
import zipfile
from strstr_extract import extract_known_categories
from Shared_variables import chosen_category


def predict():
    """Creates a pairplot showing predictions for a specific set of
    pictures. Show s-curve illustrating sigmoid function translation
    of an input value into a probability."""
    df = load(f"dataset_test_truth_{chosen_category}.csv")

    # df = normalize_df(df)

    df = df.sort_values(by='Subname')

    df = df.groupby("Subname").agg({
        'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        **{col: 'median' for col in df.select_dtypes(include=[number]).columns}
    })
    df = df.reset_index(drop=False)

    DataFrame(df.iloc[:, :2].to_csv(f"categories_truth_{chosen_category}.csv", header=True,
              index=False))
    ndf = load(f"dataset_test_{chosen_category}.csv")
    # ndf = normalize_df(ndf)

    # zip_path = 'learnings.zip'
    # extract_to = './'  # Project root

    # with zipfile.ZipFile(zip_path, 'r') as zf:
    #     zf.extractall(extract_to)

    with open(f"thetas_{chosen_category}.csv", "r") as f:
        lines = f.readlines()
        categories = ast.literal_eval(lines[0].split(":", 1)[1].strip())
        bias = ast.literal_eval(lines[1].split(":", 1)[1].strip())
        w = ast.literal_eval(lines[2].split(":", 1)[1].strip())
    # Parse statistics from CSV file
    means = []
    stds = []
    channels = []
    with open(f"statistics_{chosen_category}.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            channels.append(row['column'])
            means.append(float(row['mean']))
            stds.append(float(row['std']))

    # Convert to numpy arrays
    means_array = array(means)
    stds_array = array(stds)
    
    # Apply z-score normalization: (x - mean) / std
    print("Formula: (x - mean) / std")
    print()
    df_normalized = ndf.copy()

    # Calculate from test data itself
    test_means = ndf[channels].mean()
    test_stds = ndf[channels].std()
    df_normalized[channels] = (ndf[channels] - test_means) / test_stds

    # df_normalized[channels] = (ndf[channels] - means_array) / stds_array

    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    print()
    
    print("Mean of normalized columns (should be ≈ 0):")
    col_means = df_normalized[channels].mean()
    for ch, m in zip(channels, col_means):
        print(f"  {ch:20s}: {m:10.6f}")
    print()
    
    print("Std of normalized columns (should be ≈ 1):")
    col_stds = df_normalized[channels].std()
    for ch, s in zip(channels, col_stds):
        print(f"  {ch:20s}: {s:10.6f}")
    print()

    ncolors = ['red', 'blue', 'green', 'gray', 'pink', 'purple',
               'cyan', 'lightgreen']
    n = len([item for item in categories if item is not None])

    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']

    random_markers = random.sample(nmarkers, n)

    # Make predictions based on computed thetas
    predictions = []
    # We iterate on a specific number of rows (images) and 9 columns
    # (values like brightness for example)
    # We make 4 predictions <=> probability that the image will
    # belong to each class.
    # We take the highest probability.
    figure(figsize=(8, 5))

    for i, col in enumerate(df_normalized.iloc[:, 1:].values):
        predictions.insert(i, [])

        for j in range(len(categories)):
            z = dot(col, w[j]) + bias[j]
            predictions[i].insert(j, 1 / (1 + (e ** -z)))
            scatter(z, 1 / (1 + (e ** -z)),
                    color=random_colors[j % len(random_colors)],
                    marker='o', label=categories[j])

    # récupère tous les labels.
    handles, labels = gca().get_legend_handles_labels()
    # garde seulement un exemplaire de chaque label.
    by_label = dict(zip(labels, handles))
    # remplace la légende avec des labels uniques.
    legend(by_label.values(), by_label.keys())

    axhline(y=0.5, color='purple', linestyle='--',
            label="Seuil de décision (0.5)")
    savefig("output_scurve")
    clf()
    close()

    # Values upper than 0.5 indicates a probability that the image
    # will be in target class (categories[j]), whereas a < 0.5 value
    # tends to indicate the image belongs to another class.
    # when z is pos, the sigmoid function approches 1, whereas when
    # z is negative, the sigmoid function approaches 0.
    # From predictions get the highest value and corresponding class:
    ncategories = [categories[p.index(get_max(p))] for p
                   in predictions]

    ntypes = ['Train_', 'Test_']
    for nntype in ntypes:
        categories = [cat.replace(nntype, '') for cat in categories]
    # print("cats", categories)
    categories = sorted(list(dict.fromkeys(categories)))  # Keeps order

    df_normalized['Category'] = [extract_known_categories(ncategory, categories)
                       for ncategory in ncategories]
    df_normalized = df_normalized.sort_values(by='Subname')

    df_normalized = df_normalized.groupby("Subname").agg({
        'Category': lambda x: x.mode()[0] if len(x.mode()) > 0
        else x.iloc[0],  # Prend la première catégorie prédite
        **{col: 'median'
           for col in df_normalized.select_dtypes(include=[number]).columns}
    })
    df_normalized = df_normalized.reset_index(drop=False)
    DataFrame(df_normalized.iloc[:, :2]).to_csv(f"categories_{chosen_category}.csv", header=True,
                                      index=False)

    for i in range(len(categories)):
        filtered_df = df_normalized[df_normalized['Category'] == categories[i]]
        percent = len(filtered_df.iloc[:, 1]) * 100 / len(df_normalized.iloc[:, 1])
        print(f"There are {percent}% students from test data \
who would probably belong to {categories[i]}")

    pairplot(DataFrame(df_normalized), hue="Category", palette=random_colors,
             markers=random_markers)

    savefig("output_class_II")
    clf()
    close()


if __name__ == "__main__":
    try:
        if len(argv) == 1:
            predict() # dataset pred
        elif len(argv) == 2:
            # single pred
            csv_path = f"{Path(argv[1]).parent.parent}/{Path(argv[1]).parent.parent.name}_Augmented_features_test.csv"
            print("path", csv_path)
            csv_files = glob(csv_path)

            dfs = []
            for i, file in enumerate(csv_files):
                try:
                    if i == 0:
                        # First file: keep header
                        df = read_csv(file)
                    else:
                        # Subsequent files: skip header (first row)
                        df = read_csv(file, skiprows=1, header=None)
                        # Use column names from the first dataframe
                        df.columns = dfs[0].columns
                    dfs.append(df)
                except Exception as e:
                    print(f"warning: {e}")
                    continue

            df = concat(dfs, ignore_index=True)

            with open(f"thetas_{chosen_category}.csv", "r") as f:
                lines = f.readlines()
                categories = ast.literal_eval(lines[0].split(":", 1)[1].strip())
                bias = ast.literal_eval(lines[1].split(":", 1)[1].strip())
                w = ast.literal_eval(lines[2].split(":", 1)[1].strip())

            print(Path(Path(argv[1]).name).stem)
            df = df[df["Category"] == extract_known_categories(Path(Path(argv[1]).name).stem, categories)]
            print(df)
            
            # zip_path = 'learnings.zip'
            # extract_to = './'  # Project root

            # with zipfile.ZipFile(zip_path, 'r') as zf:
            #     zf.extractall(extract_to)
            # Parse statistics from CSV file
            means = []
            stds = []
            channels = []
            with open(f"statistics_{chosen_category}.csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    channels.append(row['column'])
                    means.append(float(row['mean']))
                    stds.append(float(row['std']))

            # Convert to numpy arrays
            means_array = array(means)
            stds_array = array(stds)
            
            # Apply z-score normalization: (x - mean) / std
            print("Formula: (x - mean) / std")
            print()
            df_normalized = df.copy()

            # Calculate from test data itself
            test_means = df[channels].mean()
            test_stds = df[channels].std()
            df_normalized[channels] = (df[channels] - test_means) / test_stds

            # df_normalized[channels] = (df[channels] - means_array) / stds_array

            print("=" * 80)
            print("VERIFICATION")
            print("=" * 80)
            print()
            
            print("Mean of normalized columns (should be ≈ 0):")
            col_means = df_normalized[channels].mean()
            for ch, m in zip(channels, col_means):
                print(f"  {ch:20s}: {m:10.6f}")
            print()
            
            print("Std of normalized columns (should be ≈ 1):")
            col_stds = df_normalized[channels].std()
            for ch, s in zip(channels, col_stds):
                print(f"  {ch:20s}: {s:10.6f}")
            print() 
            print()

            print(df_normalized)

            # df_normalized = df_normalized.groupby("Subname").agg({
            #     'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
            #     **{col: 'median' for col in df_normalized.select_dtypes(include=[number]).columns}
            # })
            # df_normalized = df_normalized.reset_index(drop=False)

            predictions = []
            # We iterate on a specific number of rows (images) and 9 columns
            # (values like brightness for example)
            # We make 4 predictions <=> probability that the image will
            # belong to each class.
            # We take the highest probability.

            # df_normalized = df_normalized[df_normalized['Category'] == extract_known_categories(Path(argv[1].removeprefix('./')), categories)]
            # df_normalized = df_normalized.groupby("Subname").agg({
            #     'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
            #     **{col: 'median' for col in df_normalized.select_dtypes(include=[number]).columns}
            # })
            # df_normalized = df_normalized.reset_index(drop=False)

            # print("hihi", df_normalized)
            # subname = df_normalized.iloc[:, 0]
            # category = df_normalized.iloc[:, 2]
            # values = df_normalized.iloc[:, 4:]

            # df_normalized = concat([subname, category], axis=1)
            # df_normalized = concat([df_normalized, values], axis=1)

            df_normalized = df_normalized.groupby("Subname").agg({
                'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
                **{col: 'median' for col in df_normalized.select_dtypes(include=[number]).columns}
            })

            df_normalized = df_normalized.reset_index(drop=False)
            ndataset = df_normalized.copy()
            ndataset.to_csv(f"dataset_test_truth_{chosen_category}.csv", header=True, index=False)
            ndataset["Category"] = None
            ndataset.to_csv(f"dataset_test_{chosen_category}.csv", header=True, index=False)

            for i, col in enumerate(df_normalized.iloc[:, 2:].values):
                predictions.insert(i, [])

                for j in range(len(categories)):
                    z = dot(col, w[j]) + bias[j]
                    predictions[i].insert(j, 1 / (1 + (e ** -z)))
            print("pred", predictions)
            ncategories = [categories[p.index(get_max(p))] for p
                   in predictions]
            print(ncategories)

            # subname = df_normalized.iloc[:, 0]
            # category = df_normalized.iloc[:, 2]
            # values = df_normalized.iloc[:, 4:]

            # df_normalized = concat([subname, category], axis=1)
            # df_normalized = concat([df_normalized, values], axis=1)

            DataFrame(df_normalized.iloc[:, :2]).to_csv(f"categories_truth_{chosen_category}.csv", header=True,
                                      index=False)
            df_normalized["Category"] = None
            df_normalized["Category"] = [categories[argmax(x)] for x in predictions]
            DataFrame(df_normalized.iloc[:, :2]).to_csv(f"categories_{chosen_category}.csv", header=True,
                                      index=False)
            print(df_normalized["Category"])

            DataFrame(df_normalized.iloc[:, :2].to_csv(f"categories_truth_{chosen_category}.csv", header=True,
                    index=False))

        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")
