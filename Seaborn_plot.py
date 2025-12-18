import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
import numpy as np
from sklearn.utils import resample
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from scipy.stats import kendalltau
import colorsys
# Apply the default theme
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
def brighten_color(color, factor=0.2):
    # Add the factor to each channel, but ensure it's capped at 1
    return tuple(min(1, c + factor) for c in color)
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
    ax = sns.stripplot(x="Group_Name", y="TrialLandingLatency", data=combined_df, jitter=0.2, size=20, alpha=0.4, marker="o", palette=Color_blind_palette)
    """for i, group_data in enumerate(Original_Data, start=1):
        if samejoint:
            ax = sns.stripplot(x="Group_Name", y="TrialLandingLatency", data=group_data, jitter=0.2, size=20, alpha=0.75, marker=markers[i - 1], color=Color_blind_palette[0])
        else:
            #ax = sns.violinplot(x="Group_Name", y="TrialLandingLatency", data=group_data, color=Color_blind_palette[i-1],
            #                    split=True, hue=0, hue_order=[1, 0], dodge=True, legend=False)
            #ax = sns.stripplot(x="Group_Name", y="TrialLandingLatency", data=group_data, jitter=0.2, size=30, alpha=0.4,
            #                   hue=0, hue_order=[2, 1, 0, -1, -2, -3, -4], dodge=True, legend=False,  marker=markers[i - 1],
            #                   color=lightened_palette[i-1])
            ax = sns.stripplot(x="Group_Name", y="TrialLandingLatency", data=group_data, jitter=0.2, size=30, alpha=0.4, dodge=True, legend=False,
                               marker=markers[i - 1],
                               color=lightened_palette[i - 1])"""

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
        plt.ylim(-0.3, 1.1)
        plt.yticks([0, 0.5, 1])
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

    print(f"Difference in mean's P-value = {Mean_diff_p_value}")
    print(f"Original mean diff = {original_mean_diff}")
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
                # g = sns.violinplot(x="Group_Name", y="LandingProb", data=d, color=Color_blind_palette[i])
            # g = sns.stripplot(x="Group_Name", y="LandingProb", data=combined_df, alpha=0.75, jitter=0.2, dodge=False, size=20, hue="Group_Name", palette=Color_blind_palette)
        else:
            g = sns.violinplot(x="Group_Name", y="LandingProb", hue="Group_Name", data=combined_df, palette=Color_blind_palette)
    g.spines['left'].set_linewidth(3)
    g.spines['bottom'].set_linewidth(3)
    g.set_ylim(-0.1, 1.1)

    group_stat = combined_df.groupby('Group_Name')['LandingProb'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2, zorder=10)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10, zorder=10)
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
    combined_df = pd.concat(Data_to_plot, ignore_index=True)
    plt.figure(figsize=(len(Data_to_plot) * 4, 10))

    # Sort by Fly# to keep connection consistent
    combined_df = combined_df.sort_values(by=['Fly#', 'Group_Name'])

    g = sns.pointplot(data=combined_df, x='Group_Name', y='LandingProb', ci=None, dodge=True, color=color, join=False)

    # Connect same flies with lines
    for fly_id, group in combined_df.groupby('Fly#'):
        plt.plot(group['Group_Name'], group['LandingProb'], marker='o', markersize=20,  color="lightgrey", linewidth=5)

    mean_df = combined_df.groupby('Group_Name', as_index=False)['LandingProb'].mean()
    plt.plot(mean_df['Group_Name'], mean_df['LandingProb'], color=color, marker='o', markersize=20, linewidth=5, label='Mean')

    plt.title('Change in Landing Probability Across Groups')
    plt.ylabel('Landing Probability')
    plt.xlabel('Group')
    g.spines['left'].set_linewidth(3)
    g.spines['bottom'].set_linewidth(3)
    # plt.legend(handles=legend_elements, loc='upper right', fontsize=20)
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
    plt.show()
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
    LP_mLL_Data = dict()
    LP_mLL_Data["LandingProb"] = []
    LP_mLL_Data["MLandingLatency"] = []
    LP_mLL_Data["Fly#"] = []
    Trials = ["Trial_" + str(i + 1 + trial_offset) for i in range(Trial_num - trial_offset)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        if FilterHighLatency:
            Landing_latency = [l / fps for l in row if not isinstance(l, str) and l > 0 and l < 1 * fps]
            Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str) or n < -1]
            Flying = [f for f in row if not (isinstance(f, str) or pd.isna(f)) and (f == -1 or f >= 1 * fps)]
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
    LP_mLL_Data = dict()
    LP_mLL_Data["LandingProb"] = []
    LP_mLL_Data["MLandingLatency"] = []
    LP_mLL_Data["Fly#"] = []
    Trials = ["Trial_" + str(i + 1 + trial_offset) for i in range(Trial_num - trial_offset)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        if FilterHighLatency:
            Landing_latency = [l / fps for l in row if not isinstance(l, str) and l > 0 and l < 1 * fps]
            Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str) or n < -1]
            Flying = [f for f in row if not (isinstance(f, str) or pd.isna(f)) and (f == -1 or f >= 1 * fps)]
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
    Trials = ["Trial_" + str(i + 1 + trial_offset) for i in range(Trial_num - trial_offset)]
    LandingData = LandingData[Trials]

    for index, row in LandingData.iterrows():
        t = 0
        # print(row)
        for data in row.values:
            if FilterHighLatency:
                if not (isinstance(data, str) or pd.isna(data) or float(data) == -1 or data > 1 * fps):
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
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
    legend_handles = []  # List to store legend handles
    legend_labels = []
    # combined_df = pd.concat(Original_Data)
    for i, d in enumerate(Original_Data):
        legend_labels.append(d["Group_Name"][0])
        sns.ecdfplot(d["TrialLandingLatency"], alpha=0.8, color=Color_blind_palette[i], linestyle=lines[i], legend=True, linewidth=3)
        legend_handles.append(Line2D([0], [0], color=Color_blind_palette[i], linestyle=lines[i], lw=3))
    if FilterHighLatency:
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xticks([0, 0.5, 1])
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
def ecdfPlotLP(Original_Data):
    from matplotlib.lines import Line2D
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
    legend_handles = []  # List to store legend handles
    legend_labels = ["G106 Manual", "G106 Predicted", "G107", "G115"]  #
    # combined_df = pd.concat(Original_Data)
    for i, d in enumerate(Original_Data):
        sns.ecdfplot(d["LandingProb"], alpha=0.8, color=Color_blind_palette[i], legend=True, linewidth=3)
        legend_handles.append(Line2D([0], [0], color=Color_blind_palette[i], lw=3))
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
    ax.set_xlabel("Landing probability", fontsize=25)
    ax.set_ylabel("Percentage (%)", fontsize=25)

    ax.legend(legend_handles, legend_labels, fontsize=20, loc="lower right", frameon=True)
    plt.tight_layout()
    plt.show()
    return None

