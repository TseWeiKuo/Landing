import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
import numpy as np
import matplotlib.patches as mpatches
# Apply the default theme

def CreateLandingProbAcrossTrial(Landing_prob_data_path):
    LandingProbData = []
    group_name = ["T2 TF (n=20)"]
    trial = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    for path in Landing_prob_data_path:
        Temp = pd.read_excel(path)
        landingtemp = []
        for key in Temp.keys()[1:]:
            Landing = 0
            Flying = 0
            for data in Temp[key]:
                if type(data) is not str and type(data) is not float:
                    if data == 1:
                        Landing += 1
                    if data == 0:
                        Flying += 1
            landingtemp.append(Landing / (Landing + Flying))
        LandingProbData.append(landingtemp)
    LandingProbData = np.asarray(LandingProbData)
    LandingProbData = np.transpose(LandingProbData)
    LandingProbData = pd.DataFrame(LandingProbData, columns=group_name)
    print(LandingProbData)

    plt.figure(figsize=(12, 9))
    LandingProbGraph = sns.lineplot(data=LandingProbData)
    LandingProbGraph.set_xticks(range(10))
    LandingProbGraph.set_xticklabels(trial)
    plt.legend(bbox_to_anchor=(0.95, 0.15))
    plt.xlabel("Trial")
    plt.ylabel("Landing probability")
    plt.savefig("Landing Probability")
    plt.show()
def CreateLandingProbAcrossFlies(Landing_prob_data_path):
    LandingProbData = []
    group_name = ["T2 TF (n=20)"]

    for path in Landing_prob_data_path:
        Temp = pd.read_excel(path)
        landingtemp = []
        for i in range(len(Temp)):
            Landing = 0
            Flying = 0
            for data in Temp.iloc[i][1:]:
                if type(data) is not str and type(data) is not float:
                    if data == 1:
                        Landing += 1
                    if data == 0:
                        Flying += 1
            landingtemp.append(Landing / (Landing + Flying))
        LandingProbData.append(landingtemp)
    plt.figure(figsize=(12, 9))
    g = sns.stripplot(LandingProbData)
    g.set_xticks(range(4))
    g.set_xticklabels(group_name)
    plt.ylabel("Landing Probability")
    plt.savefig("Landing Prob across fly")
    plt.show()
    return
def CreateLandingTimeAcrossTrial(Landing_time_data_path):
    LandingTimeData = []
    group_name = ["T2 FT 5s (n=30)", "T2 FT 10s (n=25)", "T2 FT 15s (n=25)", "T2 BC 15s (n=25)"]
    trial = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    error_value = []
    for path in Landing_time_data_path:
        Temp = pd.read_excel(path)
        landingtemp = []
        error_temp = []
        for key in Temp.keys()[1:]:
            n = 0
            Total_landing_time = 0
            good_data_point = []
            for data in Temp[key]:
                if data > -1:
                    Total_landing_time += data
                    good_data_point.append(data)
                    n += 1
            error_temp.append(st.stdev(good_data_point) / np.sqrt(len(good_data_point)))
            landingtemp.append(Total_landing_time / n)
        LandingTimeData.append(landingtemp)
        error_value.append(error_temp)

    LandingTimeData = np.asarray(LandingTimeData)
    LandingTimeData = np.transpose(LandingTimeData)
    LandingTimeData = pd.DataFrame(LandingTimeData, columns=group_name)
    print(LandingTimeData)
    plt.figure(figsize=(12, 9))
    marker = ['o', 'v', '<', '>']
    LandingTimeGraph = sns.lineplot(LandingTimeData, markers=marker)
    LandingTimeGraph.set_xticks(range(10))
    LandingTimeGraph.set_xticklabels(trial)
    plt.legend(bbox_to_anchor=(0.95, 0.15))
    plt.xlabel("Trial")
    plt.ylabel("Landing Time (# of frames)")
    plt.savefig("Landing Time")
    plt.show()
def CreateLandingTimeAcrossTrialStripplot(Landing_time_data_path):
    LandingTimeData = []
    group_name = ["T2 FT 5s (n=30)", "T2 FT 10s (n=25)", "T2 FT 15s (n=25)", "T2 BC 15s (n=25)"]
    trial = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    colors = ['blue', 'orange', 'green', 'red']
    legend_label = []
    plt.figure(figsize=(12, 9))
    for i in range(len(Landing_time_data_path)):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for key in Temp.keys()[1:]:
            # print(key)
            landingtemp = []
            for data in Temp[key]:
                print(data)
                if type(data) is not str and type(data) is not float:
                    if data > -1:
                        landingtemp.append(data)
            LandingTimeData.append(landingtemp)
        legend_label.append(mpatches.Patch(color=colors[i], label=group_name[i]))

        g = sns.stripplot(LandingTimeData, color=colors[i], linewidth=0.5, size=7)
        g.legend(handles=legend_label, bbox_to_anchor=(0.9, 1))
        g.set_xticks(range(10))
        g.set_xticklabels(trial)

    plt.ylabel("Landing time (# of frames)")
    plt.savefig("Landing time across trial strip plot")
    plt.show()
