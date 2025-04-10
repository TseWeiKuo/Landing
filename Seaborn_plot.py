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
    fig = plt.figure(1, figsize=(len(Original_Data) * 4, 10))
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

    # Visualize the bootstrap t-statistic distribution
    # plt.figure(1)
    # plt.figure(figsize=(8, 6))
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
    k = 0
    for m in bootstrap_mean_diffs:
        # print(m)
        if abs(m) > abs(original_mean_diff):
            k += 1
    Mean_diff_p_value = (np.sum(np.abs(bootstrap_mean_diffs) >= np.abs(original_mean_diff))) / (num_bootstrap_samples)
    Median_diff_p_value = (np.sum(np.abs(bootstrap_median_diffs) >= np.abs(original_median_diff))) / (num_bootstrap_samples)

    print(f"Difference in mean's P-value = {Mean_diff_p_value}")
    print(f"Original mean diff = {original_mean_diff}")
    print(f"Difference in median's P value = {Median_diff_p_value}")
    print(f"Original median diff = {original_median_diff}")
    print("*" * 20)
    print("")
    print("")
    # plt.title('Bootstrap mean and median difference Distribution', y=1)
    plt.ylabel('Count')
    plt.legend()
    # plt.savefig("Bootstrapping mean diff")

    # plt.show()
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
    g.set_ylim(-0.3, 1.5)

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
    plt.xlim(-1, len(Data_to_plot))
    sns.despine(trim=True)
    plt.tight_layout()
    plt.savefig(f"{file_name}.pdf", format='pdf', dpi=300, bbox_inches='tight')
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
        LP_mLL_Data["Fly#"].append(index + 1)
        LP_mLL_Data["LandingProb"].append(len(Landing_latency) / (len(Flying) + len(Landing_latency)))
        LP_mLL_Data["MLandingLatency"].append(np.mean(Landing_latency))
    LP_mLL_Data["Group_Name"] = [GroupName] * Landing_Data.shape[0]
    LP_mLL_Data = pd.DataFrame(LP_mLL_Data)
    return LP_mLL_Data
def CessationAcrossFlies(GroupName, Flies_to_pick, Cessation_Data_path):
    global Trial_num
    global colors
    Cessation_Data = pd.read_excel(Cessation_Data_path)
    Cessation_Data = Cessation_Data.iloc[Flies_to_pick[0] - 1:Flies_to_pick[1]]
    Valid_data_index = []
    for index, row in Cessation_Data.iterrows():
        str_nan_count = 0
        for data in row.values:
            if isinstance(data, str) or pd.isna(data):
                str_nan_count += 1
        if str_nan_count < (len(row.values) / 2):
            Valid_data_index.append(index)

    Cessation_Data = Cessation_Data[Cessation_Data.index.isin(Valid_data_index)]
    GroupNameCol = [GroupName] * len(Valid_data_index)
    Cessation_Data["Group_Name"] = GroupNameCol
    CollectedData = dict()
    CollectedData["Fly Num"] = []
    CollectedData["Cessation latency (s)"] = []


    for idx, fly in Cessation_Data.iterrows():
        for cessation_l_val in fly[Trial]:
            if not (isinstance(cessation_l_val, str) or pd.isna(cessation_l_val) or cessation_l_val < 0):
                if cessation_l_val < 500:

                    CollectedData["Fly Num"].append(fly["Fly#"])
                    # print(cessation_l_val)
                    CollectedData["Cessation latency (s)"].append(cessation_l_val/FPS)
    CollectedData = pd.DataFrame(CollectedData)
    # sns.violinplot(x="Fly_Num", y="Values", data=CollectedData, hue="Fly_Num")
    # plt.show()
    # plt.close()
    dark_palette = sns.dark_palette("blue", reverse=False, n_colors=15)
    g = sns.stripplot(x="Fly Num", y="Cessation latency (s)", data=CollectedData, hue="Fly Num", size=12, alpha=0.5, palette=dark_palette)
    if g.legend():
        g.legend_.remove()
    plt.savefig("Cessation latency across flies")
    plt.show()
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
def ecdfPlot(Original_Data):
    from matplotlib.lines import Line2D
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
    legend_handles = []  # List to store legend handles
    legend_labels = ["G106 manual", "G106 predicted", "G108", "G107", "G106", "CSS0048", "CSS0039"]  #
    # combined_df = pd.concat(Original_Data)
    for i, d in enumerate(Original_Data):
        sns.ecdfplot(d["TrialLandingLatency"], alpha=0.8, color=Color_blind_palette[i], legend=True, linewidth=3)
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
    ax.set_xlabel("Landing latency (s)", fontsize=25)
    ax.set_ylabel("Percentage (%)", fontsize=25)

    ax.legend(legend_handles, legend_labels, fontsize=20, loc="lower right", frameon=True)
    plt.tight_layout()
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
group_name = ["WT-CTF",
              "Kir Control CTF",
              "Fe-Gal4 CTF",
              "HP-Gal4 CTF"]