def cross_comparison(exp_groups):
    names = []
    p_values = []
    for i in range(len(exp_groups)):
        names.append(exp_groups[i][1])
        p_values.append([])
        for j in range(len(exp_groups)):
            p_values[-1].append(Bootstrapping_test(exp_groups[i][0], exp_groups[j][0]))
    make_group_table(p_values, group_names=names)
def make_group_table(values, group_names=None):
    n = len(values)

    if group_names is None:
        group_names = [f"Group {i + 1}" for i in range(n)]

    df = pd.DataFrame(values, columns=group_names, index=group_names)
    df.index.name = "Groups"

    return df

group_name = ["WT-CTF",
              "Kir Control CTF",
              "Fe-Gal4 CTF",
              "HP-Gal4 CTF"]

FilterHighLatency = True
samejoint = False
Trial_num = 15
trial = [str(t+1) for t in range(Trial_num)]
Trial = [f"Trial_{t + 1}" for t in range(Trial_num)]

Color_blind_palette = sns.color_palette("Set2", n_colors=10)


markers = ['o', 'o', 'o', '>', '>','>', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']

vio = False
# ReadData = True
trial_offset = 0
T1TTa_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\T1-TiTaLP.xlsx"
T1TTa_200FPS = ReadAndFilterData(r"WT-T1-TiTa", [1, 12], T1TTa_path)
T1TTa_250FPS = ReadAndFilterData(r"WT-T1-TiTa", [13, 15], T1TTa_path)
T1TTa_LP_200FPS = CalculateLPAndmLLAcrossFlies(r"WT-T1-TiTa", T1TTa_200FPS, 200)
T1TTa_LL_200FPS = GetTrial_Landing_Data(T1TTa_200FPS, "WT-T1-TiTa", 200)
T1TTa_LP_250FPS = CalculateLPAndmLLAcrossFlies(r"WT-T1-TiTa", T1TTa_250FPS, 250)
T1TTa_LL_250FPS = GetTrial_Landing_Data(T1TTa_250FPS, "WT-T1-TiTa", 250)
T1TTa_LP = pd.concat([T1TTa_LP_200FPS, T1TTa_LP_250FPS])
T1TTa_LL = pd.concat([T1TTa_LL_200FPS, T1TTa_LL_250FPS])


T2TTa_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-T2-TiTaLP.xlsx"
T2TTa_Filtered = ReadAndFilterData(r"WT", [1, 15], T2TTa_path)
T2TTa_LP = CalculateLPAndmLLAcrossFlies(r"WT", T2TTa_Filtered, 200)
T2TTa_LL = GetTrial_Landing_Data(T2TTa_Filtered, "WT", 200)

T2TTa_SL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Ablation\T2RightIntact_TTa_All.xlsx"
T2TTa_SL = ReadAndFilterData(r"WT-SL-T2-TiTa", [1, 21], T2TTa_SL_path)
T2TTa_SL_LP = CalculateLPAndmLLAcrossFlies(r"WT-SL-T2-TiTa", T2TTa_SL, 300)
T2TTa_SL_LL = GetTrial_Landing_Data(T2TTa_SL, "WT-SL-T2-TiTa", 300)

T2TTa_inward_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\WT-T2-TiTa_inward_filtered.xlsx"
T2TTa_inward_Filtered = ReadData(r"WT-In Touch", [1, 15], T2TTa_inward_path)
T2TTa_inward_LP = CalculateLPAndmLLAcrossFlies(r"WT-In Touch", T2TTa_inward_Filtered, 200)
T2TTa_inward_LL = GetTrial_Landing_Data(T2TTa_inward_Filtered, "WT-In Touch", 200)
T2TTa_outward_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\WT-T2-TiTa_outward_filtered.xlsx"
T2TTa_outward_Filtered = ReadData(r"WT-Out Touch", [1, 15], T2TTa_outward_path)
T2TTa_outward_LP = CalculateLPAndmLLAcrossFlies(r"WT-Out Touch", T2TTa_outward_Filtered, 200)
T2TTa_outward_LL = GetTrial_Landing_Data(T2TTa_outward_Filtered, "WT-Ouy Touch", 200)


T2CTF_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\T2-CxTrLP.xlsx"
T2CTF_Filtered = ReadAndFilterData(r"WT-T2-CxTr", [1, 18], T2CTF_path)
T2CTF_LP = CalculateLPAndmLLAcrossFlies(r"WT-T2-CxTr", T2CTF_Filtered, 250)
T2CTF_LL = GetTrial_Landing_Data(T2CTF_Filtered, r"WT-T2-CxTr", 250)
T2CTF_SL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Ablation\T2RightIntact_CTF_LL_All.xlsx"
T2CTF_SL = ReadAndFilterData(r"WT-SL-T2-CxTr", [1, 20], T2CTF_SL_path)
T2CTF_SL_LP = CalculateLPAndmLLAcrossFlies(r"WT-SL-T2-CxTr", T2CTF_SL, 300)
T2CTF_SL_LL = GetTrial_Landing_Data(T2CTF_SL, r"WT-SL-T2-CxTr", 300)

T3TTa_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\T3-TiTaLP.xlsx"
T3TTa_200FPS = ReadAndFilterData(r"WT-T3-TiTa", [1, 15], T3TTa_path)
T3TTa_250FPS = ReadAndFilterData(r"WT-T3-TiTa", [16, 20], T3TTa_path)
T3TTa_LP_200FPS = CalculateLPAndmLLAcrossFlies(r"WT-T3-TiTa", T3TTa_200FPS, 200)
T3TTa_LL_200FPS = GetTrial_Landing_Data(T3TTa_200FPS, "WT-T3-TiTa", 200)
T3TTa_LP_250FPS = CalculateLPAndmLLAcrossFlies(r"WT-T3-TiTa", T3TTa_250FPS, 250)
T3TTa_LL_250FPS = GetTrial_Landing_Data(T3TTa_250FPS, "WT-T3-TiTa", 250)
T3TTa_LP = pd.concat([T3TTa_LP_200FPS, T3TTa_LP_250FPS])
T3TTa_LL = pd.concat([T3TTa_LL_200FPS, T3TTa_LL_250FPS])

T3TTa_SL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Ablation\T3RightIntact_TTa_All.xlsx"
T3TTa_SL = ReadAndFilterData(r"WT-SL-T3-TiTa", [1, 17], T3TTa_SL_path)
T3TTa_SL_LP = CalculateLPAndmLLAcrossFlies(r"WT-SL-T3-TiTa", T3TTa_SL, 300)
T3TTa_SL_LL = GetTrial_Landing_Data(T3TTa_SL, r"WT-SL-T3-TiTa", 300)

T1CTF_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\T1-TiTa-Data_TarsusContact.xlsx"
T1CTF = ReadAndFilterData(r"WT-T1-CxTr", [1, 15], T1CTF_path)
T1CTF_LP = CalculateLPAndmLLAcrossFlies(r"WT-T1-CxTr", T1CTF, 250)
T1CTF_LL = GetTrial_Landing_Data(T1CTF, r"WT-T1-CxTr", 250)

T1CTF_SL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Ablation\T1RightIntact_CTF_LL_All.xlsx"
T1CTF_SL = ReadAndFilterData(r"WT-SL-T1-CxTr", [1, 21], T1CTF_SL_path)
T1CTF_SL_LP = CalculateLPAndmLLAcrossFlies(r"WT-SL-T1-CxTr", T1CTF_SL, 300)
T1CTF_SL_LL = GetTrial_Landing_Data(T1CTF_SL, r"WT-SL-T1-CxTr", 300)


T3CTF_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\T3-CxTrLP.xlsx"
T3CTF_Filtered = ReadAndFilterData(r"WT-T3-CxTr", [1, 17], T3CTF_path)
T3CTF_LP = CalculateLPAndmLLAcrossFlies(r"WT-T3-CxTr", T3CTF_Filtered, 250)
T3CTF_LL = GetTrial_Landing_Data(T3CTF_Filtered, r"WT-T3-CxTr", 250)

T3CTF_SL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Ablation\T3RightIntact_CTF_LL_All.xlsx"
T3CTF_SL = ReadAndFilterData(r"WT-SL-T3-CxTr", [1, 20], T3CTF_SL_path)
T3CTF_SL_LP = CalculateLPAndmLLAcrossFlies(r"WT-SL-T3-CxTr", T3CTF_SL, 300)
T3CTF_SL_LL = GetTrial_Landing_Data(T3CTF_SL, r"WT-SL-T3-CxTr", 300)


T2_TTa_Ab_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\WT-Ab.xlsx"
T2_TTa_Ab = ReadAndFilterData(r"WT Abdomen", [1, 11], T2_TTa_Ab_path)
T2_TTa_Ab_LP = CalculateLPAndmLLAcrossFlies(r"WT Abdomen", T2_TTa_Ab, 250)
T2_TTa_Ab_LL = GetTrial_Landing_Data(T2_TTa_Ab, r"WT Abdomen", 250)

T3Cut_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\WTAbLegCut.xlsx"
T3Cut = ReadAndFilterData(r"WT Ab T3CutOff", [1, 10], T3Cut_path)
T3Cut_LP = CalculateLPAndmLLAcrossFlies(r"WT Ab T3CutOff", T3Cut, 250)
T3Cut_LL = GetTrial_Landing_Data(T3Cut, r"WT Ab T3CutOff", 250)

NoContact_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\WT-Others\WTNoContact.xlsx"
NoContact = ReadAndFilterData(r"No contact", [1, 10], NoContact_path)
NoContact_LP = CalculateLPAndmLLAcrossFlies(r"No contact", NoContact, 300)
NoContact_LL = GetTrial_Landing_Data(NoContact, r"No contact", 300)

HP1_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP1-T2-TiTaLP.xlsx"
HP1_Filtered = ReadAndFilterData(r"HP-1", [1, 16], HP1_path)
HP1_LP = CalculateLPAndmLLAcrossFlies(r"HP-1", HP1_Filtered, 250)
HP1_LL = GetTrial_Landing_Data(HP1_Filtered, "HP-1", 250)

HP2_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP2-T2-TiTaLP.xlsx"
HP2_Filtered = ReadAndFilterData(r"HP-2", [1, 14], HP2_path)
HP2_LP = CalculateLPAndmLLAcrossFlies(r"HP-2", HP2_Filtered, 250)
HP2_LL = GetTrial_Landing_Data(HP2_Filtered, "HP-2", 250)

HP3_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HP3-T2-TiTaLP.xlsx"
HP3_Filtered = ReadAndFilterData(r"HP-3", [1, 17], HP3_path)
HP3_LP = CalculateLPAndmLLAcrossFlies(r"HP-3", HP3_Filtered, 250)
HP3_LL = GetTrial_Landing_Data(HP3_Filtered, "HP-3", 250)

ClFl_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClFl-T2-TiTaLP.xlsx"
ClFl_Filtered = ReadAndFilterData(r"CL-FL", [1, 16], ClFl_path)
ClFl_LP = CalculateLPAndmLLAcrossFlies(r"CL-FL", ClFl_Filtered, 250)
ClFl_LL = GetTrial_Landing_Data(ClFl_Filtered, "CL-FL", 250)

ClEx_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\ClEx-T2-TiTaLP.xlsx"
ClEx_Filtered = ReadAndFilterData(r"CL-EX", [1, 18], ClEx_path)
ClEx_LP = CalculateLPAndmLLAcrossFlies(r"CL-EX", ClEx_Filtered, 250)
ClEx_LL = GetTrial_Landing_Data(ClEx_Filtered, "CL-EX", 250)

HkFl_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKFL-T2-TiTaLP.xlsx"
HkFl_Filtered = ReadAndFilterData(r"HK-FL", [1, 18], HkFl_path)
HkFl_LP = CalculateLPAndmLLAcrossFlies(r"HK-FL", HkFl_Filtered, 250)
HkFl_LL = GetTrial_Landing_Data(HkFl_Filtered, "HK-FL", 250)

HkEx_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\HKEX-T2-TiTaLP.xlsx"
HkEx_Filtered = ReadAndFilterData(r"HK-EX", [1, 15], HkEx_path)
HkEx_LP = CalculateLPAndmLLAcrossFlies(r"HK-EX", HkEx_Filtered, 250)
HkEx_LL = GetTrial_Landing_Data(HkEx_Filtered, "HK-EX", 250)

Club_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\CLUB-T2-TiTaLP.xlsx"
Club_Filtered = ReadAndFilterData(r"Club", [1, 18], Club_path)
Club_LP = CalculateLPAndmLLAcrossFlies(r"Club", Club_Filtered, 250)
Club_LL = GetTrial_Landing_Data(Club_Filtered, "Club", 250)

Iav_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\DataWithNoVideos\Iav-T2-TiTaLP.xlsx"
Iav_Filtered = ReadAndFilterData(r"Iav", [1, 16], Iav_path)
Iav_LP = CalculateLPAndmLLAcrossFlies(r"Iav", Iav_Filtered, 250)
Iav_LL = GetTrial_Landing_Data(Iav_Filtered, "Iav", 250)





ANxGTACR_MAX_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-Max\LO.xlsx"
ANxGTACR_MAX_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-Max\NL.xlsx"
ANxGTACR_MAX_LO, ANxGTACR_MAX_NL = ReadAndFilterOptogeneticData(r"ANxGTACR-NATR-Max", [1, 14], [ANxGTACR_MAX_LO_path, ANxGTACR_MAX_NL_path])
ANxGTACR_MAX_LO_LP = CalculateLPAndmLLAcrossFlies(r"AN-NATR-ON", ANxGTACR_MAX_LO, 250)
ANxGTACR_MAX_LO_LL = GetTrial_Landing_Data(ANxGTACR_MAX_LO, r"AN-NATR-ON", 250)
ANxGTACR_MAX_NL_LP = CalculateLPAndmLLAcrossFlies(r"AN-NATR-OFF", ANxGTACR_MAX_NL, 250)
ANxGTACR_MAX_NL_LL = GetTrial_Landing_Data(ANxGTACR_MAX_NL, r"AN-NATR-OFF", 250)



ANxGTACRNATR_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-NATR-Max\ANxGTACR-NATR-MaxAllLO.xlsx"
ANxGTACRNATR_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-NATR-Max\ANxGTACR-NATR-MaxAllNL.xlsx"
ANxGTACRNATR_LO, ANxGTACRNATR_NL = ReadAndFilterOptogeneticData(r"ANxGTACR-NATR-Max", [1, 14], [ANxGTACRNATR_LO_path, ANxGTACRNATR_NL_path])
ANxGTACRNATR_LO_LP = CalculateLPAndmLLAcrossFlies(r"AN-NATR-ON", ANxGTACRNATR_LO, 250)
ANxGTACRNATR_LO_LL = GetTrial_Landing_Data(ANxGTACRNATR_LO, r"AN-NATR-ON", 250)
ANxGTACRNATR_NL_LP = CalculateLPAndmLLAcrossFlies(r"AN-NATR-OFF", ANxGTACRNATR_NL, 250)
ANxGTACRNATR_NL_LL = GetTrial_Landing_Data(ANxGTACRNATR_NL, r"AN-NATR-OFF", 250)

ANxGTACR4th_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-4th\All_ON.xlsx"
ANxGTACR4th_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-4th\All_OFF.xlsx"
ANxGTACR4th_LO, ANxGTACR4th_NL = ReadAndFilterOptogeneticData(r"ANxGTACR-Inter", [1, 5], [ANxGTACR4th_LO_path, ANxGTACR4th_NL_path])
# print(ANxGTACR4th_LO)
ANxGTACR4th_LO_LP = CalculateLPAndmLLAcrossFlies(r"ON", ANxGTACR4th_LO, 250)
ANxGTACR4th_LO_LL = GetTrial_Landing_Data(ANxGTACR4th_LO, r"ON", 250)
ANxGTACR4th_NL_LP = CalculateLPAndmLLAcrossFlies(r"OFF", ANxGTACR4th_NL, 250)
ANxGTACR4th_NL_LL = GetTrial_Landing_Data(ANxGTACR4th_NL, r"OFF", 250)

EmptyxGTACR_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\GTACRxEmpty-Max\All_ON.xlsx"
EmptyxGTACR_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\GTACRxEmpty-Max\All_OFF.xlsx"
EmptyxGTACR_LO, EmptyxGTACR_NL = ReadAndFilterOptogeneticData(r"EmptyxGTACR-Max", [1, 15], [EmptyxGTACR_LO_path, EmptyxGTACR_NL_path])
EmptyxGTACR_LO_LP = CalculateLPAndmLLAcrossFlies(r"Empty-ON", EmptyxGTACR_LO, 250)
EmptyxGTACR_LO_LL = GetTrial_Landing_Data(EmptyxGTACR_LO, r"Empty-ON", 250)
EmptyxGTACR_NL_LP = CalculateLPAndmLLAcrossFlies(r"Empty-OFF", EmptyxGTACR_NL, 250)
EmptyxGTACR_NL_LL = GetTrial_Landing_Data(EmptyxGTACR_NL, r"Empty-OFF", 250)


EmptyxGTACR_NATR_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\GTACRxEmpty-NATR-Max\ON.xlsx"
EmptyxGTACR_NATR_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\GTACRxEmpty-NATR-Max\OFF.xlsx"
EmptyxGTACR_NATR_LO, EmptyxGTACR_NATR_NL = ReadAndFilterOptogeneticData(r"Empty-NATR-Max", [1, 8], [EmptyxGTACR_NATR_LO_path, EmptyxGTACR_NATR_NL_path])
EmptyxGTACR_NATR_LO_LP = CalculateLPAndmLLAcrossFlies(r"Empty-NATR-ON", EmptyxGTACR_NATR_LO, 250)
EmptyxGTACR_NATR_LO_LL = GetTrial_Landing_Data(EmptyxGTACR_NATR_LO, r"Empty-NATR-ON", 250)
EmptyxGTACR_NATR_NL_LP = CalculateLPAndmLLAcrossFlies(r"Empty-NATR-OFF", EmptyxGTACR_NATR_NL, 250)
EmptyxGTACR_NATR_NL_LL = GetTrial_Landing_Data(EmptyxGTACR_NATR_NL, r"Empty-NATR-OFF", 250)


CSS048xGTACR_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\CSS048xGTACR-Max\ON.xlsx"
CSS048xGTACR_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\CSS048xGTACR-Max\OFF.xlsx"
CSS048xGTACR_LO, CSS048xGTACR_NL = ReadAndFilterOptogeneticData(r"CSS048-GTACR-Max", [1, 22], [CSS048xGTACR_LO_path, CSS048xGTACR_NL_path])
CSS048xGTACR_LO_LP = CalculateLPAndmLLAcrossFlies(r"CSS048-GTACR-ON", CSS048xGTACR_LO, 250)
CSS048xGTACR_LO_LL = GetTrial_Landing_Data(CSS048xGTACR_LO, r"CSS048-GTACR-ON", 250)
CSS048xGTACR_NL_LP = CalculateLPAndmLLAcrossFlies(r"CSS048-GTACR-OFF", CSS048xGTACR_NL, 250)
CSS048xGTACR_NL_LL = GetTrial_Landing_Data(CSS048xGTACR_NL, r"CSS048-GTACR-OFF", 250)


L006xL011_mid_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-3mW\ON.xlsx"
L006xL011_mid_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-3mW\OFF.xlsx"
L006xL011_mid_LO, L006xL011_mid_NL = ReadAndFilterOptogeneticData(r"Tarsal-Br-3mW", [1, 8], [L006xL011_mid_LO_path, L006xL011_mid_NL_path])
L006xL011_mid_LO_LP = CalculateLPAndmLLAcrossFlies(r"Tarsal-Br-3mW-ON", L006xL011_mid_LO, 250)
L006xL011_mid_LO_LL = GetTrial_Landing_Data(L006xL011_mid_LO, r"Tarsal-Br-3mW-ON", 250)
L006xL011_mid_NL_LP = CalculateLPAndmLLAcrossFlies(r"Tarsal-Br-3mW-OFF", L006xL011_mid_NL, 250)
L006xL011_mid_NL_LL = GetTrial_Landing_Data(L006xL011_mid_NL, r"Tarsal-Br-3mW-OFF", 250)


L006xL011_max_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-Max\ON.xlsx"
L006xL011_max_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-Max\OFF.xlsx"
L006xL011_max_LO, L006xL011_max_NL = ReadAndFilterOptogeneticData(r"LexA-Br", [1, 15], [L006xL011_max_LO_path, L006xL011_max_NL_path])
L006xL011_max_LO_LP = CalculateLPAndmLLAcrossFlies(r"LexA-Br-ON", L006xL011_max_LO, 250)
L006xL011_max_LO_LL = GetTrial_Landing_Data(L006xL011_max_LO, r"LexA-Br-ON", 250)
L006xL011_max_NL_LP = CalculateLPAndmLLAcrossFlies(r"LexA-Br-OFF", L006xL011_max_NL, 250)
L006xL011_max_NL_LL = GetTrial_Landing_Data(L006xL011_max_NL, r"LexA-Br-OFF", 250)


L006xL011_max_NATR_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-NATR-Max\ON.xlsx"
L006xL011_max_NATR_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\L006xL011-NATR-Max\OFF.xlsx"
L006xL011_max_NATR_LO, L006xL011_max_NATR_NL = ReadAndFilterOptogeneticData(r"LexA-Br-NATR", [1, 5], [L006xL011_max_NATR_LO_path, L006xL011_max_NATR_NL_path])
L006xL011_max_NATR_LO_LP = CalculateLPAndmLLAcrossFlies(r"LexA-Br-NATR-ON", L006xL011_max_NATR_LO, 250)
L006xL011_max_NATR_LO_LL = GetTrial_Landing_Data(L006xL011_max_NATR_LO, r"LexA-Br-NATR-ON", 250)
L006xL011_max_NATR_NL_LP = CalculateLPAndmLLAcrossFlies(r"LexA-Br-NATR-OFF", L006xL011_max_NATR_NL, 250)
L006xL011_max_NATR_NL_LL = GetTrial_Landing_Data(L006xL011_max_NATR_NL, r"LexA-Br-NATR-OFF", 250)


GTACRx49541_max_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\GTACRx49541-Max\ON.xlsx"
GTACRx49541_max_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\GTACRx49541-Max\OFF.xlsx"
GTACRx49541_max_LO, GTACRx49541_max_NL = ReadAndFilterOptogeneticData(r"GTACRx49541-Max", [1, 13], [GTACRx49541_max_LO_path, GTACRx49541_max_NL_path])
GTACRx49541_max_LO_LP = CalculateLPAndmLLAcrossFlies(r"GTACRx49541-ON", GTACRx49541_max_LO, 250)
GTACRx49541_max_LO_LL = GetTrial_Landing_Data(GTACRx49541_max_LO, r"GTACRx49541-ON", 250)
GTACRx49541_max_NL_LP = CalculateLPAndmLLAcrossFlies(r"GTACRx49541-OFF", GTACRx49541_max_NL, 250)
GTACRx49541_max_NL_LL = GetTrial_Landing_Data(GTACRx49541_max_NL, r"GTACRx49541-OFF", 250)


WTMax_LO_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\WT-Green-Max\WT-Green-Max_ON.xlsx"
WTMax_NL_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\WT-Green-Max\WT-Green-Max_OFF.xlsx"
WTMax_LO, WTMax_NL = ReadAndFilterOptogeneticData(r"WT-Green-Max", [1, 9], [WTMax_LO_path, WTMax_NL_path])
WTMax_LO_LP = CalculateLPAndmLLAcrossFlies(r"WT-ON", WTMax_LO, 250)
WTMax_LO_LL = GetTrial_Landing_Data(WTMax_LO, r"WT-ON", 250)
WTMax_NL_LP = CalculateLPAndmLLAcrossFlies(r"WT-OFF", WTMax_NL, 250)
WTMax_NL_LL = GetTrial_Landing_Data(WTMax_NL, r"WT-OFF", 250)

lines = ["solid", "solid", "dashed", "solid", "solid", "solid", "solid", "solid", "solid", "solid", "solid", "solid"]

import matplotlib.cm as cm
# Choose a colormap (e.g., viridis, plasma, coolwarm, etc.)
cmap = cm.get_cmap('viridis', 10)

# Generate list of colors
colors = [cmap(i) for i in range(10)]
# Color_blind_palette = colors[:5]
# LPAcrossFlies([T2TTa_LP, HP1_LP, HP2_LP, HP3_LP, ClFl_LP, ClEx_LP, HkFl_LP, HkEx_LP, Club_LP, Iav_LP], "KirExperiment")
# ecdfPlot([T2TTa_LL, HP1_LL, HP2_LL, HP3_LL, ClFl_LL], "KirExperimentLL1")


Color_blind_palette =  ["red", "blue", "blue", "green", "orange", "blue", "orange"]

WTnecessity = True
WTInterleg = False
LP_data_type = "LandingProb"
LL_data_type = "TrialLandingLatency"


# LPAcrossLight([GTACRx49541_max_LO_LP, GTACRx49541_max_NL_LP], "ChrimsonExpANLP", "green")
# LPAcrossLight([GTACRx49541_max_LO_LP, L006xL011_max_LO_LP], "ChrimsonExpANLP", "green")
# ecdfPlot([GTACRx49541_max_LO_LL, L006xL011_max_LO_LL], "ChrimsonExpANLP")
Bootstrapping_test(GTACRx49541_max_LO_LP["LandingProb"], GTACRx49541_max_NL_LP["LandingProb"])


import scipy.stats as stats
# t, p = stats.ttest_rel(CSS048xGTACR_LO_LP["LandingProb"], CSS048xGTACR_NL_LP["LandingProb"])
t, p = stats.ttest_rel(GTACRx49541_max_LO_LP["LandingProb"], GTACRx49541_max_NL_LP["LandingProb"])

print(t, p)




