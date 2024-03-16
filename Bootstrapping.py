import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
import numpy as np
import matplotlib.patches as mpatches
# Apply the default theme

def Perform_t_test(group1, group2):
    return

Landing_time_data_path = [r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Control\TF&CT joint\Control_TFCT_Landing_time.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Control\TT joint\Control_TT_Landing_time.xlsx",
                          #r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Starved\TF&CT joint\Starved_TFCT_Landing_time.xlsx"]
                          r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\StarvedFlyExperiment\Starved\TT joint\Starved_TT_Landing_time.xlsx"]

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
# trial = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
group_name = [# "Control-CT",
              "Coxa-Trochanter",
              # "Starved-CT",
              "Tibia-Tarsus"]
Trial_Num = 10
LandingTimeAcrossExperiment = []
for i in range(len(Landing_time_data_path[0:2])):
    LandingTimeData = []
    Temp = pd.read_excel(Landing_time_data_path[i])
    # print(Temp.to_string)
    for k in range(len(Temp)):
        landingtemp = []
        for data in Temp.iloc[k][1:][:Trial_Num]:
            if isinstance(data, np.floating):
                data = float(data)
            if type(data) is not str and (type(data) is float or type(data) is int):
                if data > -1:
                    landingtemp.append(data)
        LandingTimeData.append(landingtemp)
    LandingTimeAcrossExperiment.append(LandingTimeData)
print(LandingTimeAcrossExperiment)
Landing_Time_Mean = []
Landing_Time_Error = []
for ex in LandingTimeAcrossExperiment:
    LTM = []
    LTE = []
    for LTs in ex:
        LTE.append(1.96 * (np.std(LTs) / np.sqrt(len(LTs))))
        LTM.append(np.mean(LTs))
    Landing_Time_Mean.append(LTM)
    Landing_Time_Error.append(LTE)
print(Landing_Time_Mean)
#print(Landing_Time_Error)
mean_colors = ['#1f77b4', '#ff7f0e']
plt.figure(figsize=(8, 6))
for i, Group_Data in enumerate(LandingTimeAcrossExperiment, start=1):
    plt.subplot(1, 2, i)
    # Plot stripplot-like points for individual flies
    for j, individual_fly in enumerate(Group_Data):
        sns.stripplot(y=individual_fly, jitter=0.2, marker='o', size=8, alpha=0.4, color=colors[j])

    # Plot mean with error bars

    #plt.errorbar(x=x_means, y=Landing_Time_Mean[i - 1], yerr=Landing_Time_Error[i - 1], fmt="none", color='gray',capsize=5)
    sns.stripplot(y=Landing_Time_Mean[i - 1], jitter=0.2, marker='s', alpha=0.7, size=8, color=mean_colors[i-1])


    # plt.title(f'Strip Plot - Element {i}')
    plt.tick_params(axis='y', labelsize=15)
    plt.xlabel(group_name[i - 1], fontsize=15)
    plt.ylabel('Landing latency (# of frames)', fontsize=15)
    plt.ylim(0, 750)
    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 10})

plt.tight_layout()
plt.savefig("Landind time across fly clustered")
plt.show()