#group_name = group_name[2:]
Trial_num = 20
trial = [str(t+1) for t in range(Trial_num)]
Trial = [f"Trial_{t + 1}" for t in range(Trial_num)]
Fly_to_pick = [1, 30]
Fly_Num = 34
# '#1f77b4',
Color_blind_palette = sns.color_palette("Set2", n_colors=15)
# Color_blind_palette = [Color_blind_palette[0], Color_blind_palette[1], Color_blind_palette[2], Color_blind_palette[5], Color_blind_palette[6], Color_blind_palette[3], Color_blind_palette[4]]
lightened_palette = [brighten_color(color, 0) for color in Color_blind_palette]
# Color_blind_palette = [Color_blind_palette[5], Color_blind_palette[8], Color_blind_palette[7], Color_blind_palette[3], Color_blind_palette[4]]
# Color_blind_palette = Color_blind_palette[1:]
# Color_blind_palette = Color_blind_palette[2:]
markers = ['o', 'o', 'o', 'o', 'o','o', 'o', 'o', 'o', 'o', 'X']
# markers = [">", ">", ">", ">", ">", ">", ">", ">", ">", ">", ">"]
FilterHighLatency = True
samejoint = False
vio = False
ReadData = True
trial_offset = 3
r"""T1TTa_path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\LPAcrossLegsJoints\T1-TiTa\T1-TiTaLP.xlsx"
T1TTa_200FPS = ReadAndFilterData(r"T1-TiTa", [1, 12], T1TTa_path)
T1TTa_250FPS = ReadAndFilterData(r"T1-TiTa", [13, 15], T1TTa_path)
T1TTa_LP_200FPS = CalculateLPAndmLLAcrossFlies(r"T1-TiTa", T1TTa_200FPS, 200)
T1TTa_LL_200FPS = GetTrial_Landing_Data(T1TTa_200FPS, "T1-TiTa", 200)
T1TTa_LP_250FPS = CalculateLPAndmLLAcrossFlies(r"T1-TiTa", T1TTa_250FPS, 250)
T1TTa_LL_250FPS = GetTrial_Landing_Data(T1TTa_250FPS, "T1-TiTa", 250)
T1TTa_LP = pd.concat([T1TTa_LP_200FPS, T1TTa_LP_250FPS])
T1TTa_LL = pd.concat([T1TTa_LL_200FPS, T1TTa_LL_250FPS])"""

T2TTa_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T2-TiTa\T2-TiTaLP.xlsx"
T2TTa_Filtered = ReadAndFilterData(r"T2-TiTa WT", [1, 15], T2TTa_path)
T2TTa_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa WT", T2TTa_Filtered, 200)
T2TTa_LL = GetTrial_Landing_Data(T2TTa_Filtered, "T2-TiTa WT", 200)

T2TTa_path_prediction = r"C:\Users\agrawal-admin\Desktop\Landing\LLPrediction_WT.xlsx"
T2TTa_Filtered_prediction = ReadAndFilterData(r"T2-TiTa predicted", [1, 15], T2TTa_path_prediction)
T2TTa_LP_prediction = CalculateLPAndmLLAcrossFlies(r"T2-TiTa predicted", T2TTa_Filtered_prediction, 200)
T2TTa_LL_prediction = GetTrial_Landing_Data(T2TTa_Filtered_prediction, "T2-TiTa predicted", 200)

T2CTF_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\LPAcrossLegsJoints\T2-CxTr\T2-CxTrLP.xlsx"
T2CTF_Filtered = ReadAndFilterData(r"T2-CxTr", [1, 18], T2CTF_path)
T2CTF_LP = CalculateLPAndmLLAcrossFlies(r"T2-CxTr", T2CTF_Filtered, 250)
T2CTF_LL = GetTrial_Landing_Data(T2CTF_Filtered, r"T2-CxTr", 250)

