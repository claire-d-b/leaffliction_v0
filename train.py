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


def train(arg=None):
    """Plot the attributes' values for training images and classify
    them"""
    csv_files = glob.glob(f"features_{chosen_category}_*.csv")

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
    categories = sorted(origin_df['Category'].unique().tolist())

    origin_df = origin_df.groupby("Subname").agg({
        'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        **{col: 'median' for col in
           origin_df.select_dtypes(include=[number]).columns}
    })
    origin_df = origin_df.reset_index(drop=False)

    origin_df = origin_df.sort_values(by='Subname')

    repr_df = origin_df.copy()

    # origin_df.to_csv("dataset_test_truth.csv", index=False)
    # norigin_df = origin_df.copy()
    # origin_df['Category'] = None
    # norigin_df.to_csv("dataset_test.csv", index=False)

    # df_subname = origin_df.iloc[:, [0]]
    # df_house = origin_df.iloc[:, [1]]
    # df_course = origin_df.iloc[:, 2:]

    # df = concat([df_subname, df_house], axis=1)
    # df = concat([df, df_course], axis=1)

    # df = df.sort_values(by='Category')
    summed_df = origin_df.groupby("Category", as_index=False).median(numeric_only=True)

    w = []
    b = []
    # Generate a random floating-point number between -0.001 and 0.001
    # to ensure there is no bias when calculating thetas.
    theta_0 = random.uniform(-0.001, 0.001)
    theta_1 = random.uniform(-0.001, 0.001)

    for i in range(len(categories)):
        w.insert(i, [])
        b.insert(i, [])
        # Scores of all images for the 9 values in each class :
        # 4 lists of 9 values
        overall_scores = [item for sublist in summed_df[summed_df
                          ['Category'] == categories[i]].iloc[:, 1:].values
                          for item in sublist]

        for j, item in enumerate(overall_scores):
            weight, bias, _ = minimize_cost(len(overall_scores),
                                            theta_0, theta_1,
                                            item, 1, 0.001)
            w[i].insert(j, weight)
            b[i].insert(j, bias)

    # Here we take the average value of ou bias
    bias = [sum(b_row) / len(b_row) for b_row in b if len(b_row)]

    # Write reusable thetas to a file

    f = open(f"thetas_{chosen_category}.csv", "w")
    f.write(f"categories: {categories}\n")
    thetas_1 = [[float(x) for x in row] for row in w]
    f.write(f"theta_0: {bias}\ntheta_1: {thetas_1}")
    f.close()

    ncolors = ['red', 'blue', 'green', 'gray', 'pink',
               'purple', 'cyan', 'lightgreen']
    n = len(categories)

    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
    n = len(categories)

    random_markers = random.sample(nmarkers, n)

    pairplot(repr_df, hue="Category", palette=random_colors,
             markers=random_markers)

    savefig("output_class_I")
    # Clear the figure content
    clf()
    close()

    zip_path = Path('learnings.zip')

    if zip_path.exists():
    # Add to existing zip
        with zipfile.ZipFile(zip_path, 'a') as zf:
            zf.write(f'thetas_{chosen_category}.csv')
        
            # Add entire folder recursively
            for file in Path(arg).rglob('*'):
                if file.is_file():
                    zf.write(file, arcname=f"{arg}_{chosen_category}")
    # Create a new zip file
    else:
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(f'thetas_{chosen_category}.csv')
            
            for file in Path(arg).rglob('*'):
                if file.is_file():
                    zf.write(file, arcname=f"{arg}_{chosen_category}")


if __name__ == "__main__":
    try:
        # if len(argv) == 1:
        #     train()

        if len(argv) == 2:

            directory = Path(argv[1])

            subdirs = [d for d in directory.iterdir() if d.is_dir()]
            subdirs = [str(d) for d in directory.iterdir() if d.is_dir()]
            print("subdirectories", subdirs)

            for subdir in subdirs:
                files = glob.glob(f"{subdir}")
                for file in files:
                    process_input_transformation(file, openImage=False,
                                                 single=False)
            # for subdir in subdirs:
            #     files = glob.glob(f"{subdir}")
            #     for file in files:
            #         process_input_augmentation(file, openImage=False,
            #                                    single=False)
            train(argv[1].removeprefix("./"))
        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")