def CreateLandingTimeAcrossFlyStripplot(Landing_time_data_path):
    legend_label = []
    plt.figure(figsize=(12, 9))
    LandingTimeAcrossExperiment = []
    for i in range(len(Landing_time_data_path)):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for k in range(len(Temp)):
            landingtemp = []
            for data in Temp.iloc[k][1:]:
                if type(data) is not str and type(data) is not float:
                    if data > -1:
                        landingtemp.append(data)
            LandingTimeData.append(landingtemp)
        LandingTimeAcrossExperiment.append(LandingTimeData)
    print(LandingTimeAcrossExperiment)
    # LandingTimeAcrossExperiment = np.asarray(LandingTimeAcrossExperiment)

    data = LandingTimeAcrossExperiment

    # Create a strip plot for each sublist of the sublist with different colors in each subplot
    plt.figure(figsize=(15, 8))
    for i, element_data in enumerate(data, start=1):
        plt.subplot(2, 2, i)
        for j, sublist in enumerate(element_data, start=1):
            sns.stripplot(y=sublist, jitter=True, marker='o', alpha=0.7)

        # plt.title(f'Strip Plot - Element {i}')
        print(i)
        plt.xlabel(group_name[i - 1])
        plt.ylabel('Landing time (# of frames)')
        plt.ylim(0, 450)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 10})

    plt.tight_layout()
    plt.savefig("Landind time across fly clustered")
    plt.show()


Landing_prob_data_path = [r"C:\Users\agrawal-admin\Desktop\DataFolder\Sorted_Data\Fly_conditioning\10s\T2\TF joint\Landing Prob and Nan type.xlsx"]
Landing_time_data_path = [r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\Sorted_Data\Fly_conditioning\5s\T2\T2_5S_Landing_time.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\Sorted_Data\Fly_conditioning\10s\T2\T2 10S Landing time.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\Sorted_Data\Fly_conditioning\15s\T2\FT joint\Landing time filtered.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\Sorted_Data\Fly_conditioning\15s\T2\FT joint\T2 15S Landing time.xlsx",
                          r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\Sorted_Data\Fly_conditioning\15s\T2\BC joint\Landing time.xlsx"]


group_name = ["T2 FT 5s (n=30)", "T2 FT 10s (n=25)", "T2 FT 15s (n=25)", "T2 BC 15s (n=25)"]
trial = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
    '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173',
    '#5254a3', '#637939', '#8c6d31', '#8c6d31', '#bd9e39',
]


CreateLandingProbAcrossTrial(Landing_prob_data_path)


"""
legend_label = []
plt.figure(figsize=(15, 8))
LandingTimeAcrossExperiment = []
for i in range(len(Landing_time_data_path)):
    plt.subplot(2, 2, i+1)
    LandingTimeData = []
    Temp = pd.read_excel(Landing_time_data_path[i])
    fly_num = [i for i in range(1, len(Temp) + 1)]
    for k in range(len(Temp)):
        landingtemp = []
        for data in Temp.iloc[k][1:]:
            if type(data) is not str and type(data) is not float:
                if data > -1:
                    landingtemp.append(data)
        LandingTimeData.append(landingtemp)
    LandingTimeAcrossExperiment.append(LandingTimeData)
    g = sns.stripplot(LandingTimeData, color=colors[i])
    g.set_xticklabels(fly_num)
    plt.title(group_name[i])
    plt.ylim(0, 450)
plt.ylabel("Landing time (# of frames)")
plt.xlabel("Fly num")
plt.savefig("Landing time across fly not clustered")
plt.show()
"""
"""
for path in Landing_prob_data_path:
    Temp = pd.read_excel(path)
    Total = 0
    NANTotal = 0
    W = 0
    N = 0
    SF = 0
    N_A = 0
    for key in Temp.keys()[1:]:
        for data in Temp[key]:
            if data == 'W' or data == 'W*':
                W += 1
                NANTotal += 1
            if data == 'N' or data == 'N*':
                N += 1
                NANTotal += 1
            if data == 'SF':
                SF += 1
                NANTotal += 1
            if type(data) is float:
                N_A += 1
                NANTotal += 1
            Total += 1
    print(f"W: {W} N: {N} SF:{SF} N/A: {N_A} NanTotal: {NANTotal}")
    print("*****************")
    print(f"W: {W/NANTotal}")
    print(f"N: {N/NANTotal}")
    print(f"SF: {SF/NANTotal}")
    print(f"N/A: {N_A/NANTotal}")
    print(f"Nan percentage: {NANTotal/Total}")
    print("*****************")
"""
"""
for path in Landing_prob_data_path:
    LandingProbData = pd.read_excel(path)
    for i in range(len(LandingProbData)):
        Landing = 0
        Flying = 0
        for data in LandingProbData.iloc[i][1:]:
            if data == 1:
                Landing += 1
            if data == 0:
                Flying += 1
        LandingProbAcrossFly.append(Landing/(Flying+Landing))
LandingProbAcrossFly = np.asarray(LandingProbAcrossFly)
LandingProbAcrossFly = np.reshape(LandingProbAcrossFly, (-1, 25))
LandingProbAcrossFly = np.transpose(LandingProbAcrossFly)


Landing_df = pd.DataFrame(LandingProbAcrossFly, columns=group_name)
print(Landing_df)

sns.stripplot(Landing_df)
plt.ylim(-0.1, 1.1)
plt.show()
"""