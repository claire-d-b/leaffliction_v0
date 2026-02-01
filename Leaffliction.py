#!/usr/bin/env python3

from sys import argv


help_dict = \
    {
        './Build.sh':
        {
            'parameters':
            {
                '<None>': 'Create folder architecture for given images.'
            }
        },
        './Clean.sh':
        {
            'parameters':
            {
                '<None>': 'Remove files to reset the environment.'
            }
        },
        './Distribution.py':
        {
            'parameters':
            {
                '<directory>': 'Create charts showing images distribution.'
            }
        },
        './Transformation.py':
        {
            'parameters':
            {
                '<folder>': 'Apply transformations to all images in \
specified directory.',
                '<path_to_file>': 'Apply transformations to a specific image.'
            }
        },
        './Augmentation.py':
        {
            'parameters':
            {
                '<folder>': 'Apply augmentations to all images in \
specified directory.',
                '<path_to_file>': 'Apply augmentations to a specific image.'
            }
        },
        './train.py':
        {
            'parameters':
            {
                '<directory>': 'Apply transformations and augmentations \
to all images in a specific folder and its subfolders. Train the model and \
saves thetas and images into a zip.'
            }
        },
        './predict.py':
        {
            'parameters':
            {
                '<file>': 'Predict a single image class or classify in a given dataset.'
            }
        },
        './create_random_dataset_new_image.py':
        {
            'parameters':
            {
                '<None>': 'Randomly choose images for test and training \
(40 vs 160), including new images.'
            }
        },
        './create_random_dataset.py':
        {
            'parameters':
            {
                '<None>': 'Randomly choose images for test and training \
(40 vs 160).'
            }
        },
        './create_csv_from_dataset.py':
        {
            'parameters':
            {
                '<folder>': 'Creates a csv based on a folder specific images. \
The csv will be used for classification purposes.
            }
        }
    }


def show_helper():
    """Display help dictionary in formatted table"""
    # Print header
    print(f"{'Command':<30}{'Parameters':<30}{'Description':<60}")
    print("-" * 155)

    # Print data rows
    for script, details in help_dict.items():
        for param, description in details['parameters'].items():
            print(f"{script:<30}{param:<30}{description:<60}")


if __name__ == "__main__":
    try:
        if len(argv) == 2 and argv[1] == "--help":
            show_helper()
        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")
