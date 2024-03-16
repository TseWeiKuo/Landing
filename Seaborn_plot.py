import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
import numpy as np
from sklearn.utils import resample
import matplotlib.patches as mpatches
from scipy.stats import kendalltau
# Apply the default theme
def calculate_mean_diff(data1, data2):
    return np.mean(data1) - np.mean(data2)
def calculate_median_diff(data1, data2):
    return np.median(data1) - np.median(data2)
def CreateLandingProbAcrossTrial(Landing_prob_data_path):
    LandingProbData = []
    t = 20
    trial = []
    for i in range(Trial_num):
        trial.append(str(i + 1))
    for path in Landing_prob_data_path:
        print(path)
        Temp = pd.read_excel(path)
        landingtemp = []
        for key in Temp.keys()[1:][:Trial_num]:
            Landing = 0
            Flying = 0
            for data in Temp[key]:
                if isinstance(data, np.floating):
                    data = float(data)
                if type(data) is not str and (type(data) is float or type(data) is int):
                    if data == 1:
                        Landing += 1
                    if data == 0:
                        Flying += 1
                # print(data)
            print("Landing: " + str(Landing))
            landingtemp.append(Landing / (Landing + Flying))
        LandingProbData.append(landingtemp)
    LandingProbData = np.asarray(LandingProbData)
    LandingProbData = np.transpose(LandingProbData)
    LandingProbData = pd.DataFrame(LandingProbData, columns=group_name)
    print(LandingProbData)

    plt.figure(figsize=(12, 9))
    LandingProbGraph = sns.lineplot(data=LandingProbData)
    LandingProbGraph.set_xticks(range(Trial_num))
    LandingProbGraph.set_xticklabels(trial)
    plt.legend(loc='center right', prop={'size': 15})
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=15)
    plt.xlabel("Trial", fontsize=15)
    plt.ylabel("Landing probability", fontsize=15)
    plt.savefig("Landing Probability")
    plt.show()
def CreateLandingProbAcrossFlies(Landing_prob_data_path):
    LandingProbData = []
    group_name = ["Control (TT)", "Starved (TT)"]#, "Starved-TF-CT", "Starved-TT"]

    for path in Landing_prob_data_path:
        Temp = pd.read_excel(path)
        landingtemp = []
        for i in range(Fly_Num):
            Landing = 0
            Flying = 0
            print(f"Fly {i + 1}")
            print(Temp.iloc[i][1:][:Trial_num])
            for data in Temp.iloc[i][1:][:Trial_num]:
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

    # Find the maximum length of LandingProbData lists
    max_length = max(len(lst) for lst in LandingProbData)

    # Pad shorter lists with NaNs to make them the same length
    LandingProbData = [lst + [float('nan')] * (max_length - len(lst)) for lst in LandingProbData]
    print(LandingProbData[0])
    print(LandingProbData[1])
    # Create a DataFrame
    data = {'Target joint': [name for name in group_name for _ in range(max_length)],
            'LandingProbability': [item for sublist in LandingProbData for item in sublist]}
    print(data)
    df = pd.DataFrame(data)
    # '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'
    # Plot stripplot with different colors for each group
    plt.figure(figsize=(12, 9))
    g = sns.stripplot(x='Target joint', y='LandingProbability', data=df, size=12, linewidth=0.5, alpha=0.5, palette=['#ff7f0e', '#d62728'], jitter=0.35)

    # Plot mean and error bars
    mean_data = df.groupby('Target joint')['LandingProbability'].agg(['mean', 'std', 'count']).reset_index()
    mean_data['ci'] = 1.96 * mean_data['std'] / np.sqrt(mean_data['count'])
    print(mean_data)

    sns.pointplot(x='Target joint', y='mean', data=mean_data, color='gray', linestyles=" ", markers="s", markersize=10, ci=None)
    plt.errorbar(x=mean_data['Target joint'], y=mean_data['mean'], yerr=mean_data['ci'], fmt="none", color='gray', capsize=5)

    g.set_xticks(range(len(group_name)))
    g.set_xticklabels(group_name, fontsize=15)
    plt.tick_params(axis='y', labelsize=15)
    plt.xlim((min(range(len(group_name))) - 1, max(range(len(group_name))) + 1))
    plt.ylabel("Landing Probability", fontsize=15)
    plt.savefig("Landing Prob across fly")
    plt.show()
    return
