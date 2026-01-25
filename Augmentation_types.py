#!/usr/bin/env python3

from cv2 import (imread, imwrite, resize, INTER_CUBIC,
                 getRotationMatrix2D, warpAffine, convertScaleAbs,
                 flip, getAffineTransform, getPerspectiveTransform,
                 warpPerspective)
from numpy import float32
from os import path


# Those functions are augmentations techniques that increase the
# number of images in a particular dataset. It creates more variations,
# but do not especially highlight a specific pattern / disease / value
# of a feature. It provides way more visible gaps in features values
# when used in a pairplot. But those gaps do not represent actual images
# diversity, it is much better to use real images and transform them.


def get_contrast(src: str, dst: str):
    subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    alpha = 2.0
    # 1-3
    beta = 50
    # 0-100
    img_contrast = convertScaleAbs(img, alpha=alpha, beta=beta)

    imwrite(f"{dst}/{subdir}/{filename}_contrast.JPG", img_contrast)
    # but we wanted to show you how to access the pixels:

    # for y in range(image.shape[0]):
    #     for x in range(image.shape[1]):
    #         for c in range(image.shape[2]):
    #             new_image[y,x,c] = clip(alpha*image[y,x,c] + beta, 0, 255)


def get_scale_zoom(src: str, dst: str):
    subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    height, width = img.shape[:2]
    img_zoomed = resize(img, (width*2, height*2), interpolation=INTER_CUBIC)
    imwrite(f"{dst}/{subdir}/{filename}_scalezoom.JPG", img_zoomed)


def get_horizontal_flip(src: str, dst: str):
    subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_horizontal_flip = flip(img, 1)
    imwrite(f"{dst}/{subdir}/{filename}_horizontalflip.JPG",
            img_horizontal_flip)


def get_rotate(src: str, dst: str):
    subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    height, width = img.shape[:2]
    rotated = getRotationMatrix2D(((height-1)/2.0, (width-1)/2.0), 90, 1)
    img_rotated = warpAffine(img, rotated, (height, width))
    imwrite(f"{dst}/{subdir}/{filename}_rotation.JPG", img_rotated)


def get_affine_transformation(src: str, dst: str) -> None:
    subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    rows, cols, ch = img.shape

    pts1 = float32([[50, 50], [200, 50], [50, 200]])
    pts2 = float32([[10, 100], [200, 50], [100, 250]])

    M = getAffineTransform(pts1, pts2)

    image = warpAffine(img, M, (cols, rows))
    imwrite(f"{dst}/{subdir}/{filename}_affinetransformation.JPG", image)


def get_perspective_transformation(src: str, dst: str) -> None:
    subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    rows, cols, ch = img.shape

    # HG,HD,BD,BG
    pts1 = float32([[cols*1/12, rows*1/12], [cols*11/12, rows*1/12],
                    [cols*11/12, rows*11/12], [cols*1/12, rows*11/12]])

    output_width = cols
    output_height = rows

    pts2 = float32([
        [0, 0],
        [output_width, 0],
        [output_width, output_height],
        [0, output_height]
    ])

    M = getPerspectiveTransform(pts1, pts2)
    image = warpPerspective(img, M, (output_width, output_height))
    imwrite(f"{dst}/{subdir}/{filename}_perspectivetransformation.JPG", image)
