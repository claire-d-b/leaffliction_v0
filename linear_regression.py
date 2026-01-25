#!/usr/bin/env python3

def minimize_cost(m: int, theta_0: float, theta_1: float, real_value: float,
                  real_class: float, learning_rate: float) -> tuple:
    """Test bias values - y-interceipt - and update coefficient, taking
    the smallest square error and return corresponding w and b"""
    limit = float("inf")
    w = 0.0
    b = 0.0

    minimum = int(- 1 / learning_rate)
    maximum = int(1 / learning_rate)

    for i in range(minimum, maximum, 1):
        theta_0 = float(i / ((2 * m) / learning_rate))
        # y = mx + b -> y - b = mx -> m = (y - b) / x

        # If you are predicting the score from the class, then
        # class is x, and score is y.
        # The thing you are trying to predict is y.
        # The thing you already know or control is x.
        # And here we know the class.
        theta_1 = (real_value - theta_0) / real_class

        se = ((theta_1 * real_class + theta_0) -
              real_value) ** 2

        if se < limit:

            limit = se
            b = theta_0
            w = theta_1

    return w, b, limit