r"""T3TTa_path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\LPAcrossLegsJoints\T3-TiTa\T3-TiTaLP.xlsx"
T3TTa_200FPS = ReadAndFilterData(r"T3-TiTa", [1, 15], T3TTa_path)
T3TTa_250FPS = ReadAndFilterData(r"T3-TiTa", [16, 20], T3TTa_path)
T3TTa_LP_200FPS = CalculateLPAndmLLAcrossFlies(r"T3-TiTa", T3TTa_200FPS, 200)
T3TTa_LL_200FPS = GetTrial_Landing_Data(T3TTa_200FPS, "T3-TiTa", 200)
T3TTa_LP_250FPS = CalculateLPAndmLLAcrossFlies(r"T3-TiTa", T3TTa_250FPS, 250)
T3TTa_LL_250FPS = GetTrial_Landing_Data(T3TTa_250FPS, "T3-TiTa", 250)
T3TTa_LP = pd.concat([T3TTa_LP_200FPS, T3TTa_LP_250FPS])
T3TTa_LL = pd.concat([T3TTa_LL_200FPS, T3TTa_LL_250FPS])

T1CTF_Tarsus_path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\LPAcrossLegsJoints\T1-CxTr\T1-TiTa-Data_TarsusContact.xlsx"
T1CTF_Tarsus = ReadAndFilterData(r"T1-CxTr-TarsusContact", [1, 15], T1CTF_Tarsus_path)
T1CTF_Tarsus_LP = CalculateLPAndmLLAcrossFlies(r"T1-CxTr-TarsusContact", T1CTF_Tarsus, 250)
T1CTF_Tarsus_LL = GetTrial_Landing_Data(T1CTF_Tarsus, r"T1-CxTr-TarsusContact", 250)

T1CTF_CxTr_path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\LPAcrossLegsJoints\T1-CxTr\T1-TiTa-Data_CoxaContact.xlsx"
T1CTF_CxTr = ReadAndFilterData(r"T1-CxTr-CoxaContact", [1, 15], T1CTF_CxTr_path)
T1CTF_CxTr_LP = CalculateLPAndmLLAcrossFlies(r"T1-CxTr-CoxaContact", T1CTF_CxTr, 250)
T1CTF_CxTr_LL = GetTrial_Landing_Data(T1CTF_CxTr, r"T1-CxTr-CoxaContact", 250)

T3CTF_path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\LPAcrossLegsJoints\T3-CxTr\T3-CxTrLP.xlsx"
T3CTF_Filtered = ReadAndFilterData(r"T3-CxTr", [1, 17], T3CTF_path)
T3CTF_LP = CalculateLPAndmLLAcrossFlies(r"T3-CxTr", T3CTF_Filtered, 250)
T3CTF_LL = GetTrial_Landing_Data(T3CTF_Filtered, r"T3-CxTr", 250)"""


T2_TTa_G106_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\G106-HP1_T2-TiTa\LandingData.xlsx"
T2_TTa_G106 = ReadAndFilterData(r"T2-TiTa G106", [2, 9], T2_TTa_G106_path)
T2_TTa_G106_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa G106", T2_TTa_G106, 250)
T2_TTa_G106_LL = GetTrial_Landing_Data(T2_TTa_G106, r"T2-TiTa G106", 250)

T2_TTa_G106_predicted_path = r"C:\Users\agrawal-admin\Desktop\Landing\LLPrediction_G106.xlsx"
T2_TTa_G106_predicted = ReadAndFilterData(r"Predicted G106", [1, 16], T2_TTa_G106_predicted_path)
T2_TTa_G106_predicted_LP = CalculateLPAndmLLAcrossFlies(r"Predicted G106", T2_TTa_G106_predicted, 250)
T2_TTa_G106_predicted_LL = GetTrial_Landing_Data(T2_TTa_G106_predicted, r"T2-TiTa G106", 250)

T2_CTF_G106_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\G106-HP1_T2-CxTr\2025-03-24\G106_CxTr.xlsx"
T2_CTF_G106 = ReadAndFilterData(r"T2-CxTr G106", [1, 15], T2_CTF_G106_path)
T2_CTF_G106_LP = CalculateLPAndmLLAcrossFlies(r"T2-CxTr G106", T2_CTF_G106, 250)
T2_CTF_G106_LL = GetTrial_Landing_Data(T2_CTF_G106, r"T2-CxTr G106", 250)

T2_TTa_G107_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\G107-HP2_T2-TiTa\LandingData_G107.xlsx"
T2_TTa_G107 = ReadAndFilterData(r"T2-TiTa G107", [1, 14], T2_TTa_G107_path)
T2_TTa_G107_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa G107", T2_TTa_G107, 250)
T2_TTa_G107_LL = GetTrial_Landing_Data(T2_TTa_G107, r"T2-TiTa G107", 250)

