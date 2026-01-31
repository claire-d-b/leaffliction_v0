#!/usr/bin/env python3

from pathlib import Path
import random
import shutil
from sys import argv
from Shared_variables import chosen_category


def get_random_images(source_folder, n=25):
    source = Path(source_folder)

    image_extensions = {'.JPG'}
    images = [f for f in source.iterdir() if f.suffix in image_extensions]
    selected = random.sample(images, min(n, len(images)))

    return selected


def copy_random_images(source_files, destination_folder, n=25):
    """Copy n random images from source to destination"""
    # source = Path(source_folder)
    dest = Path(destination_folder)

    # Create destination
    dest.mkdir(parents=True, exist_ok=True)

    # Get image files
    images = source_files

    # Select random images
    selected = random.sample(images, min(n, len(images)))

    # Copy them
    for img in selected:
        shutil.copy2(img, dest / img.name)
        print(f"Copied: {img.name}")

    print(f"\nCopied {len(selected)} images")


if __name__ == "__main__":
    try:
        if len(argv) == 1:
            selected_type = chosen_category
            directory = Path("images")

            # Get subdirectory Path objects from "images" directory,
            # if selected_type is found in name of subdirectories.
            subdirs = [d for d in directory.iterdir()
                       if d.is_dir() and selected_type in d.name]
            print([d.name for d in subdirs])

            selected_subdirs = random.sample(subdirs, 4)
            print([d.name for d in selected_subdirs])

            for subdir in selected_subdirs:
                images = get_random_images(subdir, n=25)
                copy_random_images(images, f"Dataset/{Path(subdir).name}/Base/", n=25)
                Path(f"Dataset/{Path(subdir).name}/\
Transformed").mkdir(parents=True, exist_ok=True)
                Path(f"Dataset/{Path(subdir).name}/\
Augmented").mkdir(parents=True, exist_ok=True)

        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")
    except AssertionError as error:
        print(f"{error}")