def CreateLandingTimeAcrossTrialStripplot(Landing_time_data_path):
    LandingTimeData = []
    trial = []
    for i in range(Trial_num):
        trial.append(str(i+1))
    plt.figure(1, figsize=(12, 9))
    for i in range(len(Landing_time_data_path)):
        plt.subplot(2, 1, i+1)
        legend_label = []
        Mean = []
        LandingTimeData = []
        y_errors = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for key in Temp.keys()[1:][:Trial_num]:
            print(Temp[key])
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

        legend_label.append(mpatches.Patch(color=colors[i], label=group_name[i]))
        print(Mean)
        for LandingData in LandingTimeData:
            y_errors.append(np.std(LandingData) / np.sqrt(len(LandingData)))
        plt.errorbar(x=range(Trial_num), y=Mean, yerr=y_errors, color=colors[i], capsize=5)
        plt.scatter(x=range(Trial_num), y=Mean, color=colors[i], s=100, linewidths=1)
        """
        for j, m in enumerate(Mean):
            plt.errorbar(x=j, y=m, yerr=y_errors[j], color=colors[i], capsize=5)
            plt.scatter(x=j, y=m, color=colors[i], s=100, linewidths=1)
        """
        g = sns.stripplot(LandingTimeData, color=colors[i], linewidth=0.5, size=7, alpha=0.7)
        g.legend(handles=legend_label, loc='upper left', prop={'size': 15})
        g.set_xticks(range(Trial_num))
        g.set_xticklabels(trial)
        plt.ylabel("Landing time (# of frames)", fontsize=15)
        plt.xlabel("Trial", fontsize=15)
        plt.tick_params(axis='y', labelsize=15)
        plt.tick_params(axis='x', labelsize=15)
    plt.savefig("Landing time across trial strip plot")
    plt.tight_layout()
    plt.show()
def CreateLandingTimeAcrossFlyStripplot(Landing_time_data_path):
    legend_label = []
    LandingTimeAcrossExperiment = []
    for i in range(len(Landing_time_data_path)):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for k in range(len(Temp)):
            landingtemp = []
            for data in Temp.iloc[k][1:]:
                if isinstance(data, np.floating):
                    data = float(data)
                if type(data) is not str and (type(data) is float or type(data) is int):
                    if data > -1:
                        landingtemp.append(data)
            LandingTimeData.append(landingtemp)
        LandingTimeAcrossExperiment.append(LandingTimeData)
    for ex in LandingTimeAcrossExperiment:
        print(ex)
        for da in ex:
            print(da)
        print("\n")
    # LandingTimeAcrossExperiment = np.asarray(LandingTimeAcrossExperiment)

    data = LandingTimeAcrossExperiment

    # Create a strip plot for each sublist of the sublist with different colors in each subplot
    plt.figure(figsize=(15, 8))
    for i, element_data in enumerate(data, start=1):
        colr = 0
        plt.subplot(1, 2, i)
        for j, sublist in enumerate(element_data):
            if len(sublist) != 0:
                sns.stripplot(x=j+1, y=sublist, jitter=True, marker='o', alpha=0.7, color=colors[colr])
            colr += 1

        # plt.title(f'Strip Plot - Element {i}')
        plt.xlabel(group_name[i - 1])
        plt.ylabel('Landing time (# of frames)')
        plt.ylim(0, 600)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 10})

    plt.tight_layout()
    plt.savefig("Landind time across fly clustered")
    plt.show()
