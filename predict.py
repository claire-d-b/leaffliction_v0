#!/usr/bin/env python3

from utils import load, get_max
from matplotlib.pyplot import savefig, clf, close, figure, axhline, scatter
from matplotlib.pyplot import legend, gca
from pandas import DataFrame, read_csv
from seaborn import pairplot
from math import e
from glob import glob
import ast
import random
from numpy import number, dot
from sys import argv
from Transformation import process_input_transformation
from pathlib import Path
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

    with open(f"thetas_{chosen_category}.csv", "r") as f:
        lines = f.readlines()
        categories = ast.literal_eval(lines[0].split(":", 1)[1].strip())
        bias = ast.literal_eval(lines[1].split(":", 1)[1].strip())
        w = ast.literal_eval(lines[2].split(":", 1)[1].strip())

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

    for i, col in enumerate(ndf.iloc[:, 1:].values):
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

    ndf['Category'] = [extract_known_categories(ncategory, categories)
                       for ncategory in ncategories]
    ndf = ndf.sort_values(by='Subname')

    ndf = ndf.groupby("Subname").agg({
        'Category': lambda x: x.mode()[0] if len(x.mode()) > 0
        else x.iloc[0],  # Prend la première catégorie prédite
        **{col: 'median'
           for col in ndf.select_dtypes(include=[number]).columns}
    })
    ndf = ndf.reset_index(drop=False)
    DataFrame(ndf.iloc[:, :2]).to_csv(f"categories_{chosen_category}.csv", header=True,
                                      index=False)

    for i in range(len(categories)):
        filtered_df = ndf[ndf['Category'] == categories[i]]
        percent = len(filtered_df.iloc[:, 1]) * 100 / len(ndf.iloc[:, 1])
        print(f"There are {percent}% students from test data \
who would probably belong to {categories[i]}")

    pairplot(DataFrame(ndf), hue="Category", palette=random_colors,
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
            arg = Path(argv[1]).name.split('_', 1)[0]
            if Path(f"categories_{arg}.csv").exists():
                df = read_csv(f"categories_{arg}.csv")
                with open(f"thetas_{arg}.csv", "r") as f:
                    lines = f.readlines()
                    categories = ast.literal_eval(
                                                lines[0].split(
                                                ":", 1)[1].strip())

                category = extract_known_categories(argv[1], categories)
                folder = Path(argv[1]).name.split('_', 1)[0]
                subname = f"{folder}_Train_{category}"

                result = df[df['Subname\
'].str.lower().str.contains(subname.lower())]
                file = glob(f"{Path(argv[1]).parent}/{Path(argv[1]).name}")

                for unit in file:
                    process_input_transformation(src=unit, openImage=True,
                                                single=False,
                                                title=f"{Path(argv[1]).name} \
predicted as : {result.iloc[:, 1].values}")
        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")
