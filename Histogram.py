#!/usr/bin/env python3

from cv2 import (imread, cvtColor, COLOR_BGR2HLS, COLOR_BGR2HSV, calcHist,
                 split, COLOR_BGR2LAB)
from matplotlib.pyplot import (legend, close, title, xlabel, ylabel, savefig,
                               ylim, subplots)
from pathlib import Path
from numpy import ndarray
from os import path
from pandas import DataFrame, concat, read_csv
from utils import load
import glob
from Shared_variables import chosen_category


# Helper to calculate histogram
# Un histogramme : **un array de 256 valeurs**
# qui compte combien de pixels ont chaque intensité.
# Intensité 0   : 50 pixels
# Intensité 1   : 45 pixels
# ...
# Intensité 255 : 120 pixels
def calc_hist(channel):
    return calcHist([channel], [0], None, [256], [0, 256])


def get_additional_values(img: ndarray) -> tuple:
    # Tuple is an immutable ordered collection of items.
    # Convert to HLS and HSV color spaces
    hls_img = cvtColor(img, COLOR_BGR2HLS)
    hsv_img = cvtColor(img, COLOR_BGR2HSV)

    # Split channels
    h_hls, l, s_hls = split(hls_img)  # HLS channels
    h_hsv, s_hsv, v = split(hsv_img)  # HSV channels

    return (l, h_hls, s_hls, v)


