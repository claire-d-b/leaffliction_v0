#!/usr/bin/env python3

from pandas import DataFrame, read_csv
from numpy import clip


def load(path: str) -> DataFrame:
    """Function that opens a file and display inner data in the shape
    of a datatable"""
    try:
        # Ici open est un gestionnaire de contexte qui retourne un
        # object-fichier
        file = read_csv(path, index_col=0)
    except Exception as error:
        raise AssertionError(f"Error: {error}")
    return file


def get_min(df: DataFrame):
    nlst = sort_list(list(df))
    return nlst[0]


def get_max(df: DataFrame):
    nlst = sort_list(list(df))
    return nlst[len(nlst)-1]


def sort_list(sort_list: list):
    n = len(sort_list)
    for i in range(n):
        # Find the minimum element in the unsorted part of the list
        min_index = i
        for j in range(i + 1, n):
            if sort_list[j] < sort_list[min_index]:
                min_index = j
        # Swap the found minimum element with the first element
        sort_list[i], sort_list[min_index] = sort_list[min_index], sort_list[i]

    return sort_list


# def z_score_normalize_df(df, chosen_category):
#     """Z-score normalization - saves mean and std to statistics.csv"""
#     normalized_df = df.copy()
#     numeric_columns = df.select_dtypes(include=float).columns

#     stats = {'column': [], 'mean': [], 'std': []}

#     for col in numeric_columns:
#         col_mean = df[col].mean()
#         col_std = df[col].std()

#         stats['column'].append(col)
#         stats['mean'].append(col_mean)
#         stats['std'].append(col_std)

#         if col_std > 0:
#             normalized_df[col] = (df[col] - col_mean) / col_std
#             normalized_df[col] = normalized_df[col]
#         else:
#             normalized_df[col] = 0

#     stats_df = DataFrame(stats)
#     stats_df.to_csv(f'statistics_{chosen_category}.csv', index=False)

#     return normalized_df


import pandas as pd
from pandas import DataFrame
import numpy as np

def z_score_normalize_df(df, category_name, exclude_columns=None):
    """
    Z-score normalize a dataframe and save statistics to CSV.
    
    After normalization: mean ≈ 0, std ≈ 1
    
    Args:
        df: DataFrame to normalize
        category_name: Name for CSV file (e.g., 'Apple_scab')
        exclude_columns: List of columns to skip (e.g., ['Subname', 'Category'])
    
    Returns:
        (normalized_df, statistics_df)
    """
    
    normalized_df = df.copy()
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Exclude metadata columns
    if exclude_columns:
        numeric_cols = [c for c in numeric_cols if c not in exclude_columns]
    
    # Calculate statistics
    stats = {'column': [], 'mean': [], 'std': []}
    
    for col in numeric_cols:
        col_mean = df[col].mean()
        col_std = df[col].std()
        
        stats['column'].append(col)
        stats['mean'].append(col_mean)
        stats['std'].append(col_std)
        
        if col_std > 0:
            normalized_df[col] = (df[col] - col_mean) / col_std
        else:
            print(f"⚠️  {col} has std=0")
            normalized_df[col] = 0
    
    # Create statistics dataframe
    stats_df = DataFrame(stats)
    
    # Verify
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    print("\nMean (should be ≈ 0):")
    for col, m in zip(numeric_cols, normalized_df[numeric_cols].mean()):
        status = "✓" if abs(m) < 0.0001 else "✗"
        print(f"  {status} {col:20s}: {m:12.8f}")
    
    print("\nStd (should be ≈ 1):")
    for col, s in zip(numeric_cols, normalized_df[numeric_cols].std()):
        status = "✓" if 0.9999 < s < 1.0001 else "✗"
        print(f"  {status} {col:20s}: {s:12.8f}")
    print()
    
    # Save statistics
    filename = f'statistics_{category_name}.csv'
    stats_df.to_csv(filename, index=False)
    print(f"✓ Saved to: {filename}\n")
    
    return normalized_df, stats_df


def normalize_df(df):
    """Min-Max normalization to [-1, 1] range"""
    normalized_df = df.copy()
    numeric_columns = df.select_dtypes(include=float).columns
    stats = {'column': [], 'min': [], 'max': []}

    for col in numeric_columns:
        col_min = df[col].min()
        col_max = df[col].max()
        stats['column'].append(col)
        stats['min'].append(col_min)
        stats['max'].append(col_max)

        if col_max > col_min:
            # Scale to [-1, 1]
            normalized_df[col] = 2 * (
                df[col] - col_min) / (col_max - col_min) - 1
        else:
            normalized_df[col] = 0

    stats_df = DataFrame(stats)
    stats_df.to_csv('statistics.csv', index=False)
    return normalized_df


def get_dot(lst: list, other: list):
    """Computes the scalar product with specific vectors"""
    temp = []
    for index in range(len(lst)):
        temp.append(lst[index] * other[index])
    res = 0
    for index in range(len(lst)):
        res += temp[index]
    return res