def CreateLandingTimeCluster(Landing_time_data_path):
    legend_label = []
    LandingTimeAcrossExperiment = []
    for i in range(len(Landing_time_data_path)):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for k in range(len(Temp)):
            landingtemp = []
            print(Temp.iloc[k][1:][:Trial_num])
            for data in Temp.iloc[k][1:][:Trial_num]:
                # print(f"Data type: {type(data)}")
                if isinstance(data, np.floating):
                    # print(data)
                    data = float(data)
                if type(data) is not str and (type(data) is float or type(data) is int):
                    if data > -1:
                        landingtemp.append(data)
            LandingTimeData.append(landingtemp)
        LandingTimeAcrossExperiment.append(LandingTimeData)
    print(LandingTimeAcrossExperiment)
    # LandingTimeAcrossExperiment = np.asarray(LandingTimeAcrossExperiment)

    data = LandingTimeAcrossExperiment

    # Create a strip plot for each sublist of the sublist with different colors in each subplot
    plt.figure(figsize=(8, 6))
    for i, element_data in enumerate(data, start=1):
        colr = 0
        plt.subplot(1, 2, i)
        for j, sublist in enumerate(element_data):
            sns.stripplot(y=sublist, jitter=0.2, marker='o', alpha=0.7, color=colors[i-1])
            colr += 1

        # plt.title(f'Strip Plot - Element {i}')
        plt.xlabel(group_name[i - 1], fontsize=15)
        plt.ylabel('Landing time (# of frames)', fontsize=15)
        plt.tick_params(axis='y', labelsize=15)
        plt.ylim(0, 750)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 10})
    plt.tight_layout()
    plt.savefig("Landind time across fly clustered")
    plt.show()
def plotLandingTimeDistribution(Landing_time_data_path):
    LandingTimeAcrossExperiment = []
    for i in range(len(Landing_time_data_path)):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for k in range(len(Temp)):
            for data in Temp.iloc[k][1:][:Trial_num]:
                # print(f"Data type: {type(data)}")
                if isinstance(data, np.floating):
                    # print(data)
                    data = float(data)
                if type(data) is not str and (type(data) is float or type(data) is int):
                    if data > -1:
                        LandingTimeData.append(data)
        LandingTimeAcrossExperiment.append(LandingTimeData)

    data = LandingTimeAcrossExperiment
    fig, axes = plt.subplots(len(Landing_time_data_path), 1)
    for i in range(len(Landing_time_data_path)):
        plt.subplot(len(Landing_time_data_path), 1, i+1)
        sns.histplot(data[i], bins=50, kde=True, color=colors[i], stat='density', label=group_name[i])
        axes[i].legend()
    plt.xlabel("Landing time (# of frames)")
    fig.tight_layout()
    plt.savefig("Landing time distribution")
    plt.show()
def plotLandingProbDistribution(Landing_prob_data_path):
    LandingProbData = []
    for path in Landing_prob_data_path:
        Temp = pd.read_excel(path)
        landingtemp = []
        for i in range(Fly_Num):
            Landing = 0
            Flying = 0
            print(f"Fly {i + 1}")
            print(Temp.iloc[i][1:][:Trial_num])
            for data in Temp.iloc[i][1:][:Trial_num]:
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

    data = LandingProbData
    fig, axes = plt.subplots(len(Landing_prob_data_path), 1)
    for i in range(len(Landing_prob_data_path)):
        plt.subplot(len(Landing_prob_data_path), 1, i+1)
        sns.histplot(data[i], bins=50, kde=True, color=colors[i], stat='density', label=group_name[i])
        axes[i].legend()
    plt.xlabel("Landing Probability")
    fig.tight_layout()
    plt.savefig("Landing prob distribution")
    plt.show()
