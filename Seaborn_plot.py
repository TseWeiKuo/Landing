import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import numpy as np
from sklearn.utils import resample
from scipy.stats import kendalltau
from scipy.stats import ttest_ind, ttest_rel
import warnings
warnings.filterwarnings(action="ignore", category=RuntimeWarning)

def perform_t_test(data1, data2, alpha=0.05, paired=False):
    """
    Perform a t-test and return whether the null hypothesis is rejected.

    Parameters:
        data1 (array-like): First dataset.
        data2 (array-like): Second dataset.
        alpha (float): Significance level (default is 0.05).
        paired (bool): If True, perform a paired t-test; otherwise, perform an independent t-test.

    Returns:
        bool: True if the null hypothesis is rejected, False otherwise.
        float: p-value from the t-test.
    """

    if paired:
        # Perform a paired t-test
        t_stat, p_value = ttest_rel(data1, data2)
    else:
        # Perform an independent two-sample t-test
        t_stat, p_value = ttest_ind(data1, data2)
        print(p_value < alpha, p_value)
    # Return True if p-value is less than the significance level
    return p_value < alpha, p_value
def calculate_mean_diff(data1, data2):
    return np.mean(data1) - np.mean(data2)
def calculate_median_diff(data1, data2):
    return np.median(data1) - np.median(data2)
def calculate_sem(data):
    # Calculate the mean
    mean = np.mean(data)

    # Calculate the differences between each number and the mean
    differences = data - mean

    # Square each difference
    squared_diff = differences ** 2

    # Find the mean of squared differences
    mean_squared_diff = np.mean(squared_diff)

    # Calculate the standard deviation
    std_dev = np.sqrt(mean_squared_diff)

    # Calculate the standard error of the mean (SEM)
    sem = std_dev / np.sqrt(len(data))

    return sem
