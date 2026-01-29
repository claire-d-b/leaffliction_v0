#!/usr/bin/env python3


from numpy import ndarray
from glob import glob
from os import path
from Transformation_types import (get_hsv,
                                  get_bilateral_filter,
                                  get_median_blurring_small_noise,
                                  get_morphological_gradient,
                                  get_canny_edge, get_lab)
from Histogram import (plot_multiple_images_histogram,
                       plot_single_image_histogram)
from stats import get_len
from matplotlib.pyplot import close, subplots, tight_layout, show
from cv2 import imread
from sys import argv
from pathlib import Path


def process_file(src: str, dst: str, category: str, augmented: bool,
                 single=False) -> ndarray | None:
    """Create histograms for transformed or augmented images.
    Write values of channels for those pictures in csv files."""

    ncategory = category
    if not dst.endswith('/'):
        dst = dst + '/'
    ndst = f"{dst}{ncategory}/*.JPG"

    files = glob(ndst)

    if single is True:
        plot_single_image_histogram(files, src, dst,
                                    ndst, ncategory,
                                    augmented)
    else:
        plot_multiple_images_histogram(files, src, dst,
                                       ndst, ncategory,
                                       augmented)
    return files


def process_input_transformation(src=None, dst=None, option=None,
                                 openImage=True, single=False,
                                 title=None) -> None:
    """Transforms source image if src is a file, and print that image's
    variations. Transform multiple images in src folder is src is a folder."""
    if not dst:
        dst = src
    img = None
    folder = src

    if src and path.isfile(src):
        pattern = folder
        ndst = f"{Path(pattern).parent.parent}/Transformed/"

        dst = f"{Path(src).parent.parent}"

        get_lab(src, dst)
        get_hsv(src, dst)
        get_morphological_gradient(src, dst)
        get_bilateral_filter(src, dst)
        get_median_blurring_small_noise(src, dst)
        get_canny_edge(src, dst)

        img = process_file(src, dst=ndst, category="Transformed",
                           augmented=False, single=single)
        if openImage is True:
            image_paths = ("_lab.JPG", "_hsv.JPG",
                           "_morphologicalgradient.JPG",
                           "_bilateralfilter.JPG",
                           "_medianblursmallnoise.JPG",
                           "_cannyedge.JPG")
            complete_paths = []
            for ipath in image_paths:
                filepath = Path(pattern).parent
                filename = Path(pattern).stem

                filepath = f"{Path(pattern).parent.parent}/Transformed/"
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
        pattern = f"{folder}Base/*.JPG"
        img = glob(pattern)

        ndst = f"{folder}/"
        if img:
            print(f"Found {get_len(img)} files matching pattern: {pattern}")
            for i, image in enumerate(img):

                if dst.endswith('/'):
                    dst = dst.rstrip('/')

                get_lab(image, dst)
                get_hsv(image, dst)
                get_morphological_gradient(image, dst)
                get_bilateral_filter(image, dst)
                get_median_blurring_small_noise(image, dst)
                get_canny_edge(image, dst)
            process_file(img, dst=dst, category="Transformed",
                         augmented=False, single=single)

        else:
            print(f"No files found matching pattern: {src}")


if __name__ == "__main__":
    try:
        if get_len(argv) == 2:
            process_input_transformation(src=argv[1].removeprefix("./"))
        else:
            print("Unknown command. Please type ./Leaffliction.py \
--help to display available commands.")

    except AssertionError as error:
        print(f"{error}")
