import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from scipy.stats import ttest_ind
from sklearn.utils import resample
import pandas as pd

def calculate_mean_diff(data1, data2):
    return np.mean(data1) - np.mean(data2)
def calculate_median_diff(data1, data2):
    return np.median(data1) - np.median(data2)

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
if TestLandingTime:
    original_data = []
    o_temp_data = []
    LandingTimeAcrossExperiment = []
    for i in range(len(Landing_time_data_path[0:2])):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        o_temp_data = []
        for k in range(len(Temp)):
            landingtemp = []
            # print(Temp.iloc[k][1:][:Trial_Num])
            for data in Temp.iloc[k][1:][:Trial_Num]:
                if isinstance(data, np.floating):
                    data = float(data)
                if type(data) is not str and (type(data) is float or type(data) is int):
                    if data > -1:
                        landingtemp.append(data)
                        o_temp_data.append(data)
            LandingTimeData.append(landingtemp)
        original_data.append(o_temp_data)
        LandingTimeAcrossExperiment.append(LandingTimeData)
    Landing_Time_Mean = []
    Landing_Time_Error = []
    for ex in LandingTimeAcrossExperiment:
        LTM = []
        LTE = []
        for LTs in ex:
            if len(LTs) != 0:
                LTE.append(np.std(LTs) / np.sqrt(len(LTs)))
                LTM.append(np.mean(LTs))
        Landing_Time_Mean.append(LTM)
        Landing_Time_Error.append(LTE)
    sns.histplot(Landing_Time_Mean, bins=50, kde=True, color='skyblue', stat='count')
    plt.show()
    data1 = Landing_Time_Mean[0]
    data2 = Landing_Time_Mean[1]
else:
    LandingProbData = []
    for path in Landing_prob_data_path[0:2]:
        Temp = pd.read_excel(path)
        landingtemp = []
        for i in range(Fly_num):
            Landing = 0
            Flying = 0
            print(f"Fly {i + 1}")
            print(Temp.iloc[i][1:][:Trial_Num])
            for data in Temp.iloc[i][1:][:Trial_Num]:
                if isinstance(data, np.floating):
                    data = float(data)
                if type(data) is not str and (type(data) is float or type(data) is int):
                    if data == 1:
                        Landing += 1
                    if data == 0:
                        Flying += 1
            print(f"Landing: {Landing}")
            print(f"Flying: {Flying}")
            print("\n")
            if Landing + Flying != 0:
                landingtemp.append(Landing / (Landing + Flying))
        LandingProbData.append(landingtemp)
    sns.histplot(LandingProbData, bins=50, kde=True, color='skyblue', stat='count')
    plt.show()

    data1 = LandingProbData[0]
    data2 = LandingProbData[1]

# Define the number of bootstrap samples
num_bootstrap_samples = 10000

# Perform t-test on the original data



original_median_diff = calculate_median_diff(data1, data2)
original_mean_diff = calculate_mean_diff(data1, data2)

# Bootstrap resampling
bootstrap_mean_diffs = []
bootstrap_median_diffs = []
resample_data = np.concatenate((data1, data2))

for _ in range(num_bootstrap_samples):
    # Resample with replacement
    bootstrap_sample1 = resample(resample_data, n_samples=len(data1))
    bootstrap_sample2 = resample(resample_data, n_samples=len(data2))
    # print(bootstrap_sample1)

    # Perform t-test on the bootstrap samples
    bootstrap_median_diff = calculate_median_diff(bootstrap_sample1, bootstrap_sample2)
    bootstrap_mean_diff = calculate_mean_diff(bootstrap_sample1, bootstrap_sample2)

    bootstrap_mean_diffs.append(bootstrap_mean_diff)
    bootstrap_median_diffs.append(bootstrap_median_diff)

# Visualize the bootstrap t-statistic distribution
plt.figure(2)
plt.figure(figsize=(8, 6))
fig, axes = plt.subplots(2,1)
plt.subplot(2,1,1)
sns.histplot(bootstrap_mean_diffs, bins=50, kde=True, color='skyblue', stat='count')
plt.axvline(original_mean_diff, color='red', linestyle='dashed', linewidth=2, label='Original mean difference')
axes[0].legend()
#axes[0].legend(bbox_to_anchor=(1.1, 1.05))
plt.xlabel('Mean-Difference')
plt.subplot(2,1,2)
sns.histplot(bootstrap_median_diffs, bins=50, kde=True, color='skyblue', stat='count')
plt.axvline(original_median_diff, color='green',  linestyle='dashed', linewidth=2, label='Original median difference')
axes[1].legend()
#axes[1].legend(bbox_to_anchor=(1.1, 1.05))
plt.xlabel('Median-Difference')
fig.tight_layout()
Mean_diff_p_value = (np.sum(np.abs(bootstrap_mean_diffs) >= np.abs(original_mean_diff))) / (num_bootstrap_samples)
Median_diff_p_value = (np.sum(np.abs(bootstrap_median_diffs) >= np.abs(original_median_diff))) / (num_bootstrap_samples)

print(f"Difference in mean's P-value = {Mean_diff_p_value}")
print(f"Original mean diff = {original_mean_diff}")
print(f"Difference in median's P value = {Median_diff_p_value}")
print(f"Original median diff = {original_median_diff}")

#plt.title('Bootstrap mean and median difference Distribution', y=1)
plt.ylabel('Count')
plt.legend()
plt.savefig("Bootstrapping mean diff")

plt.show()