def LLAcrossTrial(Original_Data):
    global Color_blind_palette
    global markers
    global FilterHighLatency
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    #sns.set(style="whitegrid")
    plt.figure(1, figsize=(8, 6))
    for i, group_data in enumerate(Original_Data):
        legend_label = []
        plt.subplot(1, len(Original_Data), i + 1)
        LandingLatencyData = []
        for t, landinglate in group_data[0][Trials].items():
            fps = group_data[1]
            if FilterHighLatency:
                Landing_latency = [l / fps for l in landinglate if not isinstance(l, str) and l > -1 and l < 1 * fps]
            else:
                Landing_latency = [l / fps for l in landinglate if not isinstance(l, str) and l > -1]

            if len(Landing_latency) == 0:
                LandingLatencyData.append([])
            else:
                LandingLatencyData.append(Landing_latency)
        MannKendallTest(LandingLatencyData)
        LandingLatencyData = [LandingLatencyData[0], LandingLatencyData[4], LandingLatencyData[9], LandingLatencyData[14], LandingLatencyData[19]]
        g = sns.stripplot(LandingLatencyData, jitter=0.15, marker=markers[i], size=12, alpha=0.65, color=Color_blind_palette[i])
        mLandinglatency = []
        eLandingLatency = []
        for l in LandingLatencyData:
            if len(l) != 0:
                eLandingLatency.append(1.96 * (np.std(l) / np.sqrt(len(l))))
                mLandinglatency.append(np.mean(l))
            else:
                eLandingLatency.append(0)
                mLandinglatency.append(0)
        plt.errorbar(x=range(5), y=mLandinglatency, yerr=eLandingLatency, color=Color_blind_palette[i], capsize=5, marker=markers[i], linewidth=1.5, fmt=' ')
        plt.scatter(x=range(5), y=mLandinglatency, color=Color_blind_palette[i], s=100, marker=markers[i], linewidth=1.5)

        """
        legend_elements = [plt.Line2D([0], [0], marker=markers[i], color='w', label=group_name[i],
                                      markerfacecolor=Color_blind_palette[i],
                                      markersize=10)]
        """
        g.set_xticks([0, 1, 2, 3, 4])
        g.set_xticklabels(["1", "5", "10", "15", "20"])
        plt.xlabel("Trial", fontsize=25)
        plt.tick_params(axis='y', labelsize=15)
        plt.tick_params(axis='x', labelsize=15)
        plt.ylabel("Landing latency (s)", fontsize=15)
        plt.yticks([0, 0.5, 1, 1.5])
        plt.ylim(-0.2, 2)
        g.spines['left'].set_linewidth(3)
        g.spines['bottom'].set_linewidth(3)
        plt.tick_params(width=3, length=10)
        #g.legend(handles=legend_elements, loc='upper left', prop={'size': 15})
    sns.despine()
    plt.tight_layout()
    plt.savefig("LLAcrossTrials.pdf", format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
def MannKendallTest(Data):
    # Flatten the data for Kendall's Tau test
    if not isinstance(Data[0], float):
        flat_data = [item for sublist in Data for item in sublist]

        # Create corresponding x-values (trial numbers)
        x_values = np.concatenate([[i + 1] * len(trial) for i, trial in enumerate(Data)])
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
    else:
        tau, p_value = kendalltau(range(len(Data)), Data)
        # Output results
        print(f"Kendall's Tau: {tau}")
        print(f"P-value: {p_value}")

        # Check significance at a 0.05 level
        if p_value < 0.05:
            print("Reject the null hypothesis: There is a significant trend.")
        else:
            print("Fail to reject the null hypothesis: No significant trend detected.")
def LPAcrossTrials(Original_Data):
    global FilterHighLatency
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    #sns.set(style="whitegrid")
    ls = ["solid", "solid", "solid", "dashed"]
    plt.figure(1, figsize=(12, 9))
    legend_label = []
    for i, group_data in enumerate(Original_Data):
        LandingProb_AT = []
        for t, landingprob in group_data[0][Trials].items():
            fps = group_data[1]
            if FilterHighLatency:
                Flying = [f for f in landingprob if not (isinstance(f, str) or pd.isna(f)) and (f == -1 or f >= 1 * fps)]
                Landing_latency = [l / fps for l in landingprob if not isinstance(l, str) and l > 0 and l < 1 * fps]
            else:
                Flying = [f for f in landingprob if f == -1]
                Landing_latency = [l / fps for l in landingprob if not isinstance(l, str) and l > -1]
            LandingProb_AT.append(len(Landing_latency) / (len(Flying) + len(Landing_latency)))
        MannKendallTest(LandingProb_AT)
        g = sns.lineplot(x=range(Trial_num), y=LandingProb_AT, color=Color_blind_palette[i-1], linestyle=ls[i], lw=5)
        legend_label.append(plt.Line2D([0], [0], color=Color_blind_palette[i-1], linestyle=ls[i], label=group_name[i]))
        g.set_xticks([0, 4, 9, 14, 19])
        g.set_yticks([0, 0.35, 0.7])
        g.set_xticklabels(["1", "5", "10", "15", "20"])
        g.spines['left'].set_linewidth(3)
        g.spines['bottom'].set_linewidth(3)
    plt.tick_params(axis='y', labelsize=25)
    plt.tick_params(axis='x', labelsize=25)
    plt.tick_params(width=3, length=10)
    plt.xlabel("Trial", fontsize=25)
    plt.ylabel("Probability", fontsize=25)
    sns.despine()

    plt.legend(handles=legend_label, loc='upper right', prop={'size': 20})
    plt.savefig("LPAcrossTrial.pdf", format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
def MLLCluster(Filter_Data, file_name):
    global markers
    global FilterHighLatency
    Trials = ["Trial_" + str(i+1) for i in range(Trial_num)]
    fig = plt.figure(1, figsize=(20, 10))
    sns.axes_style("ticks")

    combined_df = pd.concat(Filter_Data)
    # ax = sns.violinplot(x="Group_Name", y="MLandingLatency", data=combined_df, palette=Color_blind_palette)
    ax = sns.stripplot(x="Group_Name", y="MLandingLatency", data=combined_df, jitter=0.2, size=20, alpha=0.5, marker="o", palette=Color_blind_palette)
    """for i, group_data in enumerate(Filter_Data, start=1):
        if samejoint:
            ax = sns.stripplot(x="Group_Name", y="MLandingLatency", data=group_data, jitter=0.2, size=20, alpha=0.75, marker=markers[i - 1], color=Color_blind_palette[0])
        else:
            ax = sns.stripplot(x="Group_Name", y="MLandingLatency", data=group_data, jitter=0.2, size=20, alpha=0.75, marker=markers[i - 1], color=Color_blind_palette[i-1])"""

    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)
    group_stat = combined_df.groupby('Group_Name')["MLandingLatency"].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10)
    plt.ylabel("Mean Landing latency (s)", fontsize=25)
    plt.ylim(-0.1, 1.2)
    plt.yticks([0, 0.5, 1])
    plt.xlim(-1, len(Filter_Data))
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=20, rotation=45)
    plt.tick_params(width=3, length=10)
    sns.despine()
    plt.tight_layout()

    plt.savefig(f"{file_name}.pdf", format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
def TLLCluster(Original_Data, file_name):
    global markers
    global FilterHighLatency
    Trials = ["Trial_" + str(i+1) for i in range(Trial_num)]
    fig = plt.figure(1, figsize=(len(Original_Data) * 2, 10))
    sns.axes_style("ticks")
    combined_df = pd.concat(Original_Data)

    # ax = sns.violinplot(x="Group_Name", y="TrialLandingLatency", data=combined_df, palette=Color_blind_palette)
    # ax = sns.stripplot(x="Group_Name", y="TrialLandingLatency", data=combined_df, jitter=0.2, size=20, alpha=0.2, marker=["o", ">"], palette=Color_blind_palette)
    m = ["o", ">"]
    for d, data in enumerate(Original_Data):
        ax = sns.stripplot(x="Group_Name", y="TrialLandingLatency", data=data, jitter=0.2, size=20, alpha=0.2, marker=m[d], color=Color_blind_palette[d])
        ax.spines['left'].set_linewidth(3)
        ax.spines['bottom'].set_linewidth(3)
    group_stat = combined_df.groupby('Group_Name')["TrialLandingLatency"].agg(['mean', 'std', 'count']).reset_index()
    print(group_stat)
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10, zorder=10)
    plt.ylabel("Trial Landing latency (s)", fontsize=25)
    plt.xlabel("Group", fontsize=25)
    if FilterHighLatency:
        plt.ylim(-0.1, 0.9)
        plt.yticks([0, 0.4, 0.8])
    else:
        plt.ylim(-0.3, 3)
        plt.yticks([0, 1.5, 3])
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25, rotation=45)
    plt.tick_params(width=3, length=10)
    plt.xlim(-1, len(Original_Data))
    sns.despine(trim=True)
    plt.tight_layout()

    plt.savefig(f"{file_name}.pdf", format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
def Bootstrapping_test(data1, data2):

    num_bootstrap_samples = 30000

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
        # print(bootstrap_sample1)
        bootstrap_sample2 = resample(resample_data, n_samples=len(data2))
        # print(bootstrap_sample2)
        # print(bootstrap_sample1)

        # Perform t-test on the bootstrap samples
        bootstrap_median_diff = calculate_median_diff(bootstrap_sample1, bootstrap_sample2)
        bootstrap_mean_diff = calculate_mean_diff(bootstrap_sample1, bootstrap_sample2)
        # print(bootstrap_mean_diff)

        bootstrap_mean_diffs.append(bootstrap_mean_diff)
        bootstrap_median_diffs.append(bootstrap_median_diff)

    k = 0
    for m in bootstrap_mean_diffs:
        # print(m)
        if abs(m) > abs(original_mean_diff):
            k += 1
    Mean_diff_p_value = (np.sum(np.abs(bootstrap_mean_diffs) >= np.abs(original_mean_diff))) / (num_bootstrap_samples)
    Median_diff_p_value = (np.sum(np.abs(bootstrap_median_diffs) >= np.abs(original_median_diff))) / (num_bootstrap_samples)

    # print(f"Difference in mean's P-value = {Mean_diff_p_value}")
    # print(f"Original mean diff = {original_mean_diff}")
    return Mean_diff_p_value
def LPAcrossFlies(Data_to_plot, file_name):
    global Color_blind_palette
    global markers
    global samejoint
    global vio
    combined_df = pd.concat(Data_to_plot)
    plt.figure(figsize=(len(Data_to_plot) * 2, 10))
    transparency = [0.5, 0.7, 0.9]
    g = None
    if samejoint:
        for i, d in enumerate(Data_to_plot):
            if not vio:
                g = sns.stripplot(x="Group_Name", y="LandingProb", data=d, alpha=0.4, jitter=0.2, dodge=False, size=20, marker=markers[i], color=Color_blind_palette[0])
            else:
                g = sns.violinplot(x="Group_Name", y="LandingProb", data=d, hue="Group_Name")
                for j, violin in enumerate(g.collections):
                    violin.set_alpha(transparency[j])  # Set the transparency level (0.0 to 1.0)
    else:
        if not vio:
            for i, d in enumerate(Data_to_plot):
                g = sns.stripplot(x="Group_Name", y="LandingProb", data=d, alpha=0.4, jitter=0.1, dodge=False, size=30, marker=markers[i], color=Color_blind_palette[i], zorder=10)
        else:
            g = sns.violinplot(x="Group_Name", y="LandingProb", hue="Group_Name", data=combined_df, palette=Color_blind_palette)
    g.spines['left'].set_linewidth(3)
    g.spines['bottom'].set_linewidth(3)
    g.set_ylim(-0.1, 1.1)

    group_stat = combined_df.groupby('Group_Name')['LandingProb'].agg(['mean', 'std', 'count']).reset_index()
    # group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['std'], fmt="none", color='black', capsize=10, zorder=10)
    # legend_elements = [plt.Line2D([0], [0], marker=markers[i], color='w', label=group_name[i], markerfacecolor=Color_blind_palette[i], markersize=10) for i in range(len(Data_to_plot))]

    # plt.legend(handles=legend_elements, loc='upper right', fontsize=20)
    plt.ylabel("Landing Probability", fontsize=25)
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25, rotation=45)
    plt.tick_params(width=3, length=10)
    plt.yticks([0, 0.5, 1])
    plt.xlim(-1 - 1, len(Data_to_plot) + 1)
    sns.despine(trim=True)
    plt.tight_layout()
    plt.savefig(f"{file_name}.pdf", format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
def LPAcrossLight(Data_to_plot, file_name, color):
    global Color_blind_palette
    global markers
    global samejoint
    global vio

    data_type = "LandingProb"
    combined_df = pd.concat(Data_to_plot, ignore_index=True)
    plt.figure(figsize=(len(Data_to_plot) * 3, 10))

    # Sort by Fly# to keep connection consistent
    combined_df = combined_df.sort_values(by=['Fly#', 'Group_Name'])
    # print(combined_df)

    g = sns.pointplot(data=combined_df, x='Group_Name', y=data_type, ci=None, dodge=True, color=color, join=False)

    # Connect same flies with lines
    for fly_id, group in combined_df.groupby('Fly#'):
        print(fly_id, group)
        plt.plot(group['Group_Name'], group[data_type], marker='o', markersize=20,  color="lightgrey", linewidth=5)

    group_stat = combined_df.groupby('Group_Name')['LandingProb'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color=color, linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['std'], fmt="none", color=color, capsize=10, zorder=10)

    mean_df = combined_df.groupby('Group_Name', as_index=False)[data_type].mean()
    plt.plot(mean_df['Group_Name'], mean_df[data_type], color=color, marker='o', markersize=20, linewidth=5, label='Mean')

    plt.title('Change in Landing Probability Across Groups')
    plt.xlabel('Group')
    g.spines['left'].set_linewidth(3)
    g.spines['bottom'].set_linewidth(3)
    # plt.legend(handles=legend_elements, loc='upper right', fontsize=20)
    # plt.ylabel("Mean Landing Latency", fontsize=25)
    plt.ylabel("Landing Probability", fontsize=25)
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25, rotation=45)
    plt.tick_params(width=3, length=10)
    plt.yticks([0, 0.5, 1])
    plt.ylim(-0.1, 1.1)
    plt.xlim(-0.5, 1.5)
    sns.despine(trim=True)
    plt.tight_layout()
    plt.savefig(f"{file_name}.pdf")
    plt.close()
