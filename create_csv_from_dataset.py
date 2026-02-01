#!/usr/bin/env python3

from utils import load, z_score_normalize_df
from linear_regression import minimize_cost
from matplotlib.pyplot import savefig, clf, close
from pandas import concat, read_csv
from seaborn import pairplot
import random
import glob
from numpy import number
from sys import argv
from pathlib import Path
from Transformation import process_input_transformation
from Augmentation import process_input_augmentation
from Shared_variables import chosen_category
import zipfile


def remove_prefixes(categories, prefixes):
    """Remove multiple prefixes from categories"""
    result = []
    for cat in categories:
        for prefix in prefixes:
            if cat.startswith(prefix):
                cat = cat.replace(prefix, '', 1)
                break
        result.append(cat)
    return result


def create_csv_from_random_dataset(arg=None):
    """Plot the attributes' values for training images and classify
    them"""
    csv_files = glob.glob(f"{arg}/**/{chosen_category}_*_Transformed_features_test.csv")
    print("csv files", csv_files)

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

    origin_df = concat(dfs, ignore_index=True)

    # origin_df.to_csv("features_not_normalized.csv", mode="w",
    #                  header=True, index=False)
    # new_df = load("features_not_normalized.csv")
    # new_df['Category'] = None
    # new_df = new_df.reset_index(drop=False)
    # new_df.to_csv("features_not_normalized_validation.csv", mode="w",
    #               header=True, index=False)

    origin_df = z_score_normalize_df(origin_df)

    origin_df = origin_df.groupby("Subname").agg({
        'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        **{col: 'median' for col in
           origin_df.select_dtypes(include=[number]).columns}
    })
    origin_df = origin_df.reset_index(drop=False)

    origin_df = origin_df.sort_values(by='Subname')

    repr_df = origin_df.copy()

    origin_df.to_csv(f"dataset_test_truth_{chosen_category}.csv", index=False)
    norigin_df = origin_df.copy()
    norigin_df['Category'] = None
    norigin_df.to_csv(f"dataset_test_{chosen_category}.csv", index=False)


if __name__ == "__main__":
    try:
        # directory = Path(argv[1])

        # subdirs = [d for d in directory.iterdir() if d.is_dir()]
        # subdirs = [str(d) for d in directory.iterdir() if d.is_dir()]
        # # print("subdirectories", subdirs)

        # for subdir in subdirs:
        #     files = glob.glob(f"{subdir}")
        #     for file in files:
        #         process_input_transformation(file, openImage=False,
        #                                         single=False)
        # for subdir in subdirs:
        #     files = glob.glob(f"{subdir}")
        #     for file in files:
        #         process_input_augmentation(file, openImage=False,
        #                                     single=False)
        create_csv_from_random_dataset(arg=argv[1].removeprefix('./'))

    except AssertionError as error:
        print(f"{error}")
