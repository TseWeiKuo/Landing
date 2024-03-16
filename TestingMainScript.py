from scipy.stats import kendalltau
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from scipy.stats import ttest_ind
from sklearn.utils import resample
import pandas as pd

Landing_time_data_path = [#r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Control\TF&CT joint\Control_TFCT_Landing_time.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Control\TT joint\Control_TT_Landing_time.xlsx",
                          #r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Starved\TF&CT joint\Starved_TFCT_Landing_time.xlsx"]
                          r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Starved\TT joint\Starved_TT_Landing_time.xlsx"]
Landing_prob_data_path = [#r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Control\TF&CT joint\Control_TFCT_Landing_probability.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Control\TT joint\Control_TT_Landing_probability.xlsx",
                          #r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Starved\TF&CT joint\Starved_TFCT_Landing_probability.xlsx"]
                          r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Starved\TT joint\Starved_TT_Landing_probability.xlsx"]
group_name = ["Control-TT",
              # "Control-TT",
              "Starved-TT"]
              # "Starved-TT"]
trial = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
Trial_Num = 10
Fly_num = 34
TestLandingTime = True
# '#1f77b4',
colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
    '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173',
    '#5254a3', '#637939', '#8c6d31', '#8c6d31', '#bd9e39',
    '#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a',
    '#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6',
    '#ffff99', '#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3',
    '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3', '#8dd3c7',
    '#fccde5', '#bebada', '#fb8072', '#80b1d3', '#fdb462',
    '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5',
]

LandingTimeData = []
for i in range(len(Landing_time_data_path[0:1])):
    plt.subplot(2, 1, i+1)
    legend_label = []
    Mean = []
    y_errors = []
    Temp = pd.read_excel(Landing_time_data_path[i])
    for key in Temp.keys()[1:][:Trial_Num]:
        landingtemp = []
        n = 0
        for data in Temp[key]:
            if isinstance(data, np.floating):
                data = float(data)
            if type(data) is not str and (type(data) is float or type(data) is int):
                if data > -1:
                    landingtemp.append(data)
                    n += 1
        if n == 0:
            Mean.append(0)
        else:
            Mean.append(sum(landingtemp)/n)
        LandingTimeData.append(landingtemp)
print(LandingTimeData)
data = LandingTimeData
# Flatten the data for Kendall's Tau test
flat_data = [item for sublist in data for item in sublist]

# Create corresponding x-values (trial numbers)
x_values = np.concatenate([[i + 1] * len(trial) for i, trial in enumerate(data)])
print(flat_data)
print(x_values)
# Perform Kendall's Tau test
tau, p_value = kendalltau(x_values, flat_data)

# Output results
print(f"Kendall's Tau: {tau}")
print(f"P-value: {p_value}")

# Check significance at a 0.05 level
if p_value < 0.05:
    print("Reject the null hypothesis: There is a significant trend.")
else:
    print("Fail to reject the null hypothesis: No significant trend detected.")