def plot_multiple_images_histogram(image_files, src, dst, ndst, category,
                                   augmented):
    """Create averaged histograms for several attributes of multiple images
    like brightness or blue channel. Save those attributes' values into csv
    files to be used by our model to predict."""
    fig, axs = subplots()

    # Initialize histogram accumulators
    (r_hist_sum, g_hist_sum, b_hist_sum, l_hist_sum, h_hist_sum, s_hist_sum,
     v_hist_sum) = None, None, None, None, None, None, None

    valid_images = 0

    for file in image_files:
        img = imread(file)

        if img is None:
            # print(f"Warning: Could not read image {file} because \
            #        of incorrect format (.csv)")
            continue
        else:
            valid_images += 1

        height, width = img.shape[:2]
        total_pixels = width * height

        # Split BGR channels
        b, g, r = split(img)

        # Convert to LAB color space
        lab_img = cvtColor(img, COLOR_BGR2LAB)
        # Ligthness + blue-yellow and green-magenta
        # = colors that cancel each other
        L, A, B = split(lab_img)

        # A channel = Green-Magenta axis
        # B channel = Blue-Yellow axis

        # Get additional color space channels
        l, h_hls, s_hls, v = get_additional_values(img)

        # Calculate histograms and normalize
        r_hist = calc_hist(r) / total_pixels * 100
        g_hist = calc_hist(g) / total_pixels * 100
        b_hist = calc_hist(b) / total_pixels * 100

        A_hist = calc_hist(A) / total_pixels * 100
        B_hist = calc_hist(B) / total_pixels * 100

        l_hist = calc_hist(l) / total_pixels * 100
        h_hist = calc_hist(h_hls) / total_pixels * 100
        s_hist = calc_hist(s_hls) / total_pixels * 100
        v_hist = calc_hist(v) / total_pixels * 100

        # Accumulate histograms
        if r_hist_sum is None:
            r_hist_sum = r_hist
            g_hist_sum = g_hist
            b_hist_sum = b_hist
            A_hist_sum = A_hist
            B_hist_sum = B_hist
            l_hist_sum = l_hist
            h_hist_sum = h_hist
            s_hist_sum = s_hist
            v_hist_sum = v_hist
        else:
            r_hist_sum += r_hist
            g_hist_sum += g_hist
            b_hist_sum += b_hist
            A_hist_sum += A_hist
            B_hist_sum += B_hist
            l_hist_sum += l_hist
            h_hist_sum += h_hist
            s_hist_sum += s_hist
            v_hist_sum += v_hist

        if valid_images == 0:
            return

        # Average the histograms
        r_hist_avg = r_hist_sum / valid_images
        g_hist_avg = g_hist_sum / valid_images
        b_hist_avg = b_hist_sum / valid_images

        A_hist_avg = A_hist_sum / valid_images
        B_hist_avg = B_hist_sum / valid_images

        l_hist_avg = l_hist_sum / valid_images
        h_hist_avg = h_hist_sum / valid_images
        s_hist_avg = s_hist_sum / valid_images
        v_hist_avg = v_hist_sum / valid_images

        if category == "Transformed" or category == "Augmented" or \
           category == "Base":

            src = file
            nsrc = path.basename(src)
            dst = f"{dst}"

            file_path = file

            name_without_ext = Path(file_path).stem  # "image (263)_hsv"
            print("name", file)
            # Split from the right, limiting to 1 split
            parts = name_without_ext.rsplit('_', 1)
            # parts = ["image (263)", "hsv"]

            # base_name = parts[0]  # "image (263)"
            modif = parts[1]  # "hsv"
            dstname = f"{dst}{path.splitext(path.basename(nsrc))[0]}_{modif}"

            VALID_CATEGORIES = ["Grape_Black_rot", "Grape_Esca",
                            "Grape_healthy", "Grape_spot"] if chosen_category == "Grape" else \
                            ["Apple_Black_rot", "Apple_healthy",
                            "Apple_rust", "Apple_scab"]

            # Chercher la vraie catégorie
            extracted_category = None
            for cat in VALID_CATEGORIES:
                if cat in file:
                    extracted_category = cat
                    break
            dictionary = dict({
                            "Subname": f"{Path(dstname).name.split('_')[0]}_\
{Path(dstname).parts[1]}_{extracted_category}",
                            "Name": f"{Path(dstname).name.split('_')[0]}_\
{Path(dstname).parts[1]}_{'_'.join(Path(dstname).name.split('_')[1:])}",
                            "Category": f"{extracted_category}",
                            "Modification": f"\
{'_'.join(Path(dstname).name.split('_')[1:])}",
                            "Red": r_hist_avg.flatten(),
                            "Green": g_hist_avg.flatten(),
                            "Blue": b_hist_avg.flatten(),
                            "Blue_Yellow": A_hist_avg.flatten(),
                            "Green_Magenta": B_hist_avg.flatten(),
                            "Lightness": l_hist_avg.flatten(),
                            "Hue": h_hist_avg.flatten(),
                            "Saturation": s_hist_avg.flatten(),
                            "Value": v_hist_avg.flatten()})
            ndf = DataFrame(dictionary)

            ndst = Path(dst).parent

            print("etx", extracted_category)

            if extracted_category:

                if path.exists(f'{dst}{Path(dstname).parts[1]}_\
{category}_features.csv'):
                    ndf.to_csv(f'{dst}{Path(dstname).parts[1]}_\
{category}_features.csv', mode='a', header=False)
                else:
                    ndf.to_csv(f'{dst}{Path(dstname).parts[1]}_\
{category}_features.csv', mode='w', index=True)

                newdf = load(f"{dst}{Path(dstname).parts[1]}_\
{category}_features.csv")
                nndf = newdf.groupby(['Subname', 'Name', 'Category',
                                    'Modification']).median(numeric_only=True)
                nndf.to_csv(f"{dst}{Path(dstname).parts[1]}_{category}_\
features_test.csv", mode='w')

                if category == "Transformed":
                    pattern = f"**/*{Path(dstname).parts[1]}_Transformed_\
features_test.csv"

                    csv_files = glob.glob(pattern, recursive=True)

                    # Combine files with only one header
                    dfs = []
                    for i, file in enumerate(csv_files):
                        try:
                            if i == 0:
                                # First file: keep header
                                df = read_csv(file)
                            else:
                                # Subsequent files: skip header (first row)
                                df = read_csv(file, skiprows=1, header=None)
                                # Use column names from the first dataframe
                                df.columns = dfs[0].columns

                            dfs.append(df)
                        except Exception as err:
                            print(f"warning: {err}")
                            continue

                    combined_df = concat(dfs, ignore_index=True)
                    test_df = combined_df.copy()
                    file = Path(f"{Path(dstname).parts[1]}")

                    if file.exists():
                        test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="a", header=False)
                        test_df.to_csv(f"features_{Path(dstname).parts[1]}_test\
.csv", mode="a", header=False, index=False)
                    else:
                        test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="w", header=True)
                        test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="w", header=True, index=False)

            if valid_images:
                # Plot averaged histograms
                axs.plot(b_hist_avg, color='b', label='Blue')
                axs.plot(A_hist_avg, color='yellow', label='Blue-Yellow')
                axs.plot(g_hist_avg, color='g', label='Green')
                axs.plot(B_hist_avg, color='fuchsia', label='Green-magenta')
                axs.plot(h_hist_avg, color='purple', label='Hue')
                axs.plot(l_hist_avg, color='gray', label='Lightness')
                axs.plot(r_hist_avg, color='r', label='Red')
                axs.plot(s_hist_avg, color='cyan', label='Saturation')
                axs.plot(v_hist_avg, color='orange', label='Value')

                title(f'Average Color Histogram - {valid_images} Images')
                xlabel('Pixel Intensity')
                ylabel('Average Proportion of pixels')
                ylim(0, 10)

                handles, labels = axs.get_legend_handles_labels()
                unique = dict(zip(labels, handles))
                legend(unique.values(), unique.keys())

                output_path = f"{ndst}_color_histogram_multiple.png"
                savefig(output_path)

    axs.clear()
    fig.clf()
    close(fig)