def CreateLandingTimeClusterWithMeans(Landing_time_data_path):
    LandingTimeAcrossExperiment = []
    for i in range(len(Landing_time_data_path)):
        LandingTimeData = []
        Temp = pd.read_excel(Landing_time_data_path[i])
        for k in range(len(Temp)):
            landingtemp = []
            for data in Temp.iloc[k][1:]:
                if isinstance(data, np.floating):
                    data = float(data)
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
        colr = 0
        plt.subplot(2, 2, i)
        for j, sublist in enumerate(element_data):
            sns.stripplot(y=sublist, jitter=True, marker='o', alpha=0.7, color=colors[colr])
            colr += 1


        # plt.title(f'Strip Plot - Element {i}')
        plt.xlabel(group_name[i - 1])
        plt.ylabel('Landing time (# of frames)')
        plt.ylim(0, 750)
        # plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 10})

    plt.tight_layout()
    plt.savefig("Landind time across fly clustered")
    plt.show()
def LLAcrossTrial(Original_Data, Filter_Data):
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    sns.set(style="whitegrid")
    plt.figure(1, figsize=(12, 9))
    for i, group_data in enumerate(Original_Data):
        legend_label = []
        plt.subplot(2,1,i + 1)
        LandingLatencyData = []
        for t, landinglate in group_data[Trials].items():
            Landing_latency = [l / FPS for l in landinglate if not isinstance(l, str) and l > -1]
            #print(Landing_latency)
            if len(Landing_latency) == 0:
                LandingLatencyData.append([])
            else:
                LandingLatencyData.append(Landing_latency)
        g = sns.stripplot(LandingLatencyData, jitter=0.2, marker='o', size=8, alpha=0.4, color=colors[i])

        data = LandingLatencyData
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
        mLandinglatency = []
        eLandingLatency = []
        for l in LandingLatencyData:
            if len(l) != 0:
                eLandingLatency.append(1.96 * (np.std(l) / np.sqrt(len(l))))
                mLandinglatency.append(np.mean(l))
            else:
                eLandingLatency.append(0)
                mLandinglatency.append(0)
        plt.errorbar(x=range(Trial_num), y=mLandinglatency, yerr=eLandingLatency, color=colors[i], capsize=5)
        plt.scatter(x=range(Trial_num), y=mLandinglatency, color=colors[i], s=100, linewidths=1)
        legend_label.append(mpatches.Patch(color=colors[i], label=group_name[i]))
        g.set_xticks(range(Trial_num))
        g.set_xticklabels(trial)
        plt.xlabel("Trial", fontsize=15)
        plt.tick_params(axis='y', labelsize=15)
        plt.tick_params(axis='x', labelsize=15)
        plt.ylabel("Landing latency (s)", fontsize=15)
        g.legend(handles=legend_label, loc='upper left', prop={'size': 15})
    plt.tight_layout()
    plt.savefig("LL AcrossTrial (ControlCTF vs Starved CTF)")
    plt.show()
def LPAcrossTrials(Original_Data):
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    sns.set(style="whitegrid")
    plt.figure(1, figsize=(12, 9))
    legend_label = []
    for i, group_data in enumerate(Original_Data):
        LandingProb_AT = []
        for t, landingprob in group_data[Trials].items():
            Flying = [f for f in landingprob if f == -1]
            Landing_latency = [l / FPS for l in landingprob if not isinstance(l, str) and l > -1]
            LandingProb_AT.append(len(Landing_latency) / (len(Flying) + len(Landing_latency)))
        g = sns.lineplot(x=range(Trial_num), y=LandingProb_AT, color=colors[i])
        legend_label.append(mpatches.Patch(color=colors[i], label=group_name[i]))
        g.set_xticks(range(Trial_num))
        g.set_xticklabels(trial)
    plt.tick_params(axis='y', labelsize=15)
    plt.tick_params(axis='x', labelsize=15)
    plt.xlabel("Trial", fontsize=15)
    plt.ylabel("Landing Probability", fontsize=15)


    plt.legend(handles=legend_label, loc='upper left', prop={'size': 15})
    plt.savefig("LandingProb AcrossTrial (Control CTF vs Starved CTF")
    plt.show()
