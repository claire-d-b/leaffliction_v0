#!/usr/bin/env python3

import os
import csv
from pathlib import Path
from sys import argv
from matplotlib.pyplot import savefig, close, subplots
from pandas import DataFrame


def get_subdirs_with_image_count(parent_dir):
    """
    Get all subdirectories from a parent directory and count images in each.
    Returns a list of dictionaries with directory info and image counts.
    """
    subdirs_info = []
    image_extension = '.jpg'

    # Check if parent directory exists
    if not os.path.isdir(parent_dir):
        print(f"Error: {parent_dir} is not a valid directory")
        return

    # Get all items in parent directory
    try:
        items = os.listdir(parent_dir)
    except PermissionError:
        print(f"Error: Permission denied to access {parent_dir}")
        return

    # Iterate through items and get subdirectories
    for item in sorted(items):
        item_path = os.path.join(parent_dir, item)
        subfolder_names = ['Base', 'Transformed', 'Augmented']

        for sname in subfolder_names:
            item_path = f"{argv[1].removeprefix("./")}/{item}/{sname}"

            if Path(item_path).is_dir():
                # Check if it's a directory
                # Count images in this subdirectory
                image_count = 0

                try:
                    for file in os.listdir(item_path):
                        file_path = os.path.join(item_path, file)
                        # Check if it's a file and has image extension
                        if os.path.isfile(file_path):
                            file_ext = os.path.splitext(file)[1].lower()
                            if file_ext == image_extension:
                                image_count += 1
                except PermissionError:
                    print(f"Warning: Permission denied to access {item_path}")
                    return

                subdirs_info.append({
                    'Directory': item,
                    'Path': item_path,
                    'Image_Count': image_count
                })

    return subdirs_info


def save_to_csv(subdirs_info, output_file='distribution.csv'):
    """
    Save subdirectory information to a CSV file.
    """
    if not subdirs_info:
        print("No subdirectories found")
        return

    try:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Directory', 'Image_Count', 'Path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in subdirs_info:
                writer.writerow({
                    'Directory': row['Directory'],
                    'Image_Count': row['Image_Count'],
                    'Path': row['Path']
                })

        print(f"CSV file created: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error creating CSV: {e}")
        return None


def main():
    # Example usage - change this path to your parent directory
    parent_directory = argv[1].removeprefix("./")

    # Get subdirectories with image counts
    subdirs_info = get_subdirs_with_image_count(parent_directory)

    # Print results
    if subdirs_info:

        total_images = 0
        for info in subdirs_info:
            if info['Image_Count'] > 0:
                total_images += info['Image_Count']

        # Save to CSV
        save_to_csv(subdirs_info)

        fig, ax = subplots()
        subdirs_info = DataFrame(subdirs_info)
        summed_info_values = subdirs_info.groupby('Directory\
')['Image_Count'].sum()
        summed_info_labels = subdirs_info.groupby('Directory\
')['Directory'].sum()
        ax.pie(summed_info_values, labels=summed_info_labels,
               autopct='%1.1f%%')
        savefig(f"{parent_directory}/Distribution_Pie")
        ax.clear()
        fig.clf()
        close(fig)

        fig, ax = subplots()
        bars = ax.bar([i for i, x in enumerate((
                      summed_info_values.astype(int)))],
                      summed_info_values.astype(int),
                      label=summed_info_labels)
        total = sum(summed_info_values)
        ax.bar_label(bars, fmt=lambda x: f'{100*x/total:.1f}%')
        ax.set_ylim(bottom=0)
        savefig(f"{parent_directory}/Distribution_Bar")
        ax.clear()
        fig.clf()
        close(fig)

    else:
        print("No subdirectories found or parent directory doesn't exist")


if __name__ == "__main__":
    try:
        if len(argv) == 2:
            main()
        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")
    except AssertionError as error:
        print(f"{error}")
