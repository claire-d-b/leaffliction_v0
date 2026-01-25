#!/usr/bin/env python3

from sys import argv
from glob import glob
from os import path
from Augmentation_types import (get_contrast, get_scale_zoom,
                                get_horizontal_flip, get_rotate,
                                get_perspective_transformation,
                                get_affine_transformation)
from Transformation import process_file
from stats import get_len
from matplotlib.pyplot import close, subplots, tight_layout, show
from cv2 import imread
from pathlib import Path


def process_input_augmentation(src=None, dst=None, option=None,
                               openImage=True, single=False,
                               title=None) -> None:
    """Augmentation applies changes to create more images to train a model on,
    it is used for boosting the images' basis artificially.
    This function creates variations of a source image if src is a file,
    and print that image's variations. If src is a folder,s
    it augments multiple images in this folder."""

    dst = src

    img = None
    folder = src

    if src and path.isfile(src):
        pattern = folder
        ndst = f"{Path(pattern).parent.parent}/Augmented/"

        dst = f"{Path(src).parent.parent}"

        get_contrast(src, dst)
        get_scale_zoom(src, dst)
        get_horizontal_flip(src, dst)
        get_rotate(src, dst)
        get_affine_transformation(src, dst)
        get_perspective_transformation(src, dst)

        img = process_file(src, dst=ndst, category="Augmented",
                           augmented=True, single=single)
        if openImage is True:
            image_paths = ("_contrast.JPG", "_scalezoom.JPG",
                           "_horizontalflip.JPG", "_rotation.JPG",
                           "_affinetransformation.JPG",
                           "_perspectivetransformation.JPG")
            complete_paths = []
            for ipath in image_paths:
                filepath = Path(pattern).parent
                filename = Path(pattern).stem

                filepath = f"{Path(pattern).parent.parent}/Augmented/"
                complete_paths.append(f"{filepath}{filename}{ipath}")

            n_cols = 3
            n_rows = 2

            fig_width_per_image = 3  # inches per image width
            fig_height_per_image = 4  # inches per image height

            close('all')
            fig, axes = subplots(n_rows, n_cols,
                                 figsize=(fig_width_per_image * n_cols,
                                          fig_height_per_image * n_rows))
            if title:
                fig.suptitle(title, fontsize=16, fontweight='bold')
            # Flatten axes array for easy iteration
            axes = axes.flatten()

            for i, ipath in enumerate(complete_paths):
                image = imread(f"{ndst}{Path(ipath).name}")
                axes[i].imshow(image)
            tight_layout()
            show()
            close('all')

    else:
        if not folder.endswith('/'):
            folder = folder + '/'
        # Try to find multiple files using glob pattern
        pattern = f"{folder}Transformed/*.JPG"
        img = glob(pattern)

        ndst = f"{folder}Histogram_subcategory/"
        if img:
            print(f"Found {get_len(img)} files matching pattern: {pattern}")
            for i, image in enumerate(img):

                if dst.endswith('/'):
                    dst = dst.rstrip('/')

                get_contrast(image, dst)
                get_scale_zoom(image, dst)
                get_horizontal_flip(image, dst)
                get_rotate(image, dst)
                get_affine_transformation(image, dst)
                get_perspective_transformation(image, dst)
            process_file(img, dst=dst, category="Augmented",
                         augmented=True, single=single)

        else:
            print(f"No files found matching pattern: {pattern}")


if __name__ == "__main__":
    try:
        if get_len(argv) == 2:
            process_input_augmentation(src=argv[1].removeprefix("./"))
        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")