def LLCluster(Original_Data, Filter_Data):
    global FPS
    sns.set(style="whitegrid")
    Trials = ["Trial_" + str(i+1) for i in range(Trial_num)]
    plt.figure(1, figsize=(8, 6))
    for i, group_data in enumerate(Original_Data, start=1):
        print(group_data)
        plt.subplot(1, 2, i)
        n = 0
        for index, fly in group_data[Trials].iterrows():
            Landing_latency = [l / FPS for l in fly if not isinstance(l, str) and l > -1]
            sns.stripplot(y=Landing_latency, jitter=0.2, marker='o', size=8, alpha=0.4, color=colors[n])
            n += 1
    for i, group_data in enumerate(Filter_Data, start=1):
        plt.subplot(1, 2, i)
        sns.stripplot(y="MLandingLatency", data=group_data, jitter=0.2, marker='s', size=12, alpha=0.4, color=colors[i-1])
        plt.xlabel(group_data["Group_Name"][0])
        plt.ylabel("Landing latency (s)", fontsize=15)
        plt.ylim(0, 3)
        plt.tick_params(axis="y", labelsize=15)
    plt.tight_layout()
    plt.savefig("LandingLatency (ControlCTF vs StarvedCTF")
    plt.show()
def Bootstrapping_test(data1, data2):

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
    fig, axes = plt.subplots(2, 1)
    plt.subplot(2, 1, 1)
    sns.histplot(bootstrap_mean_diffs, bins=50, kde=True, color='skyblue', stat='count')
    plt.axvline(original_mean_diff, color='red', linestyle='dashed', linewidth=2, label='Original mean difference')
    axes[0].legend()
    # axes[0].legend(bbox_to_anchor=(1.1, 1.05))
    plt.xlabel('Mean-Difference')
    plt.subplot(2, 1, 2)
    sns.histplot(bootstrap_median_diffs, bins=50, kde=True, color='skyblue', stat='count')
    plt.axvline(original_median_diff, color='green', linestyle='dashed', linewidth=2, label='Original median difference')
    axes[1].legend()
    # axes[1].legend(bbox_to_anchor=(1.1, 1.05))
    plt.xlabel('Median-Difference')
    fig.tight_layout()
    Mean_diff_p_value = (np.sum(np.abs(bootstrap_mean_diffs) >= np.abs(original_mean_diff))) / (num_bootstrap_samples)
    Median_diff_p_value = (np.sum(np.abs(bootstrap_median_diffs) >= np.abs(original_median_diff))) / (num_bootstrap_samples)

    print(f"Difference in mean's P-value = {Mean_diff_p_value}")
    print(f"Original mean diff = {original_mean_diff}")
    print(f"Difference in median's P value = {Median_diff_p_value}")
    print(f"Original median diff = {original_median_diff}")

    # plt.title('Bootstrap mean and median difference Distribution', y=1)
    plt.ylabel('Count')
    plt.legend()
    plt.savefig("Bootstrapping mean diff")

    plt.show()
def LPAcrossFlies(Data_to_plot):
    combined_df = pd.concat(Data_to_plot)
    sns.set(style="whitegrid")

    # Create catplot
    plt.figure(figsize=(10, 6))
    g = sns.stripplot(x="Group_Name", y="LandingProb", hue="Group_Name", data=combined_df, jitter=0.3, alpha=0.5, size=12)
    group_stat = combined_df.groupby('Group_Name')['LandingProb'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='gray', linestyles=" ", markers="s", markersize=10,
                  errorbar=None)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='gray',
                 capsize=5)
    plt.title('Landing Probability (Light touch: Control CTF vs Starved CTF)', fontsize=15)
    plt.ylabel("Landing Probability", fontsize=15)
    plt.tick_params(axis="y", labelsize=15)
    plt.xlabel("Group", fontsize=15)
    g.set_ylim(-0.1, 1)

    # Show the plot

    plt.savefig("Landing Probability ControlCTF vs StarvedCTF")
    plt.show()