def plot_single_image_histogram(image_files, src, dst, ndst, category,
                                augmented):
    """Create averaged histograms for several attributes of a single image
    like brightness or blue channel. Save those attributes' values into csv
    files to be used by our model to predict."""
    fig, axs = subplots()

    # Initialize histogram accumulators
    (r_hist_sum, g_hist_sum, b_hist_sum, l_hist_sum, h_hist_sum, s_hist_sum,
     v_hist_sum) = None, None, None, None, None, None, None

    valid_images = 0

    for file in image_files:
        img = imread(file)

        if img is None:
            # print(f"Warning: Could not read image {file} because \
            #        of incorrect format (.csv)")
            continue
        else:
            valid_images += 1

        height, width = img.shape[:2]
        total_pixels = width * height

        # Split BGR channels
        b, g, r = split(img)

        # Convert to LAB color space
        lab_img = cvtColor(img, COLOR_BGR2LAB)
        # Ligthness + blue-yellow and green-magenta
        # = colors that cancel each other
        L, A, B = split(lab_img)

        # A channel = Green-Magenta axis
        # B channel = Blue-Yellow axis

        # Get additional color space channels
        l, h_hls, s_hls, v = get_additional_values(img)

        # Calculate histograms and normalize
        r_hist = calc_hist(r) / total_pixels * 100
        g_hist = calc_hist(g) / total_pixels * 100
        b_hist = calc_hist(b) / total_pixels * 100

        A_hist = calc_hist(A) / total_pixels * 100
        B_hist = calc_hist(B) / total_pixels * 100

        l_hist = calc_hist(l) / total_pixels * 100
        h_hist = calc_hist(h_hls) / total_pixels * 100
        s_hist = calc_hist(s_hls) / total_pixels * 100
        v_hist = calc_hist(v) / total_pixels * 100

        # Accumulate histograms
        if r_hist_sum is None:
            r_hist_sum = r_hist
            g_hist_sum = g_hist
            b_hist_sum = b_hist
            A_hist_sum = A_hist
            B_hist_sum = B_hist
            l_hist_sum = l_hist
            h_hist_sum = h_hist
            s_hist_sum = s_hist
            v_hist_sum = v_hist
        else:
            r_hist_sum += r_hist
            g_hist_sum += g_hist
            b_hist_sum += b_hist
            A_hist_sum += A_hist
            B_hist_sum += B_hist
            l_hist_sum += l_hist
            h_hist_sum += h_hist
            s_hist_sum += s_hist
            v_hist_sum += v_hist

        if valid_images == 0:
            return

        # Average the histograms
        r_hist_avg = r_hist_sum / valid_images
        g_hist_avg = g_hist_sum / valid_images
        b_hist_avg = b_hist_sum / valid_images

        A_hist_avg = A_hist_sum / valid_images
        B_hist_avg = B_hist_sum / valid_images

        l_hist_avg = l_hist_sum / valid_images
        h_hist_avg = h_hist_sum / valid_images
        s_hist_avg = s_hist_sum / valid_images
        v_hist_avg = v_hist_sum / valid_images

        src = file
        nsrc = path.basename(src)
        dst = f"{dst}"

        name_without_ext = Path(file).stem

        # If you know modification always has exactly 2 parts
        # (lab_perspectivetransformation)
        # Split from the right with max 2 splits
        parts = name_without_ext.rsplit('_', 2)
        # parts = ['Grape_Black_rot2', 'lab', 'perspectivetransformation']

        # Join the last 2 parts
        modif = '_'.join(parts[-2:])

        dstname = f"{dst}{path.splitext(path.basename(nsrc))[0]}"

        VALID_CATEGORIES = ["Grape_Black_rot", "Grape_Esca",
                            "Grape_healthy", "Grape_spot"] if chosen_category == "Grape" else \
                            ["Apple_Black_rot", "Apple_healthy",
                            "Apple_rust", "Apple_scab"]

        # Chercher la vraie catégorie
        extracted_category = None
        for cat in VALID_CATEGORIES:
            if cat in file:
                extracted_category = cat
                break
        dictionary = dict({
                        "Subname": f"{Path(dstname).name.split('_')[0]}_\
{Path(dstname).parts[1]}_{extracted_category}",
                        "Name": f"{Path(dstname).name.split('_')[0]}_\
{Path(dstname).parts[1]}",
                        "Category": f"{extracted_category}",
                        "Modification": f"{modif}",
                        "Red": r_hist_avg.flatten(),
                        "Green": g_hist_avg.flatten(),
                        "Blue": b_hist_avg.flatten(),
                        "Blue_Yellow": A_hist_avg.flatten(),
                        "Green_Magenta": B_hist_avg.flatten(),
                        "Lightness": l_hist_avg.flatten(),
                        "Hue": h_hist_avg.flatten(),
                        "Saturation": s_hist_avg.flatten(),
                        "Value": v_hist_avg.flatten()})
        ndf = DataFrame(dictionary)

        if extracted_category:
            ndst = Path(dst).parent

            if path.exists(f'{dst}{Path(dstname).parts[1]}_\
{extracted_category}_features.csv'):
                ndf.to_csv(f'{dst}{Path(dstname).parts[1]}_\
{extracted_category}_features.csv', mode='a', header=False)
            else:
                ndf.to_csv(f'{dst}{Path(dstname).parts[1]}_\
{extracted_category}_features.csv', mode='w', index=True)

            newdf = load(f"{dst}{Path(dstname).parts[1]}_\
{extracted_category}_features.csv")
            nndf = newdf.groupby(['Subname', 'Name', 'Category',
                                'Modification']).median(numeric_only=True)
            nndf.to_csv(f"{dst}{Path(dstname).parts[1]}_{extracted_category}_\
features_test.csv", mode='w')

            if category == "Transformed":
                pattern = f"**/*{Path(dstname).parts[1]}_Transformed_\
features_test.csv"

                csv_files = glob.glob(pattern, recursive=True)

                # Combine files with only one header
                dfs = []
                for i, file in enumerate(csv_files):
                    try:
                        if i == 0:
                            # First file: keep header
                            df = read_csv(file)
                        else:
                            # Subsequent files: skip header (first row)
                            df = read_csv(file, skiprows=1, header=None)
                            # Use column names from the first dataframe
                            df.columns = dfs[0].columns

                        dfs.append(df)
                    except Exception as e:
                        print(f"warning: {e}")
                        continue

                combined_df = concat(dfs, ignore_index=True)
                test_df = combined_df.copy()
                file = Path(f"{Path(dstname).parts[1]}")

                if file.exists():
                    test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="a", header=False)
                    test_df.to_csv(f"features_{Path(dstname).parts[1]}_test\
.csv", mode="a", header=False, index=False)
                else:
                    test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="w", header=True)
                    test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="w", header=True, index=False)

            if valid_images:
                # Plot averaged histograms
                axs.plot(b_hist_avg, color='b', label='Blue')
                axs.plot(A_hist_avg, color='yellow', label='Blue-Yellow')
                axs.plot(g_hist_avg, color='g', label='Green')
                axs.plot(B_hist_avg, color='fuchsia', label='Green-magenta')
                axs.plot(h_hist_avg, color='purple', label='Hue')
                axs.plot(l_hist_avg, color='gray', label='Lightness')
                axs.plot(r_hist_avg, color='r', label='Red')
                axs.plot(s_hist_avg, color='cyan', label='Saturation')
                axs.plot(v_hist_avg, color='orange', label='Value')

                title(f'Average Color Histogram - {valid_images} Images')
                xlabel('Pixel Intensity')
                ylabel('Average Proportion of pixels')
                ylim(0, 10)

                handles, labels = axs.get_legend_handles_labels()
                unique = dict(zip(labels, handles))
                legend(unique.values(), unique.keys())

                output_path = f"{ndst}_color_histogram_multiple.png"
                savefig(output_path)

    axs.clear()
    fig.clf()
    close(fig)