T2_TTa_G107_Prediction_path = r"C:\Users\agrawal-admin\Desktop\Landing\LLPrediction_G107.xlsx"
T2_TTa_G107_Prediction = ReadAndFilterData(r"T2-TiTa G107", [1, 14], T2_TTa_G107_Prediction_path)
T2_TTa_G107_Prediction_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa G107", T2_TTa_G107_Prediction, 250)
T2_TTa_G107_Prediction_LL = GetTrial_Landing_Data(T2_TTa_G107_Prediction, r"T2-TiTa G107", 250)

T2_CTF_G107_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\G107-HP2_T2-CxTr\LandingData_G107CxTr.xlsx"
T2_CTF_G107 = ReadAndFilterData(r"T2-CxTr G107", [1, 14], T2_CTF_G107_path)
T2_CTF_G107_LP = CalculateLPAndmLLAcrossFlies(r"T2-CxTr G107", T2_CTF_G107, 250)
T2_CTF_G107_LL = GetTrial_Landing_Data(T2_CTF_G107, r"T2-CxTr G107", 250)

T2_TTa_G115_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\G115-Iav_T2-TiTa\LandingData_G115.xlsx"
T2_TTa_G115 = ReadAndFilterData(r"T2-TiTa G115", [1, 16], T2_TTa_G115_path)
T2_TTa_G115_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa G115", T2_TTa_G115, 250)
T2_TTa_G115_LL = GetTrial_Landing_Data(T2_TTa_G115, "T2-TiTa G115", 250)

T2_TTa_G115_predicted_path = r"C:\Users\agrawal-admin\Desktop\Landing\LLPrediction_G115.xlsx"
T2_TTa_G115_predicted = ReadAndFilterData(r"T2-TiTa G115", [1, 16], T2_TTa_G115_predicted_path)
T2_TTa_G115_predicted_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa G115", T2_TTa_G115_predicted, 250)
T2_TTa_G115_predicted_LL = GetTrial_Landing_Data(T2_TTa_G115_predicted, "T2-TiTa G115", 250)

T2_TTa_CSS0039_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\CSS-0039_T2-TiTa\LandingData_All.xlsx"
T2_TTa_CSS0039 = ReadAndFilterData(r"T2-TiTa CSS-0039", [1, 15], T2_TTa_CSS0039_path)
T2_TTa_CSS0039_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa CSS-0039", T2_TTa_CSS0039, 250)
T2_TTa_CSS0039_LL = GetTrial_Landing_Data(T2_TTa_CSS0039, "T2-TiTa CSS-0039", 250)

T2_TTa_CSS0048_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\CSS-0048_T2-TiTa\LandingData_all.xlsx"
T2_TTa_CSS0048 = ReadAndFilterData(r"T2-TiTa CSS-0048", [1, 9], T2_TTa_CSS0048_path)
T2_TTa_CSS0048_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa CSS-0048", T2_TTa_CSS0048, 250)
T2_TTa_CSS0048_LL = GetTrial_Landing_Data(T2_TTa_CSS0048, "T2-TiTa CSS-0048", 250)

T2_TTa_G108_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\G108-HP3_T2-TiTa\LandingData_All.xlsx"
T2_TTa_G108 = ReadAndFilterData(r"T2-TiTa G108", [1, 7], T2_TTa_G108_path)
T2_TTa_G108_LP = CalculateLPAndmLLAcrossFlies(r"T2-TiTa G108", T2_TTa_G108, 250)
T2_TTa_G108_LL = GetTrial_Landing_Data(T2_TTa_G108, "T2-TiTa G108", 250)




LPAcrossFlies([T2_TTa_G106_LP, T2_TTa_G106_predicted_LP], "PredvsManual G106")
ecdfPlot([T2_TTa_G106_LL, T2_TTa_G106_predicted_LL])

# LPAcrossFlies([T2TTa_LP, T2_TTa_G115_LP, T2_TTa_G108_LP, T2_TTa_G107_LP, T2_TTa_G106_LP, T2_TTa_CSS0048_LP, T2_TTa_CSS0039_LP], "Mutant Fly TTa LP")
# TLLCluster([T2CTF_LL, T2_CTF_G106_LL, T2_CTF_G107_LL], "Mutant Fly CTF LL")


# Cumulative_Histplot_LL([T2TTa_LL, T2TTa_LL_prediction])
# ecdfPlot([T2TTa_LL, T2_TTa_G115_LL, T2_TTa_G108_LL, T2_TTa_G107_LL, T2_TTa_G106_LL, T2_TTa_CSS0048_LL, T2_TTa_CSS0039_LL])
# ecdfPlotLP([T2_TTa_G106_LP, T2_TTa_G106_predicted_LP])
# ecdfPlot([T2TTa_LP, T2_TTa_G106_LP, T2_TTa_G107_LP, T2_TTa_G115_LP])