def FlyingProbability(Data_to_plot, file_name):
    global Color_blind_palette
    global markers
    global samejoint
    global vio
    combined_df = pd.concat(Data_to_plot)
    plt.figure(figsize=(len(Data_to_plot) * 4, 10))
    transparency = [0.5, 0.7, 0.9]
    g = None

    g = sns.stripplot(x="Group_Name", y="NotFlyingProb", hue="Group_Name", data=combined_df, palette=Color_blind_palette, size=20, alpha=0.8)
    g.spines['left'].set_linewidth(3)
    g.spines['bottom'].set_linewidth(3)
    g.set_ylim(-0.3, 1.5)

    group_stat = combined_df.groupby('Group_Name')['NotFlyingProb'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10)

    plt.ylabel("NotFlying Probability", fontsize=25)
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25, rotation=45)
    plt.tick_params(width=3, length=10)
    plt.yticks([0, 0.5, 1])
    plt.xlim(-0.5, len(Data_to_plot))
    sns.despine(trim=True)
    plt.tight_layout()
    plt.savefig(f"{file_name}.pdf", format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
def ReadAndFilterData(GroupName, Flies_to_pick, Landing_Data_path):
    global Trial_num
    global Threshold
    Landing_Data = pd.read_excel(Landing_Data_path)
    Landing_Data = Landing_Data.iloc[Flies_to_pick[0] - 1:Flies_to_pick[1]]
    Valid_data_index = []
    for index, row in Landing_Data.iterrows():
        str_nan_count = 0
        for data in row.values:
            if isinstance(data, str) or pd.isna(data):
                str_nan_count += 1
        if Threshold:
            if str_nan_count < (len(row.values) / 2):
                Valid_data_index.append(index)
        else:
            Valid_data_index.append(index)
    Landing_Data = Landing_Data[Landing_Data.index.isin(Valid_data_index)]
    GroupNameCol = [GroupName] * len(Valid_data_index)
    Landing_Data["Group_Name"] = GroupNameCol
    return Landing_Data
def ReadAndFilterOptogeneticData(GroupName, Flies_to_pick, Landing_Data_paths):
    global Trial_num
    Landing_Data_LO = pd.read_excel(Landing_Data_paths[0])
    Landing_Data_NL = pd.read_excel(Landing_Data_paths[1])
    Landing_Data_LO = Landing_Data_LO.iloc[Flies_to_pick[0] - 1:Flies_to_pick[1]]
    Landing_Data_NL = Landing_Data_NL.iloc[Flies_to_pick[0] - 1:Flies_to_pick[1]]

    Valid_data_index_LO = []
    for index, row in Landing_Data_LO.iterrows():
        str_nan_count = 0
        for data in row.values:
            if isinstance(data, str) or pd.isna(data):
                str_nan_count += 1
        if str_nan_count < (len(row.values) / 2):
            Valid_data_index_LO.append(index)

    Valid_data_index_NL = []
    for index, row in Landing_Data_NL.iterrows():
        str_nan_count = 0
        for data in row.values:
            if isinstance(data, str) or pd.isna(data):
                str_nan_count += 1
        if str_nan_count < (len(row.values) / 2):
            Valid_data_index_NL.append(index)

    Valid_index = []
    if len(Valid_data_index_LO) <= len(Valid_data_index_NL):
        Valid_index = Valid_data_index_LO
    else:
        Valid_index = Valid_data_index_NL

    Landing_Data_LO = Landing_Data_LO[Landing_Data_LO.index.isin(Valid_index)]
    GroupNameCol = [GroupName + " LO"] * len(Valid_index)
    Landing_Data_LO["Group_Name"] = GroupNameCol

    Landing_Data_NL = Landing_Data_NL[Landing_Data_NL.index.isin(Valid_index)]
    GroupNameCol = [GroupName + " NL"] * len(Valid_index)
    Landing_Data_NL["Group_Name"] = GroupNameCol

    return Landing_Data_LO, Landing_Data_NL
def CalculateOptogeneticLPLL(GroupName, Landing_Data, fps):
    global FilterHighLatency
    global trial_offset

    latency_threshold = 0.5
    LP_mLL_Data = dict()
    LP_mLL_Data["LandingProb"] = []
    LP_mLL_Data["MLandingLatency"] = []
    LP_mLL_Data["Fly#"] = []
    Trials = ["Trial_" + str(i + 1 + trial_offset) for i in range(Trial_num - trial_offset)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        if FilterHighLatency:
            Landing_latency = [l / fps for l in row if not isinstance(l, str) and l > 0 and l < latency_threshold * fps]
            Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str) or n < -1]
            Flying = [f for f in row if not (isinstance(f, str) or pd.isna(f)) and (f == -1 or f >= latency_threshold * fps)]
        else:
            Landing_latency = [l / fps for l in row if not isinstance(l, str) and l > 0]
            Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str)]
            Flying = [f for f in row if not (isinstance(f, str) or pd.isna(f)) and (f == -1)]
        if len(Nan_data) + len(Flying) + len(Landing_latency) != Trial_num - trial_offset:
            print(f"Error while filtering data")
            print(f"Index: {index}")
            print(f"# of Nan: {len(Nan_data)}\t{Nan_data}")
            print(f"# of Flying: {len(Flying)}\t{Flying}")
            print(f"# of Landing: {len(Landing_latency)}\t{Landing_latency}")
        if len(Flying) + len(Landing_latency) != 0:
            LP_mLL_Data["Fly#"].append(index + 1)
            LP_mLL_Data["LandingProb"].append(len(Landing_latency) / (len(Flying) + len(Landing_latency)))
            LP_mLL_Data["MLandingLatency"].append(np.mean(Landing_latency))
    LP_mLL_Data["Group_Name"] = [GroupName] * len(LP_mLL_Data["Fly#"])
    LP_mLL_Data = pd.DataFrame(LP_mLL_Data)
    return LP_mLL_Data
def ReadData(GroupName, Flies_to_pick, Landing_Data_path):
    global Trial_num
    Landing_Data = pd.read_excel(Landing_Data_path)
    Landing_Data = Landing_Data.iloc[Flies_to_pick[0] - 1:Flies_to_pick[1]]

    GroupNameCol = [GroupName] * (Flies_to_pick[1] - Flies_to_pick[0] + 1)
    Landing_Data["Group_Name"] = GroupNameCol
    return Landing_Data
