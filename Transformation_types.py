#!/usr/bin/env python3

from cv2 import (imread, imwrite, cvtColor,  COLOR_BGR2HSV,
                 medianBlur, bilateralFilter, BORDER_CONSTANT,
                 morphologyEx, MORPH_GRADIENT, blur, Canny,
                 COLOR_BGR2LAB)
from numpy import ones, uint8
from os import path


def get_lab(src: str, dst: str) -> None:
    """Used in medical imaging (provides better contrast)"""
    subdir = "Transformed"
    # lightness, green to red, blue to yellow
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_lab = cvtColor(img, COLOR_BGR2LAB)
    imwrite(f"{dst}/{subdir}/{filename}_lab.JPG", img_color_lab)


def get_hsv(src: str, dst: str) -> None:
    """Helps with color detection"""
    # hue saturation value
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_hsv = cvtColor(img, COLOR_BGR2HSV)
    imwrite(f"{dst}/{subdir}/{filename}_hsv.JPG", img_color_hsv)


def get_bilateral_filter(src: str, dst: str) -> None:
    """Reduces noise but keeps edges sharp"""
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    nimg = None
    img_bilateral_filter = bilateralFilter(img, nimg,
                                           sigmaColor=5*20, sigmaSpace=5*20,
                                           borderType=BORDER_CONSTANT)
    subdir = "Transformed"

    imwrite(f"{dst}/{subdir}/{filename}_bilateralfilter.JPG",
            img_bilateral_filter)
    # Used for denoising.
    # See, the texture on the surface is gone, but the edges are
    # still preserved.


def get_median_blurring_small_noise(src: str, dst: str) -> None:
    """Median filter replacing each pixel with the median value
    of its neighborhood (not average, good at removing
    isolated noise (salt-and-pepper))"""
    # ksize: aperture linear size; it must be odd and greater than 1,
    # for example: 3, 5, 7 ...
    # Aperture: The size of the kernel or neighborhood used in various
    # image processing operations.
    # 3 vs 5 - 3 looks at broader neighborhood, remove larger noise patterns
    # Removes salt and pepper effect - small noise
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_median_blur_small = medianBlur(img, 3)
    imwrite(f"{dst}/{subdir}/{filename}_medianblursmallnoise.JPG",
            img_median_blur_small)


def get_morphological_gradient(src: str, dst: str) -> None:
    """Edge detection technique that highlights the boundaries/contours
    of objects"""
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    kernel = ones((3, 3), uint8)
    img_morphological_gradient = morphologyEx(img, MORPH_GRADIENT, kernel)

    imwrite(f"{dst}/{subdir}/{filename}_morphologicalgradient.JPG",
            img_morphological_gradient)


def get_canny_edge(src: str, dst: str) -> None:
    """Highlights Object shapes and boundaries, Internal patterns
    and textures, Transitions between different regions,
    Fine details and patterns"""
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    low_threshold = 0
    ratio = 3
    kernel_size = 3

    img_blur = blur(img, (3, 3))
    detected_edges = Canny(img_blur, low_threshold, low_threshold*ratio,
                           kernel_size)
    mask = detected_edges != 0
    img_canny_edge = img * (mask[:, :, None].astype(img.dtype))
    imwrite(f"{dst}/{subdir}/{filename}_cannyedge.JPG",
            img_canny_edge)
