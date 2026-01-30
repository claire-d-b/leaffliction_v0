#!/usr/bin/env python3

from pandas import read_csv
from Shared_variables import chosen_category


def basic_comparison(file1, file2):
    """Basic comparison - shows differences between two CSV files"""
    print("=== BASIC COMPARISON ===")

    # Read CSV files
    df1 = read_csv(file1)
    df2 = read_csv(file2)

    print(f"File 1 shape: {df1.shape}")
    print(f"File 2 shape: {df2.shape}")

    # Check if columns are the same
    if list(df1.columns) == list(df2.columns):
        print("✓ Columns match")
    else:
        print("✗ Columns differ")
        print(f"File 1 columns: {list(df1.columns)}")
        print(f"File 2 columns: {list(df2.columns)}")

    # Check if data is identical
    if df1.equals(df2):
        print("✓ Files are identical")
    else:
        print("✗ Files differ")

        # Show different rows if same structure
        if df1.shape == df2.shape and list(df1.columns) == list(df2.columns):
            diff_mask = (df1 != df2).any(axis=1)
            diff_rows = df1[diff_mask].index.tolist()
            print(f"Different rows: {diff_rows}")
            print("length")
            print(f"{len(diff_rows)}")
            print("Accuracy rate")
            print(f"{round(100-len(diff_rows)*100/df1.shape[0], 2)}%")


if __name__ == "__main__":
    try:
        basic_comparison(f"categories_{chosen_category}.csv", f"categories_truth_{chosen_category}.csv")

    except AssertionError as error:
        print(f"{error}")