def CalculateLPAndmLLAcrossFlies(GroupName, Landing_Data, fps):
    global FilterHighLatency
    global trial_offset
    global latency_threshold
    LP_mLL_Data = dict()
    LP_mLL_Data["LandingProb"] = []
    LP_mLL_Data["MLandingLatency"] = []
    LP_mLL_Data["Fly#"] = []
    Trials = ["Trial_" + str(i + 1 + trial_offset) for i in range(Trial_num - trial_offset)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        if FilterHighLatency:
            Landing_latency = [l / fps for l in row if not isinstance(l, str) and l > 0 and l < latency_threshold * fps]
            Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str) or n < -1]
            Flying = [f for f in row if not (isinstance(f, str) or pd.isna(f)) and (f == -1 or f >= latency_threshold * fps)]
        else:
            Landing_latency = [l / fps for l in row if not isinstance(l, str) and l > 0]
            Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str)]
            Flying = [f for f in row if not (isinstance(f, str) or pd.isna(f)) and (f == -1)]
        if len(Nan_data) + len(Flying) + len(Landing_latency) != Trial_num - trial_offset:
            print(f"Error while filtering data")
            print(f"Index: {index}")
            print(f"# of Nan: {len(Nan_data)}\t{Nan_data}")
            print(f"# of Flying: {len(Flying)}\t{Flying}")
            print(f"# of Landing: {len(Landing_latency)}\t{Landing_latency}")
        if len(Flying) + len(Landing_latency) != 0:
            LP_mLL_Data["Fly#"].append(index + 1)
            LP_mLL_Data["LandingProb"].append(len(Landing_latency) / (len(Flying) + len(Landing_latency)))
            LP_mLL_Data["MLandingLatency"].append(np.mean(Landing_latency))
    LP_mLL_Data["Group_Name"] = [GroupName] * len(LP_mLL_Data["Fly#"])
    LP_mLL_Data = pd.DataFrame(LP_mLL_Data)
    return LP_mLL_Data
def GetTrial_Landing_Data(LandingData, group_name, fps):
    landing_data = []
    global trial_offset
    global FilterHighLatency
    global latency_threshold
    Trials = ["Trial_" + str(i + 1 + trial_offset) for i in range(Trial_num - trial_offset)]
    LandingData = LandingData[Trials]

    for index, row in LandingData.iterrows():
        t = 0
        # print(row)
        for data in row.values:
            if FilterHighLatency:
                if not (isinstance(data, str) or pd.isna(data) or float(data) == -1 or data > latency_threshold * fps):
                    # print(group_name, index, t + trial_offset)
                    landing_data.append(data/fps)
                    t += 1
            else:
                if not (isinstance(data, str) or pd.isna(data) or float(data) == -1):
                    # print(group_name, index, t + trial_offset)
                    landing_data.append(data/fps)
                    t += 1
        # print(t)
    landing_data = pd.DataFrame(
        {
            "TrialLandingLatency": landing_data,
            "Group_Name": [group_name] * len(landing_data)
        }
    )
    # print(group_name, len(landing_data))
    return landing_data
def CalculateNFProbability(GroupName, Landing_Data):
    global FilterHighLatency
    NF_Data = dict()
    NF_Data["NotFlyingProb"] = []
    NF_Data["Fly#"] = []
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        NotFlying = [nf for nf in row if isinstance(nf, str)]
        Flying = [f for f in row if isinstance(f, int) or isinstance(f, float)]

        NF_Data["Fly#"].append(index + 1)
        NF_Data["NotFlyingProb"].append(len(NotFlying) / (len(NotFlying) + len(Flying)))
    NF_Data["Group_Name"] = [GroupName] * Landing_Data.shape[0]
    NF_Data = pd.DataFrame(NF_Data)
    return NF_Data
def Cumulative_Histplot_LL(Original_Data):

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
    # combined_df = pd.concat(Original_Data)
    for i, d in enumerate(Original_Data):
        sns.kdeplot(d["TrialLandingLatency"], alpha=0.8, color=Color_blind_palette[i], cumulative=True, legend=True, linewidth=3)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25)
    plt.tick_params(width=3, length=10)
    sns.despine(trim=True)
    ax.spines["left"].set_linewidth(2)  # Top border
    ax.spines["bottom"].set_linewidth(2)
    ax.set_xlabel("Landing latency (s)", fontsize=25)
    ax.set_ylabel("Percentage (%)", fontsize=25)
    plt.tight_layout()
    plt.show()
    return None
