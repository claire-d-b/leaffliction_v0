#!/usr/bin/env python3

from pandas import DataFrame
from math import fabs


def get_len(lst: list):
    i = 0
    for item in lst:
        i += 1
    return i


def sort_list(sort_list: list):
    n = get_len(sort_list)
    for i in range(n):
        # Find the minimum element in the unsorted part of the list
        min_index = i
        for j in range(i + 1, n):
            if sort_list[j] < sort_list[min_index]:
                min_index = j
        # Swap the found minimum element with the first element
        sort_list[i], sort_list[min_index] = sort_list[min_index], sort_list[i]

    return sort_list


def nearest(number: float, lst: list) -> float:
    distance = 0
    mindistance = float('inf')
    index = 0
    for i in range(get_len(lst)):
        distance = fabs(lst[i] - number)
        if distance < mindistance:
            mindistance = distance
            index = i
    return lst[index]


def get_mean(largs: any) -> float:
    ret = 0
    try:
        get_len(largs)
        for arg in largs:
            ret += arg
        ret = ret / get_len(largs)
        return ret
    except Exception:
        print("ERROR")


def get_median(largs: any) -> float:
    ret = 0
    try:
        get_len(largs)
        largs = sort_list(largs)

        if get_len(largs) % 2:
            index = int(get_len(largs) / 2)
            ret = largs[index]

        else:
            index = int(get_len(largs) / 2)
            ret = (largs[index - 1] +
                   largs[index]) / 2
        return ret
    except Exception as e:
        print(f"ERROR:{e}")


def get_variance(largs: any) -> float:
    try:
        get_len(largs)
        # Calculate the Mean:
        mean = 0
        for arg in largs:
            mean += arg
        mean = mean / get_len(largs)
        # Calculate Each Deviation from the Mean and
        # Square it:
        deviation_lst = []
        for arg in largs:
            deviation_lst.append((arg - mean) ** 2)
        # Calculate the Mean of These Squared Deviations:
        sd_mean = 0

        for item in deviation_lst:
            sd_mean += item
        sd_mean = sd_mean / get_len(deviation_lst)
        return sd_mean
    except Exception as error:
        raise AssertionError(f"Error: {error}")


def get_standard_deviation(largs: any) -> float:
    # The standard deviation is a measure of
    # the amount of variation or dispersion in a set
    # of values. It quantifies how much the values
    # in a dataset deviate from the mean (average)
    # of the dataset.
    # Variance is a measure of the dispersion or
    # spread of a set of data points.
    # It quantifies how much the values in a dataset
    # differ from the mean of the dataset. """
    try:
        get_len(largs)
        # Calculate the Mean:
        mean = 0
        for arg in largs:
            mean += arg
        mean = mean / get_len(largs)
        # Calculate Each Deviation from the Mean and
        # Square it:
        deviation_lst = []
        for arg in largs:
            deviation_lst.append((arg - mean) ** 2)
        # Calculate the Mean of These Squared Deviations:
        sd_mean = 0

        for item in deviation_lst:
            sd_mean += item
        sd_mean = sd_mean / get_len(deviation_lst)
        return sd_mean ** 0.5
    except Exception as error:
        raise AssertionError(f"Error: {error}")


def get_quartile(largs: any) -> float:
    try:
        get_len(largs)
        largs = sort_list(largs)

        # identify quartile position
        q1 = float((get_len(largs) + 1) / 4)

        q3 = float((3 * (get_len(largs) + 1)) / 4)
        # Q1: Interpolate between values:
        if not isinstance(q1, int):
            pos1, pos2 = largs[int(q1)], largs[int(q1) - 1]
            q1 = float(pos2 + (pos1 - pos2) * 0.75)

        else:
            q1 = largs[q1]
        # Q3: Interpolate between values:
        if not isinstance(q3, int):
            pos1, pos2 = largs[int(q3)], largs[int(q3) - 1]
            q3 = float(pos2 + (pos1 - pos2) * 0.25)

        else:
            q3 = largs[q3]

        if get_len(largs) % 2:
            largs = [float(nearest(q1, largs)),
                     float(nearest(q3, largs))]
        else:
            largs = [float(q1), float(q3)]
        return largs

    except Exception as error:
        raise AssertionError(f"Error: {error}")


def get_min(df: DataFrame):
    nlst = sort_list(list(df))
    return nlst[0]


def get_max(df: DataFrame):
    nlst = sort_list(list(df))
    return nlst[get_len(nlst)-1]
