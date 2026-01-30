#!/usr/bin/env python3

from pathlib import Path
import random
import shutil
from glob import glob
from strstr_extract import extract_known_categories
import os
from sys import argv
from Shared_variables import chosen_category


path_to_test_folder = "Unit/Unit_test2/Base"


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


def copy_single_image(source_image, destination_folder):
    """Copy a single image from source to destination folder"""
    source = Path(source_image)
    dest = Path(destination_folder)

    # Validate source image exists
    if not source.exists():
        raise FileNotFoundError(f"Image not found: {source}")

    if not source.is_file():
        raise ValueError(f"Source is not a file: {source}")

    # Create destination folder
    dest.mkdir(parents=True, exist_ok=True)

    # Copy the image
    shutil.copy2(source, dest / source.name)
    print(f"Copied: {source.name} -> {dest / source.name}")


if __name__ == "__main__":
    try:
        if len(argv) == 1:
            selected_type = chosen_category
            directory = Path("images")

            # Get subdirectory Path objects from "images" directory,
            # if selected_type is found in name of subdirectories.
            subdirs = [d for d in directory.iterdir()
                       if d.is_dir() and selected_type in d.name]

            selected_subdirs = random.sample(subdirs, 4)
            selected_subdirs = sorted(selected_subdirs)
            categories = [d.name for d in selected_subdirs]

            jpg_files = list(Path(path_to_test_folder).glob("*.JPG"))

            if not jpg_files:
                raise AssertionError("Please provide a correct \
folder name for images to test.")

            else:
                images = sorted(glob(f"{path_to_test_folder}/*.JPG"))
                for img in images:
                    # On copie chaque image du set de test, le nom
                    # de ces images doit contenir la catégorie pour
                    # que le programme fonctionne
                    copy_single_image(img, f"To_test/Train_\
{extract_known_categories(Path(Path(img).name).stem, categories)}/\
Base/")
                    # On crée des directories pour les images
                    # transformées, ou si besoin augmentées.
                    Path(f"To_test/Train_{extract_known_categories(
                                    Path(Path(img).name).stem, categories)}/\
Transformed").mkdir(parents=True, exist_ok=True)
                    Path(f"To_test/Train_{extract_known_categories(
                                    Path(Path(img).name).stem, categories)}/\
Augmented").mkdir(parents=True, exist_ok=True)

                for subdir in selected_subdirs:
                    # Ici on vérifie que les subfolders ont bien le même nombre
                    # d'images par classe.
                    folder_path = f"To_test/Train_\
{Path(subdir).name}/Base/"
                    print("fpath", folder_path)
                    num_files = (len([f for f in os.listdir(folder_path)
                                      if os.path.isfile(os.path.join(
                                                        folder_path, f
                                                        ))]))
                    print("nunu", num_files)

                    # Soustraire au nombre d'images injectées le nombre
                    # d'images déjà présentes.
                    images = get_random_images(subdir, n=(20 - num_files))

                    copy_random_images(images[2 - num_files:20], f"To_test/\
Train_{Path(subdir).name}/Base/", n=(20 - (2 - num_files)))

                    Path(f"To_test/Test_{Path(subdir).name}/\
Base").mkdir(parents=True, exist_ok=True)
                    Path(f"To_test/Test_{Path(subdir).name}/\
Transformed").mkdir(parents=True, exist_ok=True)
                    Path(f"To_test/Test_{Path(subdir).name}/\
Augmented").mkdir(parents=True, exist_ok=True)

        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")