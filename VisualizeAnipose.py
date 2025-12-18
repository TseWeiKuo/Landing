import numpy as np
import math
import pandas as pd
from decimal import Decimal
import seaborn as sns
import matplotlib.pyplot as plt

"""
Takes function, t0, y0, stop time, steps array, and name of the questions as parameters.
"""
def euler_method(func, t0, y0, stop, steps, question):

    # Initialize table for y values
    data_points = dict()

    # Initialize time column [0, 0.1, 0.2 ...]
    data_points["time"] = [Decimal(str(i)[:3]) for i in np.linspace(t0, stop, int((stop - t0) / 0.1) + 1)]

    # Iterate through different steps
    for h in steps:

        # Initialize column values for step h
        data_points[str(h)] = []

        # Calculate number of steps to take
        N = int((stop - t0) / h)

        # Initialize y as y0
        y = y0

        # Take steps to approximate y values
        for i in range(N+1):

            # Calculate next time point
            t = t0 + i * h

            # Calculate slope by plugging in the t and y to the function
            k = func(t, y)

            # Convert t to decimal to avoid floating point error in calculation.
            t = Decimal(str(t)[:6])

            # Record y values when t is multiple of 0.1
            if t % Decimal("0.1") == 0:

                # Append the y values to corresponding h (step) column
                data_points[str(h)].append(round(y, 10))

            # update y value to y_i+1
            y = y + h * k

    # Convert data table to csv file
    data_points = pd.DataFrame(data_points)
    data_points.to_csv(question + "DataPoints.csv", index=False)

    # Create plot for h = 0.001 approximation
    sns.lineplot(x=data_points["time"], y=data_points["0.001"], linewidth=5)
    plt.grid()
    plt.ylabel("y")
    plt.savefig(question + "DataPoint.png")
    plt.show()


# Initializing question a
question_a = lambda t, y: math.sin(2*math.pi*t) + (t**2)*y
a_t0 = 0
a_y0 = 1
a_tstop = 1

# Initializing question b
question_b = lambda t, y: 3 + 2*math.exp(t**2) - 5*y
b_t0 = 1
b_y0 = 4
b_tstop = 2

# Set steps
steps = [0.1,  0.01, 0.001]

# Question a
euler_method(question_a, a_t0, a_y0, a_tstop, steps, "A")

# Question b
euler_method(question_b, b_t0, b_y0, b_tstop, steps, "B")