def ecdfPlot(Original_Data, filename):
    global labels
    global lines
    global latency_threshold
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    legend_handles = []  # List to store legend handles
    legend_labels = []
    # legend_labels = ["ON", "OFF"]
    # combined_df = pd.concat(Original_Data)

    for i, d in enumerate(Original_Data):
        print(d)
        sns.ecdfplot(d["TrialLandingLatency"], alpha=0.8, color=Color_blind_palette[i], linestyle=lines[i], legend=True, linewidth=3)
        legend_handles.append(Line2D([0], [0], color=Color_blind_palette[i], linestyle=lines[i], lw=3))
        # print(d["Group_Name"][0])
        legend_labels.append(d["Group_Name"].iloc[2])
    if FilterHighLatency:
        ax.set_xlim(-0.1, latency_threshold + 0.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xticks([0, latency_threshold])
        ax.set_yticks([0, 0.5, 1])
    else:
        ax.set_xlim(-0.1, 3.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xticks([0, 1.5, 3])
        ax.set_yticks([0, 0.5, 1])
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25)
    plt.tick_params(width=3, length=10)
    sns.despine(trim=True)
    ax.spines["left"].set_linewidth(2)  # Top border
    ax.spines["bottom"].set_linewidth(2)
    ax.set_xlabel("Landing latency (s)", fontsize=25)
    ax.set_ylabel("Percentage", fontsize=25)

    ax.legend(legend_handles, legend_labels, fontsize=20, loc="lower right", frameon=True)
    plt.tight_layout()
    plt.savefig(f"{filename}.pdf")
    plt.show()
    return None
def make_group_table(values, group_names=None):
    n = len(values)

    if group_names is None:
        group_names = [f"Group {i + 1}" for i in range(n)]

    df = pd.DataFrame(values, columns=group_names, index=group_names)
    df.index.name = "Groups"

    return df
def ReadLandingData(FileName, GroupName, FPS, FirstFly, LastFly):
    FilterdData = ReadAndFilterData(GroupName, [FirstFly, LastFly], FileName)
    LPData = CalculateLPAndmLLAcrossFlies(GroupName, FilterdData, FPS)
    LLData = GetTrial_Landing_Data(FilterdData, GroupName, FPS)
    return LPData, LLData
def ReadOptogeneticData(ONFile, OFFFile, GroupName, FPS, FirstFly, LastFly):
    ONFiltered, OFFFiltered = ReadAndFilterOptogeneticData(GroupName, [FirstFly, LastFly], [ONFile, OFFFile])
    ONLPData = CalculateLPAndmLLAcrossFlies(GroupName + "-ON", ONFiltered, FPS)
    ONLLData = GetTrial_Landing_Data(ONFiltered, GroupName + "-ON", FPS)
    OFFLPData = CalculateLPAndmLLAcrossFlies(GroupName + "-OFF", OFFFiltered, FPS)
    OFFLLData = GetTrial_Landing_Data(OFFFiltered, GroupName + "-OFF", FPS)
    return ONLPData, ONLLData, OFFLPData, OFFLLData

FilterHighLatency = True
samejoint = False
OPTO = True
Trial_num = 15
vio = False
Threshold = True
trial_offset = 0
DataFolder = r"C:\Users\agrawal-admin\Desktop\LandingDataSummary"

# latency_threshold = 0.5
latency_threshold = 0.71
T1CTF_path = os.path.join(DataFolder, r"6LegsLP\T1-CxTrLP.xlsx")
T1CTF_LP, T1CTF_LL = ReadLandingData(T1CTF_path, r"WT-T1-CxTr", 250, 1, 15)

T2CTF_path = os.path.join(DataFolder, r"6LegsLP\T2-CxTrLP.xlsx")
T2CTF_LP, T2CTF_LL = ReadLandingData(T2CTF_path, r"WT-T2-CxTr", 250, 1, 18)

T1CTF_SL_path = os.path.join(DataFolder, r"Necessity\T1RightIntact_CTF_LL_All.xlsx")
T1CTF_SL_LP, T1CTF_SL_LL = ReadLandingData(T1CTF_SL_path, r"WT-SL-T1-CxTr", 300, 1, 21)

T2CTF_SL_path = os.path.join(DataFolder, r"Necessity\T2RightIntact_CTF_LL_All.xlsx")
T2CTF_SL_LP, T2CTF_SL_LL = ReadLandingData(T2CTF_SL_path, r"WT-SL-T2-CxTr", 300, 1, 20)

T3CTF_path = os.path.join(DataFolder, r"6LegsLP\T3-CxTrLP.xlsx")
T3CTF_LP, T3CTF_LL = ReadLandingData(T3CTF_path, r"WT-T3-CxTr", 250, 1, 17)

T3CTF_SL_path = os.path.join(DataFolder, r"Necessity\T3RightIntact_CTF_LL_All.xlsx")
T3CTF_SL_LP, T3CTF_SL_LL = ReadLandingData(T3CTF_SL_path, r"WT-SL-T3-CxTr", 300, 1, 20)



T1TTa_path = os.path.join(DataFolder, r"6LegsLP\T1-TiTaLP.xlsx")
T1TTa_LP200FPS, T1TTa_LL200FPS = ReadLandingData(T1TTa_path, r"WT-T1-TiTa", 200, 1, 12)
T1TTa_LP250FPS, T1TTa_LL250FPS = ReadLandingData(T1TTa_path, r"WT-T1-TiTa", 250, 13, 15)
T1TTa_LP = pd.concat([T1TTa_LP200FPS, T1TTa_LP250FPS])
T1TTa_LL = pd.concat([T1TTa_LL200FPS, T1TTa_LL250FPS])


T2TTa_path = os.path.join(DataFolder, r"6LegsLP\T2-TiTaLP.xlsx")
T2TTa_LP, T2TTa_LL = ReadLandingData(T2TTa_path, r"WT-T2-TiTa", 200, 1, 15)

T2TTa_SL_path = os.path.join(DataFolder, r"Necessity\T2RightIntact_TTa_All.xlsx")
T2TTa_SL_LP, T2TTa_SL_LL = ReadLandingData(T2TTa_SL_path, r"WT-SL-T2-TiTa", 300, 1, 21)

T2TTa_inward_path = os.path.join(DataFolder, r"Others\WT-T2-TiTa_OT_filtered.xlsx")
T2TTa_inward_LP, T2TTa_inward_LL = ReadLandingData(T2TTa_inward_path, r"WT-IN", 200, 1, 15)

T2TTa_outward_path = os.path.join(DataFolder, r"Others\WT-T2-TiTa_IT_filtered.xlsx")
T2TTa_outward_LP, T2TTa_outward_LL = ReadLandingData(T2TTa_outward_path, r"WT-OUT", 200, 1, 15)

T3TTa_path = os.path.join(DataFolder, r"6LegsLP\T3-TiTaLP.xlsx")
T3TTa_LP200FPS, T3TTa_LL200FPS = ReadLandingData(T3TTa_path, r"WT-T3-TiTa", 200, 1, 15)
T3TTa_LP250FPS, T3TTa_LL250FPS = ReadLandingData(T3TTa_path, r"WT-T3-TiTa", 250, 16, 20)
T3TTa_LP = pd.concat([T3TTa_LP200FPS, T3TTa_LP250FPS])
T3TTa_LL = pd.concat([T3TTa_LL200FPS, T3TTa_LL250FPS])

T3TTa_SL_path = os.path.join(DataFolder, r"Necessity\T3RightIntact_TTa_All.xlsx")
T3TTa_SL_LP, T3TTa_SL_LL = ReadLandingData(T3TTa_SL_path, r"WT-SL-T3-TiTa", 300, 1, 17)

T2_TTa_Ab_path = os.path.join(DataFolder, r"CONTROL\WT-Abdomen-ALL.xlsx")
T2_TTa_Ab_LP, T2_TTa_Ab_LL = ReadLandingData(T2_TTa_Ab_path, r"WT Abdomen", 250, 1, 11)

T3Cut_path = os.path.join(DataFolder, r"CONTROL\WT-Ab-LegCutOff-ALL.xlsx")
T3Cut_LP, T3Cut_LL = ReadLandingData(T3Cut_path, r"WT Ab T3CutOff", 250, 1, 10)

NoContact_path = os.path.join(DataFolder, r"CONTROL\IntactFly_Control.xlsx")
NoContact_LP, NoContact_LL = ReadLandingData(NoContact_path, r"No contact", 300, 1, 10)

CSS39_path = os.path.join(DataFolder, r"KIR\CSS-0039_T2-TiTa-ALL.xlsx")
CSS39_LP, CSS39_LL = ReadLandingData(CSS39_path, r"CSS39", 250, 1, 15)

CSS48_path = os.path.join(DataFolder, r"KIR\CSS-0048_T2-TiTa-ALL.xlsx")
CSS48_LP, CSS48_LL = ReadLandingData(CSS48_path, r"CSS48", 250, 1, 17)

HP1_path = os.path.join(DataFolder, r"KIR\G106-HP1_T2-TiTa-ALL.xlsx")
HP1_LP, HP1_LL = ReadLandingData(HP1_path, r"HP-1", 250, 1, 16)

HP2_path = os.path.join(DataFolder, r"KIR\G107-HP2_T2-TiTa-ALL.xlsx")
HP2_LP, HP2_LL = ReadLandingData(HP2_path, r"HP-2", 250, 1, 14)

HP3_path = os.path.join(DataFolder, r"KIR\G108-HP3_T2-TiTa-ALL.xlsx")
HP3_LP, HP3_LL = ReadLandingData(HP3_path, r"HP-3", 250, 1, 17)


ClFl_path = os.path.join(DataFolder, r"KIR\G114-ClFl_T2-TiTa-ALL.xlsx")
ClFl_LP, ClFl_LL = ReadLandingData(ClFl_path, r"CL-FL", 250, 1, 16)

ClFl_path = os.path.join(DataFolder, r"Others\G114-ClFl_outward_filtered.xlsx")
ClFl_LP_inward, ClFl_LL_inward = ReadLandingData(ClFl_path, r"CL-FL-IN", 250, 1, 16)

ClFl_path = os.path.join(DataFolder, r"Others\G114-ClFl_inward_filtered.xlsx")
ClFl_LP_outward, ClFl_LL_outward = ReadLandingData(ClFl_path, r"CL-FL-OUT", 250, 1, 16)


ClEx_path = os.path.join(DataFolder, r"KIR\G116-ClEx_T2-TiTa-ALL.xlsx")
ClEx_LP, ClEx_LL = ReadLandingData(ClEx_path, r"CL-EX", 250, 1, 18)

HkFl_path = os.path.join(DataFolder, r"KIR\G117-HkFl_T2-TiTa-ALL.xlsx")
HkFl_LP, HkFl_LL = ReadLandingData(HkFl_path, r"HK-FL", 250, 1, 18)

HkEx_path = os.path.join(DataFolder, r"KIR\G118-HkEx_T2-TiTa-ALL.xlsx")
HkEx_LP, HkEx_LL = ReadLandingData(HkEx_path, r"HK-EX", 250, 1, 15)

HkEx_path = os.path.join(DataFolder, r"Others\G118-HkEx_outward_filtered.xlsx")
HkEx_LP_inward, HkEx_LL_inward = ReadLandingData(HkEx_path, r"HK-EX-IN", 250, 1, 15)

HkEx_path = os.path.join(DataFolder, r"Others\G118-HkEx_inward_filtered.xlsx")
HkEx_LP_outward, HkEx_LL_outward = ReadLandingData(HkEx_path, r"HK-EX-OUT", 250, 1, 15)


Club_path = os.path.join(DataFolder, r"KIR\G119-Club_T2-TiTa-ALL.xlsx")
Club_LP, Club_LL = ReadLandingData(Club_path, r"Club", 250, 1, 18)

Iav_path = os.path.join(DataFolder, r"KIR\G115-Iav_T2-TiTa-ALL.xlsx")
Iav_LP, Iav_LL = ReadLandingData(T1TTa_path, r"Iav", 250, 1, 16)


if OPTO:
    Trial_num = 15
    trial_offset = 0
    ANxGTACR_MAX_ON_path = os.path.join(DataFolder, r"OPTO\ANxGTACR-12mW-ON.xlsx")
    ANxGTACR_MAX_OFF_path = os.path.join(DataFolder, r"OPTO\ANxGTACR-12mW-OFF.xlsx")
    ANxGTACR_MAX_LO_LP, ANxGTACR_MAX_LO_LL, ANxGTACR_MAX_NL_LP, ANxGTACR_MAX_NL_LL = ReadOptogeneticData(ANxGTACR_MAX_ON_path, ANxGTACR_MAX_OFF_path, r"AN", 250, 1, 14)

    EmptyxGTACR_LO_path = os.path.join(DataFolder, r"OPTO\MTGal4xGTACR-12mW-ON.xlsx")
    EmptyxGTACR_NL_path = os.path.join(DataFolder, r"OPTO\MTGal4xGTACR-12mW-OFF.xlsx")
    EmptyxGTACR_LO_LP, EmptyxGTACR_LO_LL, EmptyxGTACR_NL_LP, EmptyxGTACR_NL_LL = ReadOptogeneticData(EmptyxGTACR_LO_path, EmptyxGTACR_NL_path, r"EmptyGal4", 250, 1, 15)

    CSS048xGTACR_LO_path = os.path.join(DataFolder, r"OPTO\CS048xGTACR-12mW-ON.xlsx")
    CSS048xGTACR_NL_path = os.path.join(DataFolder, r"OPTO\CS048xGTACR-12mW-OFF.xlsx")
    CSS048xGTACR_LO_LP, CSS048xGTACR_LO_LL, CSS048xGTACR_NL_LP, CSS048xGTACR_NL_LL = ReadOptogeneticData(CSS048xGTACR_LO_path, CSS048xGTACR_NL_path, r"CSS48", 250, 1, 22)

    L006xL011_max_LO_path = os.path.join(DataFolder, r"OPTO\TaBRIxLexAG-12mW-ON.xlsx")
    L006xL011_max_NL_path = os.path.join(DataFolder, r"OPTO\TaBRIxLexAG-12mW-OFF.xlsx")
    L006xL011_max_LO_LP, L006xL011_max_LO_LL, L006xL011_max_NL_LP, L006xL011_max_NL_LL = ReadOptogeneticData(L006xL011_max_LO_path, L006xL011_max_NL_path, r"Ta-Br", 250, 1, 15)

    GTACRxCSS21_max_LO_path = os.path.join(DataFolder, r"OPTO\CSS021xGTACR-12mW-ON.xlsx")
    GTACRxCSS21_max_NL_path = os.path.join(DataFolder, r"OPTO\CSS021xGTACR-12mW-OFF.xlsx")
    GTACRxCSS21_max_LO_LP, GTACRxCSS21_max_LO_LL, GTACRxCSS21_max_NL_LP, GTACRxCSS21_max_NL_LL = ReadOptogeneticData(GTACRxCSS21_max_LO_path, GTACRxCSS21_max_NL_path, r"CSS21", 250, 1, 19)

    GTACRxIav_max_LO_path = os.path.join(DataFolder, r"OPTO\IAVxGTACR-12mW-ON.xlsx")
    GTACRxIav_max_NL_path = os.path.join(DataFolder, r"OPTO\IAVxGTACR-12mW-OFF.xlsx")
    GTACRxIav_max_LO_LP, GTACRxIav_max_LO_LL, GTACRxIav_max_NL_LP, GTACRxIav_max_NL_LL = ReadOptogeneticData(GTACRxIav_max_LO_path, GTACRxIav_max_NL_path, r"IAV", 250, 1, 17)

    WTMax_LO_path = os.path.join(DataFolder, r"OPTO\WTxGREEN-12mW-ON.xlsx")
    WTMax_NL_path = os.path.join(DataFolder, r"OPTO\WTxGREEN-12mW-OFF.xlsx")
    WTMax_LO_LP, WTMax_LO_LL, WTMax_NL_LP, WTMax_NL_LL = ReadOptogeneticData(WTMax_LO_path, WTMax_NL_path, r"WT", 250, 1, 9)

# lines = ["dashed", "dashed", "dashed", "dashed", "dashed", "dashed", "dashed", "dashed", "dashed", "solid", "solid", "solid"]
lines = ["solid", "solid", "solid", "solid", "solid", "solid", "solid", "solid", "solid","solid","solid","solid"]
markers = ["o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "o", "o"]

# Choose a colormap (e.g., viridis, plasma, coolwarm, etc.)
cmap = cm.get_cmap('viridis', 12)

# Generate list of colors
colors = [cmap(i) for i in range(12)]
Color_blind_palette = ["blue", "green", "orange", "dodgerblue", "lawngreen", "orange"]
Color_blind_palette = ["blue", "peru", "sandybrown", "olive", "darkkhaki", "gold", "darkgreen", "seagreen", "mediumseagreen", "mediumaquamarine", "lightseagreen", "teal"]

LP_data_type = "LandingProb"
LL_data_type = "TrialLandingLatency"

Color_blind_palette = ["blue", "red", "green", "dodgerblue", "orange", "lawngreen", "orange"]
# Color_blind_palette = ["indigo", "deepskyblue", "orangered"]

"""
Color_blind_palette = ["deepskyblue", "orangered", "indigo"]
LPAcrossFlies([T2TTa_inward_LP, T2TTa_outward_LP],"INvsOUT-WT-LP")
ecdfPlot([T2TTa_inward_LL, T2TTa_outward_LL], "INvsOUT-WT-LL")

Data_type = "LandingProb"
print("WT-IT vs OT LP", Bootstrapping_test(T2TTa_inward_LP[Data_type], T2TTa_outward_LP[Data_type]))
Data_type = "TrialLandingLatency"
print("WT-IT vs OT LP", Bootstrapping_test(T2TTa_inward_LL[Data_type], T2TTa_outward_LL[Data_type]))"""

"""# Threshold = True
Color_blind_palette = ["blue", "red", "green", "dodgerblue", "orange", "lawngreen", "orange"]
LPAcrossFlies([T1TTa_LP, T2TTa_LP, T3TTa_LP, T1CTF_LP, T2CTF_LP, T3CTF_LP], "WT-LP")
ecdfPlot([T1TTa_LL, T2TTa_LL, T3TTa_LL, T1CTF_LL, T2CTF_LL, T3CTF_LL], "WT-LL")

Color_blind_palette = ["red", "green",  "dodgerblue", "orange", "lawngreen"]
LPAcrossFlies([T2TTa_SL_LP, T3TTa_SL_LP, T1CTF_SL_LP, T2CTF_SL_LP, T3CTF_SL_LP], "Ablation-LP")
ecdfPlot([T2TTa_SL_LL, T3TTa_SL_LL, T1CTF_SL_LL, T2CTF_SL_LL, T3CTF_SL_LL], "Ablation-LL")

Color_blind_palette = colors[:7]
LPAcrossFlies([T2TTa_LP, CSS39_LP, CSS48_LP, HP1_LP, HP2_LP, HP3_LP, Iav_LP], "KIR1-LP")
ecdfPlot([T2TTa_LL, CSS39_LL, CSS48_LL, HP1_LL, HP2_LL, HP3_LL, Iav_LL], "KIR1-LL")

Color_blind_palette = [colors[0]] + colors[7:]
LPAcrossFlies([T2TTa_LP, ClFl_LP, ClEx_LP, HkFl_LP, HkEx_LP, Club_LP], "KIR2-LP")
ecdfPlot([T2TTa_LL, ClFl_LL, ClEx_LL, HkFl_LL, HkEx_LL, Club_LL], "KIR2-LL")"""


c = "black"
Color_blind_palette = [c, c]
lines = ["dashed", "solid"]
LPAcrossLight([WTMax_LO_LP, WTMax_NL_LP], "WT-Green-LP", c)
ecdfPlot([WTMax_LO_LL, WTMax_NL_LL], "WT-Green-LL")

c = "blue"
Color_blind_palette = [c, c]
LPAcrossLight([EmptyxGTACR_LO_LP, EmptyxGTACR_NL_LP], "Empty-Gal4-LP", c)
ecdfPlot([EmptyxGTACR_LO_LL, EmptyxGTACR_NL_LL], "Empty-Gal4-LL")

c = "red"
Color_blind_palette = [c, c]
LPAcrossLight([CSS048xGTACR_LO_LP, CSS048xGTACR_NL_LP], "CSS048-LP", c)
ecdfPlot([CSS048xGTACR_LO_LL, CSS048xGTACR_NL_LL], "CSS048-LL")

c = "brown"
Color_blind_palette = [c, c]
LPAcrossLight([GTACRxIav_max_LO_LP, GTACRxIav_max_NL_LP], "IavxGTACR-LP", c)
ecdfPlot([GTACRxIav_max_LO_LL, GTACRxIav_max_NL_LL], "IavxGTACR-LL")

c = "orange"
Color_blind_palette = [c, c]
LPAcrossLight([GTACRxCSS21_max_LO_LP, GTACRxCSS21_max_NL_LP], "CSS021-LP", c)
ecdfPlot([GTACRxCSS21_max_LO_LL, GTACRxCSS21_max_NL_LL], "CSS021-LL")

c = "magenta"
Color_blind_palette = [c, c]
LPAcrossLight([ANxGTACR_MAX_LO_LP, ANxGTACR_MAX_NL_LP], "ANxGTACR-LP", c)
ecdfPlot([ANxGTACR_MAX_LO_LL, ANxGTACR_MAX_NL_LL], "ANxGTACR-LL")

c = "green"
Color_blind_palette = [c, c]
LPAcrossLight([L006xL011_max_LO_LP, L006xL011_max_NL_LP], "LexA_Br-G-LP", c)
ecdfPlot([L006xL011_max_LO_LL, L006xL011_max_NL_LL], "LexA_Br-G-LL")

Data_type = "LandingProb"
"""print("T1-TTa vs T2-TTa LP", Bootstrapping_test(T1TTa_LP[Data_type], T2TTa_LP[Data_type]))
print("T1-TTa vs T3-TTa LP", Bootstrapping_test(T1TTa_LP[Data_type], T3TTa_LP[Data_type]))
print("T2-TTa vs T3-TTa LP", Bootstrapping_test(T2TTa_LP[Data_type], T3TTa_LP[Data_type]))

print("T1-CTF vs T2-CTF LP", Bootstrapping_test(T1CTF_LP[Data_type], T2CTF_LP[Data_type]))
print("T1-CTF vs T3-CTF LP", Bootstrapping_test(T1CTF_LP[Data_type], T3CTF_LP[Data_type]))
print("T2-CTF vs T3-CTF LP", Bootstrapping_test(T2CTF_LP[Data_type], T3CTF_LP[Data_type]))

print("T1-TTa vs T1-CTF LP", Bootstrapping_test(T1TTa_LP[Data_type], T1CTF_LP[Data_type]))
print("T2-TTa vs T2-CTF LP", Bootstrapping_test(T2TTa_LP[Data_type], T2CTF_LP[Data_type]))
print("T3-TTa vs T3-CTF LP", Bootstrapping_test(T3TTa_LP[Data_type], T3CTF_LP[Data_type]))


print("T2-TTa-SL vs T3-TTa-SL LP", Bootstrapping_test(T2TTa_SL_LP[Data_type], T3TTa_SL_LP[Data_type]))
print("T2-TTa-SL vs T2-CTF-SL LP", Bootstrapping_test(T2TTa_SL_LP[Data_type], T2CTF_SL_LP[Data_type]))
print("T3-TTa-SL vs T3-CTF-SL LP", Bootstrapping_test(T3TTa_SL_LP[Data_type], T3CTF_SL_LP[Data_type]))

print("T1-CTF-SL vs T2-CTF-SL LP", Bootstrapping_test(T1CTF_SL_LP[Data_type], T2CTF_SL_LP[Data_type]))
print("T1-CTF-SL vs T3-CTF-SL LP", Bootstrapping_test(T1CTF_SL_LP[Data_type], T3CTF_SL_LP[Data_type]))
print("T2-CTF-SL vs T3-CTF-SL LP", Bootstrapping_test(T2CTF_SL_LP[Data_type], T3CTF_SL_LP[Data_type]))


print("WT vs CS39 LP", Bootstrapping_test(T2TTa_LP[Data_type], CSS39_LP[Data_type]))
print("WT vs CS48 LP", Bootstrapping_test(T2TTa_LP[Data_type], CSS48_LP[Data_type]))
print("WT vs HP1 LP", Bootstrapping_test(T2TTa_LP[Data_type], HP1_LP[Data_type]))
print("WT vs HP2 LP", Bootstrapping_test(T2TTa_LP[Data_type], HP2_LP[Data_type]))
print("WT vs HP3 LP", Bootstrapping_test(T2TTa_LP[Data_type], HP3_LP[Data_type]))
print("WT vs IAV LP", Bootstrapping_test(T2TTa_LP[Data_type], Iav_LP[Data_type]))
print("WT vs ClFl LP", Bootstrapping_test(T2TTa_LP[Data_type], ClFl_LP[Data_type]))
print("WT vs ClEx LP", Bootstrapping_test(T2TTa_LP[Data_type], ClEx_LP[Data_type]))
print("WT vs HkFl LP", Bootstrapping_test(T2TTa_LP[Data_type], HkFl_LP[Data_type]))
print("WT vs HkEx LP", Bootstrapping_test(T2TTa_LP[Data_type], HkEx_LP[Data_type]))
print("WT vs Club LP", Bootstrapping_test(T2TTa_LP[Data_type], Club_LP[Data_type]))"""

"""t_stat, p_value = ttest_rel(WTMax_LO_LP[Data_type], WTMax_NL_LP[Data_type])
print("WT-ON vs OFF", p_value)

t_stat, p_value = ttest_rel(EmptyxGTACR_LO_LP[Data_type], EmptyxGTACR_NL_LP[Data_type])
print("MTGal4-ON vs OFF", p_value)

t_stat, p_value = ttest_rel(CSS048xGTACR_LO_LP[Data_type], CSS048xGTACR_NL_LP[Data_type])
print("CSS48-ON vs OFF", p_value)

t_stat, p_value = ttest_rel(GTACRxIav_max_LO_LP[Data_type], GTACRxIav_max_NL_LP[Data_type])
print("IAV-ON vs OFF", p_value)

t_stat, p_value = ttest_rel(GTACRxCSS21_max_LO_LP[Data_type], GTACRxCSS21_max_NL_LP[Data_type])
print("CSS21-ON vs OFF", p_value)

t_stat, p_value = ttest_rel(ANxGTACR_MAX_LO_LP[Data_type], ANxGTACR_MAX_NL_LP[Data_type])
print("AN-ON vs OFF", p_value)

t_stat, p_value = ttest_rel(L006xL011_max_LO_LP[Data_type], L006xL011_max_NL_LP[Data_type])
print("Tar bri-ON vs OFF", p_value)"""


Data_type = "TrialLandingLatency"
"""print("T1-TTa vs T2-TTa LP", Bootstrapping_test(T1TTa_LL[Data_type], T2TTa_LL[Data_type]))
print("T1-TTa vs T3-TTa LP", Bootstrapping_test(T1TTa_LL[Data_type], T3TTa_LL[Data_type]))
print("T2-TTa vs T3-TTa LP", Bootstrapping_test(T2TTa_LL[Data_type], T3TTa_LL[Data_type]))

print("T1-CTF vs T2-CTF LP", Bootstrapping_test(T1CTF_LL[Data_type], T2CTF_LL[Data_type]))
print("T1-CTF vs T3-CTF LP", Bootstrapping_test(T1CTF_LL[Data_type], T3CTF_LL[Data_type]))
print("T2-CTF vs T3-CTF LP", Bootstrapping_test(T2CTF_LL[Data_type], T3CTF_LL[Data_type]))

print("T1-TTa vs T1-CTF LP", Bootstrapping_test(T1TTa_LL[Data_type], T1CTF_LL[Data_type]))
print("T2-TTa vs T2-CTF LP", Bootstrapping_test(T2TTa_LL[Data_type], T2CTF_LL[Data_type]))
print("T3-TTa vs T3-CTF LP", Bootstrapping_test(T3TTa_LL[Data_type], T3CTF_LL[Data_type]))


print("T2-TTa-SL vs T3-TTa-SL LP", Bootstrapping_test(T2TTa_SL_LL[Data_type], T3TTa_SL_LL[Data_type]))
print("T2-TTa-SL vs T2-CTF-SL LP", Bootstrapping_test(T2TTa_SL_LL[Data_type], T2CTF_SL_LL[Data_type]))
print("T3-TTa-SL vs T3-CTF-SL LP", Bootstrapping_test(T3TTa_SL_LL[Data_type], T3CTF_SL_LL[Data_type]))

print("T1-CTF-SL vs T2-CTF-SL LP", Bootstrapping_test(T1CTF_SL_LL[Data_type], T2CTF_SL_LL[Data_type]))
print("T1-CTF-SL vs T3-CTF-SL LP", Bootstrapping_test(T1CTF_SL_LL[Data_type], T3CTF_SL_LL[Data_type]))
print("T2-CTF-SL vs T3-CTF-SL LP", Bootstrapping_test(T2CTF_SL_LL[Data_type], T3CTF_SL_LL[Data_type]))


print("WT vs CS39 LP", Bootstrapping_test(T2TTa_LL[Data_type], CSS39_LL[Data_type]))
print("WT vs CS48 LP", Bootstrapping_test(T2TTa_LL[Data_type], CSS48_LL[Data_type]))
print("WT vs HP1 LP", Bootstrapping_test(T2TTa_LL[Data_type], HP1_LL[Data_type]))
print("WT vs HP2 LP", Bootstrapping_test(T2TTa_LL[Data_type], HP2_LL[Data_type]))
print("WT vs HP3 LP", Bootstrapping_test(T2TTa_LL[Data_type], HP3_LL[Data_type]))
print("WT vs IAV LP", Bootstrapping_test(T2TTa_LL[Data_type], Iav_LL[Data_type]))
print("WT vs ClFl LP", Bootstrapping_test(T2TTa_LL[Data_type], ClFl_LL[Data_type]))
print("WT vs ClEx LP", Bootstrapping_test(T2TTa_LL[Data_type], ClEx_LL[Data_type]))
print("WT vs HkFl LP", Bootstrapping_test(T2TTa_LL[Data_type], HkFl_LL[Data_type]))
print("WT vs HkEx LP", Bootstrapping_test(T2TTa_LL[Data_type], HkEx_LL[Data_type]))
print("WT vs Club LP", Bootstrapping_test(T2TTa_LL[Data_type], Club_LL[Data_type]))"""

"""print("WT-ON vs OFF", Bootstrapping_test(WTMax_LO_LL[Data_type], WTMax_NL_LL[Data_type]))
print("MTGal4-ON vs OFF", Bootstrapping_test(EmptyxGTACR_LO_LL[Data_type], EmptyxGTACR_NL_LL[Data_type]))
print("CSS48-ON vs OFF", Bootstrapping_test(CSS048xGTACR_LO_LL[Data_type], CSS048xGTACR_NL_LL[Data_type]))
print("IAV-ON vs OFF", Bootstrapping_test(GTACRxIav_max_LO_LL[Data_type], GTACRxIav_max_NL_LL[Data_type]))
print("CSS21-ON vs OFF", Bootstrapping_test(GTACRxCSS21_max_LO_LL[Data_type], GTACRxCSS21_max_NL_LL[Data_type]))
print("AN-ON vs OFF", Bootstrapping_test(ANxGTACR_MAX_LO_LL[Data_type], ANxGTACR_MAX_NL_LL[Data_type]))
print("Tar bri-ON vs OFF", Bootstrapping_test(L006xL011_max_LO_LL[Data_type], L006xL011_max_NL_LL[Data_type]))"""
"""def median_mad(x, scale=True):
    x = np.asarray(x)
    x = x[~np.isnan(x)]  # remove NaNs if needed

    med = np.median(x)
    mad = np.median(np.abs(x - med))

    if scale:
        mad *= 1.4826  # make comparable to std

    return med, mad
med, mad = median_mad(T2TTa_LL["TrialLandingLatency"])
sns.histplot(T2TTa_LL["TrialLandingLatency"], bins=50, stat="probability")
plt.axvline(med, color="red", label="median")
plt.axvline(med - mad, color="blue", label="1MAD")
plt.axvline(med + mad, color="blue")
plt.axvline(med - 2 * mad, color="green", label="2MAD")
plt.axvline(med + 2 * mad, color="green")
plt.xticks([0, 0.5, 1, 1.5, 2])
plt.yticks([0, 0.2])
plt.legend()
print(med)
print(med + 2 * mad)
print(med + mad)
plt.savefig("T2-Landing latency distribution.pdf")
plt.show()"""