def ReadAndFilterData(GroupName, Flies_to_pick, Landing_Data_path):
    global Trial_num
    Landing_Data = pd.read_excel(Landing_Data_path)
    Landing_Data = Landing_Data.iloc[Flies_to_pick[0] - 1:Flies_to_pick[1]]
    Valid_data_index = []
    for index, row in Landing_Data.iterrows():
        str_nan_count = 0
        for data in row.values:
            if isinstance(data, str) or pd.isna(data):
                str_nan_count += 1
        if str_nan_count < (len(row.values) / 2):
            Valid_data_index.append(index)
    Landing_Data = Landing_Data[Landing_Data.index.isin(Valid_data_index)]
    GroupNameCol = [GroupName] * len(Valid_data_index)
    Landing_Data["Group_Name"] = GroupNameCol
    return Landing_Data
def CalculateLPAndmLLAcrossFlies(GroupName, Landing_Data):
    global FPS
    LP_mLL_Data = dict()
    LP_mLL_Data["LandingProb"] = []
    LP_mLL_Data["MLandingLatency"] = []
    LP_mLL_Data["Fly#"] = []
    LP_mLL_Data["Time"] = Landing_Data["Time"].tolist()
    LP_mLL_Data["Date"] = Landing_Data["Date"].tolist()
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str)]
        Flying = [f for f in row if f == -1]
        Landing_latency = [l / FPS for l in row if not isinstance(l, str) and l > -1]
        if len(Nan_data) + len(Flying) + len(Landing_latency) != Trial_num:
            print(f"Error while filtering data")
            print(f"Index: {index}")
            print(f"# of Nan: {len(Nan_data)}\t{Nan_data}")
            print(f"# of Flying: {len(Flying)}\t{Flying}")
            print(f"# of Landing: {len(Landing_latency)}\t{Landing_latency}")
        LP_mLL_Data["Fly#"].append(index + 1)
        LP_mLL_Data["LandingProb"].append(len(Landing_latency) / (len(Flying) + len(Landing_latency)))
        LP_mLL_Data["MLandingLatency"].append(np.mean(Landing_latency))
    LP_mLL_Data["Group_Name"] = [GroupName] * Landing_Data.shape[0]
    LP_mLL_Data = pd.DataFrame(LP_mLL_Data)
    return LP_mLL_Data

Landing_Prob_Data_Path_Control_CTF = r"C:\Users\agrawal-admin\Desktop\DataFolder\Starved_Fly_Experiment\Control_CTF\Control_CTF_All.xlsx"
Landing_Prob_Data_Path_Starved_CTF = r"C:\Users\agrawal-admin\Desktop\DataFolder\Starved_Fly_Experiment\Starved_CTF\Starved_CTF_All.xlsx"
FPS = 250
group_name = ["Control-CTF",
              "Starved-CTF"]
Trial_num = 20
trial = [str(t+1) for t in range(Trial_num)]
Control_CTF_Picked_Fly = [34, 78]
Starved_CTF_Picked_Fly = [42, 96]
Fly_Num = 34
# '#1f77b4',
Linestyles = [(0, (1, 10)), (0, (1, 1)), (0, (1, 1)), (5, (10, 3)), (0, (5, 10)), (0, (5, 5)), (0, (5, 1))]
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

Control_CTF_Landing_Data = ReadAndFilterData("Control_CTF", Control_CTF_Picked_Fly, Landing_Prob_Data_Path_Control_CTF)
Starved_CTF_Landing_Data = ReadAndFilterData("Starved_CTF", Starved_CTF_Picked_Fly, Landing_Prob_Data_Path_Starved_CTF)
Control_CTF_LP_mLL_AF = CalculateLPAndmLLAcrossFlies("Control_CTF", Control_CTF_Landing_Data)
Starved_CTF_LP_mLL_AF = CalculateLPAndmLLAcrossFlies("Starved_CTF", Starved_CTF_Landing_Data)
print(Starved_CTF_LP_mLL_AF)

