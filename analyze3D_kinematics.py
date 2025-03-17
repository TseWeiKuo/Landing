import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import h5py
from sklearn.tree import DecisionTreeClassifier
from dateutil.parser import parse
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from datetime import datetime
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statistics import median
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks, peak_widths
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter1d
import warnings
import re
warnings.filterwarnings(action="ignore", category=RuntimeWarning)

"""
These functions are responsible for preprocessing of angle data and 3D pose data
"""
def exponential_moving_average(data, alpha):
    if isinstance(data, pd.Series):
        data = data.tolist()
    ema = [data[0]]
    for i in range(1, len(data)):
        ema.append(alpha * data[i] + (1 - alpha) * ema[-1])
    return ema
def find_derivative(y):
    return np.gradient(y, 1)
def two_phase_decay_func(x, a1, b1, a2, b2, c):
    return a1 * np.exp(-b1 * x) + a2 * np.exp(-b2 * x) + c
def Find_best_fit_platform(x_data, y_data):
    x_data = np.asarray(x_data)
    y_data = np.asarray(y_data)
    valid_indices = ~np.isnan(y_data)
    x_valid = x_data[valid_indices]
    y_valid = y_data[valid_indices]
    if len(y_valid) != 0:
        params, covariance = curve_fit(two_phase_decay_func, x_data, y_valid, maxfev=10000)
        a1, b1, a2, b2, c = params
        y_pred = two_phase_decay_func(x_valid, a1, b1, a2, b2, c)
        return x_valid, y_pred
    else:
        return [], []
def determine_smooth_amplify_curve(data, sig, amp):
    if amp:
        data = np.asarray(data)
        data = gaussian_filter1d(data, sigma=sig)
        return np.asarray(data)
    else:
        return np.asarray(data)
def TraceData_Preprocessing(angle_data, kinematic_data, start, end):
    DataToBeShown = dict()
    trial_angle_data = angle_data[start:end]
    trial_kinematic_data = kinematic_data[start:end]

    distance_pltf_RmCT = CalculateDistance_Platform_RmCT(trial_kinematic_data, "platform", "R-mCT")
    Platform_error = trial_kinematic_data["platform_error"]
    Platform_x = trial_kinematic_data["platform_x"]
    Platform_y = trial_kinematic_data["platform_y"]
    Platform_z = trial_kinematic_data["platform_z"]
    RightWing = trial_angle_data["RightWingAngle"]
    LeftWing = trial_angle_data["LeftWingAngle"]
    # CTAngle = trial_angle_data["CTAngle"]
    # CT_axis = trial_angle_data["CTAngle_axis"]
    # CT_cross = trial_angle_data["CTAngle_cross"]
    # FTAngle = trial_angle_data["FTAngle"]

    distance_pltf_RmCT = determine_smooth_amplify_curve(distance_pltf_RmCT, 5, True)
    Platform_x = determine_smooth_amplify_curve(Platform_x, 10, True)
    Platform_y = determine_smooth_amplify_curve(Platform_y, 10, True)
    Platform_z = determine_smooth_amplify_curve(Platform_z, 10, True)
    # CTAngle = determine_smooth_amplify_curve(CTAngle, True)
    # CT_axis = determine_smooth_amplify_curve(CT_axis, True)
    # CT_cross = determine_smooth_amplify_curve(CT_cross, True)
    # FTAngle = determine_smooth_amplify_curve(FTAngle, True)
    RightWing = determine_smooth_amplify_curve(RightWing, 10, True)
    LeftWing = determine_smooth_amplify_curve(LeftWing, 10, True)

    # platform_distance = determine_smooth_amplify_curve(trial_kinematic_data["platform_x"], True)
    DataToBeShown["platform"] = pd.Series(distance_pltf_RmCT)
    DataToBeShown["RightWingAngle"] = pd.Series(RightWing)
    DataToBeShown["LeftWingAngle"] = pd.Series(LeftWing)
    # DataToBeShown["CTAngle"] = pd.Series(CTAngle)
    # DataToBeShown["CT_axis"] = pd.Series(CT_axis)
    # DataToBeShown["CT_cross"] = pd.Series(CT_cross)
    # DataToBeShown["FTAngle"] = pd.Series(FTAngle)
    DataToBeShown["Platform_error"] = pd.Series(Platform_error)
    DataToBeShown["Platform_x"] = pd.Series(Platform_x)
    DataToBeShown["Platform_y"] = pd.Series(Platform_y)
    DataToBeShown["Platform_z"] = pd.Series(Platform_z)

    return DataToBeShown
def CalculateDistance_Platform_RmCT(threeD_data, keypoint1, keypoint2):
    platform_coxa_distance = []
    """

    for p_x, p_y, p_z, C_x, C_y, C_z in zip(threeD_data[f"{keypoint1}_x"], threeD_data[f"{keypoint1}_y"],
                                            threeD_data[f"{keypoint1}_z"], threeD_data[f"{keypoint2}_x"],
                                            threeD_data[f"{keypoint2}_y"], threeD_data[f"{keypoint2}_z"]):
        platform_coxa_distance.append(np.sqrt((p_x - C_x) ** 2 + (p_y - C_y) ** 2 + (p_z - C_z) ** 2))
    # sns.lineplot(x=range(len(threeD_data)), y=platform_coxa_distance)
    return platform_coxa_distance
    """
    C_x = np.average(threeD_data[f"{keypoint2}_x"][:100])
    C_y = np.average(threeD_data[f"{keypoint2}_y"][:100])
    C_z = np.average(threeD_data[f"{keypoint2}_z"][:100])
    for p_x, p_y, p_z in zip(threeD_data[f"{keypoint1}_x"], threeD_data[f"{keypoint1}_y"],
                                            threeD_data[f"{keypoint1}_z"]):
        platform_coxa_distance.append(np.sqrt((p_x - C_x) ** 2 + (p_y - C_y) ** 2 + (p_z - C_z) ** 2))
    # sns.lineplot(x=range(len(threeD_data)), y=platform_coxa_distance)
    return platform_coxa_distance
def normalize_list(data, method="min-max"):
    if method == "min-max":
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            raise ValueError("Cannot perform Min-Max normalization when all values are the same.")
        return [(x - min_val) / (max_val - min_val) for x in data]

"""
These functions are responsible for detecting various characteristic of the angle and 3D data
"""
def detect_brief_landing(angle_data, bl_range, wing_ang_fold_th, wing_ang_drop_percent, window_size, st_base_th, consecutive_fold_th):

    # Calculate the start and end baseline of wing angle
    start_baseline = np.mean(angle_data[:bl_range])
    end_baseline = np.mean(angle_data[-bl_range:])

    chunk_size = 10
    consecutive_chunk = 0

    if start_baseline > st_base_th:

        for i in range(0, len(angle_data), window_size):
            curr_v = np.mean(angle_data[i:i + window_size])
            if curr_v / start_baseline < (1 - wing_ang_drop_percent) and curr_v < wing_ang_fold_th:
                consecutive_chunk += 1
            else:
                consecutive_chunk = 0
            if consecutive_chunk >= consecutive_fold_th:
                stop_idx = i - (consecutive_fold_th - 1) * window_size
                return True, stop_idx
    return False, 0
def detect_significant_drop(angle_data, bl_range, wing_ang_fold_th, wing_ang_drop_percent, window_size):
    start_baseline = np.mean(angle_data[:bl_range])
    end_baseline = np.mean(angle_data[-bl_range:])
    repeat = 0
    cons_th = 4
    if (1 - (end_baseline / start_baseline)) > 0.05:
        # print(start_baseline)
        for i in range(0, len(angle_data), window_size):
            current_chunk_v = np.mean(angle_data[i:i + window_size])
            if (abs(current_chunk_v - start_baseline) / (start_baseline - end_baseline) > wing_ang_drop_percent) and current_chunk_v < wing_ang_fold_th:
                # return i

                repeat += 1
            else:
                repeat = 0
            if repeat >= cons_th:
                return i - ((cons_th - 1) * window_size)


    return 0
def detect_Not_Flying(angle_data, bl_range, wing_ang_fold_th, wing_ang_drop_percent, window_size, baseline_diff_percent):
    start_base_line = np.mean(angle_data[:bl_range])
    end_base_line = np.mean(angle_data[-bl_range:])
    # print(start_base_line, end_base_line)
    if ((start_base_line - end_base_line) / start_base_line) < baseline_diff_percent and start_base_line < wing_ang_fold_th:
        return True
    else:
        stop_idx = detect_significant_drop(angle_data, bl_range, wing_ang_fold_th, wing_ang_drop_percent, window_size)
        # print(stop_idx)
        if stop_idx < int(0.1 * len(angle_data)) and stop_idx != 0:
            return True
        else:
            return False
def detect_moment_of_landing(trace_data, wing_distance_threshold, wind_size, duration_threshold):
    wing_fold_duration = 0
    cons_th = 4
    if np.average(trace_data[:100]) < 2:
        return 0
    for i in range(0, len(trace_data), wind_size):
        if np.average(trace_data[i:i+wind_size]) < wing_distance_threshold:
            wing_fold_duration += 1
        else:
            wing_fold_duration = 0
        if wing_fold_duration > duration_threshold:
            return i - ((cons_th - 1) * wind_size)
    return 0
def detectFlying(angle_data, bl_range, wing_ang_fold_th, window_size):
    chunk_size = 20
    start_base_line = np.mean(angle_data[:bl_range])
    end_base_line = np.mean(angle_data[-bl_range:])
    if start_base_line > wing_ang_fold_th and end_base_line > wing_ang_fold_th:
        for i in range(0, len(angle_data), window_size):
            current_v = np.mean(angle_data[i:i + window_size])
            if current_v < wing_ang_fold_th:
                return False
    return True
def detect_moment_of_contact(threeD_data):
    for index, f in threeD_data.iterrows():
        TT_joint = [f["R-mTT_x"], f["R-mTT_y"], f["R-mTT_z"]]
        LT_joint = [f["R-mLT_x"], f["R-mLT_y"], f["R-mLT_z"]]
        Center = [f["platform-tip_x"], f["platform-tip_y"], f["platform-tip_z"]]
        Left = [f["L-platform-tip_x"], f["L-platform-tip_y"], f["L-platform-tip_z"]]
        Right = [f["R-platform-tip_x"], f["R-platform-tip_y"], f["R-platform-tip_z"]]
        if check_leg_platform_intersection(TT_joint, LT_joint, Center, Left, Right):
            return index
    return 0
def WingAngle_DetermineLanding(wing_data, platform_data, fly, trial):
    global Customized_wing_threshold
    global Customized_Flying_threshold
    global Customized_notFly_threshold
    chunk_size = 4
    chunk_num = 0

    nan_count = wing_data.isna().sum()
    percentage_nan = (nan_count / len(wing_data)) * 100
    moment_of_contact = 0
    stop_dropping = 0
    # Determine validity of the data
    print(f"Fly: {fly}---Trial{trial}")
    if percentage_nan > 50:
        # print(np.nan)
        return np.nan, 0
    else:
        stop_dropping = detect_significant_drop(wing_data, 50, 105, 0.3, 15)
        moment_of_contact = detect_moment_of_contact(platform_data, "Threshold", 0, 4, 0, 0)
        if detect_Not_Flying(wing_data, 50, 105, 0.3, 10, 0.15):

            # print(2, 0)
            return 2, 0
        else:
            if stop_dropping > 50:
                latency = stop_dropping - moment_of_contact
                print(f"Stop dropping: {stop_dropping}")
                print(f"MOC: {moment_of_contact}")
                if latency > 0:
                    if latency > 450:
                        return 0, 0
                    else:
                        return 1, latency
                else:
                    return 2, 0
            else:
                if detectFlying(wing_data, 50, 100, 5):
                    # print(0, 0)
                    return 0, 0
                else:
                    landing, latency = detect_brief_landing(wing_data, 50, 150, 0.25, 10, 105, 5)
                    # print(landing, latency)
                    if landing:
                        return 1, latency - moment_of_contact

    # print("Uncategorized")
    return 0, 0
"""
These functions are responsible for testing and plotting the result from detection functions.
"""

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
    # LP_mLL_Data["Time"] = Landing_Data["Time"].tolist()
    # LP_mLL_Data["Date"] = Landing_Data["Date"].tolist()
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    Landing_Data = Landing_Data[Trials]
    for index, row in Landing_Data.iterrows():
        Nan_data = [n for n in row if pd.isna(n) or isinstance(n, str)]
        Flying = [f for f in row if f == -1]
        Landing_latency = [l / 250 for l in row if not isinstance(l, str) and l > -1]
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
def LLCluster(Original_Data, Filter_Data):
    global FPS
    global markers
    Trials = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    fig = plt.figure(1, figsize=(16, 8))
    sns.axes_style("ticks")
    for i, group_data in enumerate(Original_Data, start=1):
        Landing_latency = []
        n = 0
        print(group_data)
        for index, fly in group_data[Trials].iterrows():
            Landing_latency.extend([l / 250 for l in fly if not isinstance(l, str) and l > -1])

            # sns.stripplot(x=np.full(len(Landing_latency), i + 2), y=Landing_latency, jitter=0.2, marker='o', size=8, alpha=0.4, color=colors[n])
        sns.violinplot(x=np.full(len(Landing_latency), i), y=Landing_latency, color=Color_blind_palette[i - 1],
                       fill=False)

    for i, group_data in enumerate(Filter_Data, start=1):
        # ax = sns.stripplot(x="Group_Name", y="MLandingLatency", data=group_data, jitter=0.2, marker=markers[i - 1], size=20, alpha=0.75, color=Color_blind_palette[i-1])
        ax = sns.violinplot(x="Group_Name", y="MLandingLatency", data=group_data, color=Color_blind_palette[i - 1])
        ax.spines['left'].set_linewidth(3)
        ax.spines['bottom'].set_linewidth(3)
    plt.ylabel("Landing latency (s)", fontsize=25)

    plt.ylim(0, 3.2)
    plt.yticks([0, 1.5, 3])
    plt.xticks(ticks=[0, 1, 2, 3],
               labels=['Trial LL M', 'Trial LL C', 'Mean LL M', 'Mean LL C'])
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=20)
    plt.tick_params(width=3, length=10)
    sns.despine()
    # fig.suptitle("Landing latency (T2-TTa vs T2-CTF)")
    # plt.rcParams["axes.linewidth"] = 2.5
    plt.tight_layout()

    plt.savefig("LLAcrossFlies.pdf", dpi=300, bbox_inches='tight')
    plt.show()
def LPAcrossFlies(Data_to_plot):
    global Color_blind_palette
    global markers

    combined_df = pd.concat(Data_to_plot)
    plt.figure(figsize=(16, 8))

    for i, d in enumerate(Data_to_plot):
        print(i)
        # g = sns.stripplot(x="Group_Name", y="LandingProb", hue="Group_Name", data=d, marker=markers[i], jitter=0.3, alpha=0.75, size=20, palette=[Color_blind_palette[i]])
        g = sns.violinplot(x="Group_Name", y="LandingProb", hue="Group_Name", data=d, palette=[Color_blind_palette[i]])
        g.spines['left'].set_linewidth(3)
        g.spines['bottom'].set_linewidth(3)
        g.set_ylim(-0.1, 1.3)

    group_stat = combined_df.groupby('Group_Name')['LandingProb'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    sns.pointplot(x='Group_Name', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None)
    plt.errorbar(x=group_stat['Group_Name'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=5)

    # plt.legend(handles=legend_elements, loc='upper right', fontsize=20)
    plt.ylabel("Landing Probability", fontsize=25)
    plt.tick_params(axis="y", labelsize=25)
    plt.tick_params(axis="x", labelsize=25)
    plt.tick_params(width=3, length=10)
    plt.yticks([0, 0.5 ,1])

    sns.despine()
    plt.savefig("LPAcrossFliesStarvedExp", dpi=300, bbox_inches='tight')
    plt.show()
def CalculatePlatform_distance_average(collected_data):
    np_matrix = np.array(collected_data)
    transposed_matrix = np_matrix.T
    average_trace = []
    for frame_data in transposed_matrix:
        average_trace.append(np.average(frame_data))
    # average_trace = determine_smooth_amplify_curve(average_trace, 5, True)
    return average_trace
def detectMOC(data, threshold=0.09538):
    wind_size = 5
    baseline = np.average(data[400:])
    for i in range(0, len(data), wind_size):
        if np.average(data[i:i + wind_size]) <= threshold:
            return i
    return 0
def MakePlot(Angle_data, Pose_Data, fly_num, clipstart, clipend, plot_manual):
    global mol_data
    global moc_data
    global p_dist_at_moc
    global p_baseline
    global fit_line_pred_at_moc
    global fit_line_baseline
    global average_baseline
    global average_distance_at_moc
    global moc_error
    global slopes
    global intercepts
    global platform_distance
    i = 0
    j = 0
    t = 0
    fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 16))
    for trial_angle, trial_kinematic in zip(Angle_data, Pose_Data):
        filtered = False
        if i % 5 == 0:
            j += 1
            i = 1
        else:
            i += 1
        # Plot data
        ax2 = axs[i - 1, j - 1].twinx()
        ax2.set_ylim(-2, 10)
        seconds = [f / FPS for f in range(clipend - clipstart)]
        wing_distance = CalculateDistance_Platform_RmCT(trial_kinematic[clipstart:clipend], "L-wing", "R-wing")
        sns.lineplot(x=seconds, y=trial_angle["RightWingAngle"][clipstart:clipend], ax=axs[i - 1, j - 1], color="red")
        sns.lineplot(x=seconds, y=trial_angle["LeftWingAngle"][clipstart:clipend], ax=axs[i - 1, j - 1], color="blue")
        sns.lineplot(x=seconds, y=wing_distance, ax=ax2, color="green")

        axs[i - 1, j - 1].set_xlabel("Second")
        # axs[i - 1, j - 1].set_ylabel("Platform distance (mm)")
        # axs[i - 1, j - 1].set_yticks([-0.1, 0, 0.1, 0.2, 0.3])
        axs[i - 1, j - 1].set_ylabel("Angle")
        axs[i - 1, j - 1].set_yticks([0, 50, 100, 150, 200])
        axs[i - 1, j - 1].set_title(f"Trial {t + 1}")
        t += 1
    print(f"Plotting {fly_num}'s data")
    plt.suptitle(str(fly_num), fontsize=20)
    plt.tight_layout()  # Adjust subplot layout
    plt.savefig("KirExp_WT_CTF" + str(fly_num) + ".png")  # Save the figure
    plt.close()
def Platform_data_preprocessing(Fly_kinematic_data, clip_start, clip_end):
    Platform_collected_data = dict()
    Platform_collected_data["Unprocessed"] = [[] for i in range(20)]
    Platform_collected_data["BestFitLine"] = [[] for i in range(20)]
    Platform_collected_data["Residual"] = [[] for i in range(20)]
    Platform_collected_data["Filtered"] = [[] for i in range(20)]
    Platform_collected_data["FilteredAverage"] = None
    Platform_collected_data["UnfilteredAverage"] = None
    Filtered_platform_data = []
    Unfiltered_platform_data = []

    for t, trial_kinematic in enumerate(Fly_kinematic_data):
        platform_distance = CalculateDistance_Platform_RmCT(trial_kinematic[clip_start:clip_end], "platform", "R-mCT")
        platform_distance = determine_smooth_amplify_curve(platform_distance, 3, True)
        Platform_collected_data["Unprocessed"][t] = platform_distance
        try:
            params, covariance = curve_fit(two_phase_decay_func, range(len(platform_distance)), platform_distance, maxfev=10000)
            a1, b1, a2, b2, c = params
            y_pred = two_phase_decay_func(range(len(platform_distance)), a1, b1, a2, b2, c)
            residual = [abs(p) ** 0.5 for p in np.asarray(platform_distance) - y_pred]
            Platform_collected_data["BestFitLine"][t] = y_pred
            Platform_collected_data["Residual"][t] = residual
        except (ValueError, RuntimeError) as e:
            pass
        if len([q for q in Platform_collected_data["Residual"][t][:300] if q > 0.13]) > 30:
            Platform_collected_data["Filtered"][t] = True
        else:
            Platform_collected_data["Filtered"][t] = False
            Filtered_platform_data.append(platform_distance)
        Unfiltered_platform_data.append(platform_distance)
    Platform_collected_data["FilteredAverage"] = CalculatePlatform_distance_average(Filtered_platform_data)
    Platform_collected_data["UnfilteredAverage"] = CalculatePlatform_distance_average(Unfiltered_platform_data)
    return Platform_collected_data
def PlotWingAngleDistribution(AngleData, kinematic_pose_data):
    global Analysis_start
    global Analysis_end
    global Customized_wing_threshold
    i = 0
    j = 0
    t = 0
    fig, axs = plt.subplots(nrows=5, ncols=6, figsize=(20, 16))
    for key in AngleData.keys():
        if i % 5 == 0:
            j += 1
            i = 1
        else:
            i += 1
        R_wing = []
        L_wing = []
        for trial_angle, trial_kinematic in zip(AngleData[key], kinematic_pose_data[key]):
            DataToBeShown = TraceData_Preprocessing(trial_angle, trial_kinematic, Analysis_start, Analysis_end)
            #moment_of_contact_manual = platform_moc.iloc[int(fly) - 1][f"Trial_{t + 1}"]
            #moment_of_landing = mol_data.iloc[int(fly) - 1][f"Trial_{t + 1}"]

            nan_count = DataToBeShown["RightWingAngle"].isna().sum()

            percentage_nan = (nan_count / len(AngleData)) * 100
            moment_of_contact = 0
            stop_dropping = 0
            # Determine validity of the data
            # print(f"Fly: {fly}---Trial{trial}")
            if percentage_nan < 50:
                R_wing.extend(DataToBeShown["RightWingAngle"])
                L_wing.extend(DataToBeShown["LeftWingAngle"])
                # sns.lineplot(x=[i / 250 for i in range(len(DataToBeShown["RightWingAngle"]))], y=DataToBeShown["RightWingAngle"], ax=axs[i - 1, j - 1], color="orange")
                # sns.lineplot(x=[i / 250 for i in range(len(DataToBeShown["RightWingAngle"]))], y=DataToBeShown["LeftWingAngle"], ax=axs[i - 1, j - 1], color="blue")

        if not len(R_wing) == 0:
            sns.histplot(R_wing, binwidth=2, ax=axs[i - 1, j - 1], color="orange", kde=True)
            sns.histplot(L_wing, binwidth=2, ax=axs[i - 1, j - 1], color="blue", kde=True)
            bin_width = 2

            # Calculate the number of bins
            bin_range = np.arange(min(R_wing), max(R_wing) + bin_width, bin_width)

            # Calculate histogram
            hist, bin_edges = np.histogram(R_wing, bins=bin_range)
            max_f = 0
            # Print bin edges and frequencies

            # axs[i - 1, j - 1].axvline(Customized_wing_threshold[int(key) - 1], color="black")

        axs[i - 1, j - 1].set_title(f"Fly {key}")
        # axs[i - 1, j - 1].set_ylabel("Wing Angle")
        # axs[i - 1, j - 1].set_xlabel("Time (s)")
        axs[i - 1, j - 1].set_xlabel("Wing Angle")
        print(f"Plotting {key} data")
        # axs[i - 1, j - 1].set_xticks([50, 100, 150, 200])
        # axs[i - 1, j - 1].set_ylim(0, 350)
    # plt.suptitle(f"Fly {key}")
    plt.tight_layout()
    # print(f"Plotting fly {key} data")
    plt.savefig("Trace_Superimposed.png")  # Save the figure
    plt.close()

"""
These functions are responsible for extracting and writing the data from and to CSV file.
"""
# Extract the data path of the csv files and organize them in the order by fly number
def Extract_data_path(angles_folder):
    Data_by_date = dict()
    Angles_data_directory = []
    parent_list = sorted(os.listdir(angles_folder), key=len)

    # Sort the angles csv files by date
    for file in parent_list:
        if file.endswith('.csv'):
            angle_csv_path = os.path.join(angles_folder, file)
            Angles_data_directory.append(angle_csv_path)
            # Split the string by underscores and hyphens to extract the date components
            components = file.split('-')
            d = components[2].split("_")

            date = components[0] + components[1] + d[0]
            if str(date) not in Data_by_date.keys():
                Data_by_date[str(date)] = []
            Data_by_date[str(date)].append(angle_csv_path)
    for date_key, value in Data_by_date.items():
        sort_by_fly_num = dict()
        for fly in Data_by_date[date_key]:
            fly_num_and_trial_parsed = fly[fly.find("_Fly"):].split("_")
            if str(fly_num_and_trial_parsed[2]) not in sort_by_fly_num.keys():
                sort_by_fly_num[str(fly_num_and_trial_parsed[2])] = []
            sort_by_fly_num[str(fly_num_and_trial_parsed[2])].append(fly)
        Data_by_date[date_key] = sort_by_fly_num

    # Sort the path by total fly num
    data_path_by_fly = dict()
    f = 0
    for date_key, value in Data_by_date.items():
        for key_f, trials_data_path in Data_by_date[date_key].items():
            # print(trials_data_path)
            f += 1
            Single_Fly_Data_Path = []
            for trial in trials_data_path:
                Single_Fly_Data_Path.append(trial)
            data_path_by_fly[f"Fly_{f}"] = Single_Fly_Data_Path
    return data_path_by_fly
def Extract_3D_pose_data(Data_by_fly, fly_num=0):
    Pose_Data = dict()
    if fly_num != 0:
        for key, value in Data_by_fly.items():
            fnum = key.split('_')
            if int(fnum[-1]) == fly_num:
                print(f"Extracting Fly {key}'s pose data")
                Pose_Data[key] = Read_Single_fly_data(value)
    else:
        for key, value in Data_by_fly.items():
            print(f"Extracting Fly {key}'s pose data")
            Pose_Data[key] = Read_Single_fly_data(value)
    return Pose_Data
def Read_Single_fly_data(Trials_Data):
    Fly_data = []
    for trial_path in Trials_Data:
        Fly_data.append(pd.read_csv(trial_path))
    return Fly_data
def Analyze_3D_pose_data(posedata):
    Landing_Data = []
    LandingLatency_Data = []
    for fly_num, indi_fly_pose in posedata.items():
        Single_Fly_Landing_Prob_Data = []
        Single_Fly_Landing_Late_Data = []
        t = 0
        # print("*" * 10)
        for trial_pose in indi_fly_pose:
            t += 1
            Right_Wing_Landing, right_latency = WingAngle_DetermineLanding(trial_pose["RightWingAngle"], trial_pose["platform"], fly_num, t)
            Left_Wing_Landing, left_latency = WingAngle_DetermineLanding(trial_pose["LeftWingAngle"], trial_pose["platform"], fly_num, t)
            # print("Fly " + fly_num + f" Trial{t}--Right Wing: {Right_Wing_Landing} Left Wing {Left_Wing_Landing}")
            if Right_Wing_Landing == 1 and Left_Wing_Landing == 1:
                Single_Fly_Landing_Prob_Data.append(1)
                Single_Fly_Landing_Late_Data.append(max([right_latency, left_latency]))
            elif Right_Wing_Landing == 0 and Left_Wing_Landing == 0:
                Single_Fly_Landing_Prob_Data.append(-1)
                Single_Fly_Landing_Late_Data.append(0)
            elif Right_Wing_Landing == 2 or Left_Wing_Landing == 2:
                Single_Fly_Landing_Prob_Data.append(0)
                Single_Fly_Landing_Late_Data.append(0)
            elif (Right_Wing_Landing == 1 and Left_Wing_Landing == 0) or (Right_Wing_Landing == 0 and Left_Wing_Landing == 1):
                Single_Fly_Landing_Prob_Data.append(-1)
                Single_Fly_Landing_Late_Data.append(0)
            else:
                Single_Fly_Landing_Prob_Data.append(np.nan)
                Single_Fly_Landing_Late_Data.append(0)
        Landing_Data.append(Single_Fly_Landing_Prob_Data)
        LandingLatency_Data.append(Single_Fly_Landing_Late_Data)
    return Landing_Data, LandingLatency_Data
def Write_to_csv(LandingProbData, LandingLatencyData, output_path, compare_path):
    Manual_data = pd.read_excel(compare_path)
    T = ["Trial_" + str(i) for i in range(1, 21)]
    Manual_data = Manual_data[T]
    # Create an Excel writer using openpyxl
    excel_writer = pd.ExcelWriter(output_path, engine='openpyxl')
    LandingProbData.to_excel(excel_writer, index=False, sheet_name='Sheet1')
    # Access the workbook and sheet
    workbook = excel_writer.book
    sheet = workbook['Sheet1']

    # Define cell colors
    yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
    orange_fill = PatternFill(start_color='FFC000', end_color='FFC000', fill_type='solid')
    red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
    blue_fill = PatternFill(start_color='9BC2E6', end_color='9BC2E6', fill_type='solid')
    gray_fill = PatternFill(start_color='696969', end_color='696969', fill_type='solid')

    # Apply cell colors based on conditions
    for row_idx in range(2, sheet.max_row + 1):  # Start from row 2 (excluding header)
        for col_idx in range(2, sheet.max_column + 1):  # Start from column 2 (excluding Fly# column)
            cell_value = sheet.cell(row=row_idx, column=col_idx).value
            cell = sheet.cell(row=row_idx, column=col_idx)
            if cell_value == 1:
                if isinstance(Manual_data[T].iloc[row_idx - 2][col_idx - 2], str):
                    cell.fill = gray_fill
                else:
                    if Manual_data[T].iloc[row_idx - 2][col_idx - 2] > 1:
                        cell.fill = yellow_fill
                    else:
                        cell.fill = gray_fill
                cell.value = LandingLatencyData[row_idx - 2][col_idx - 2]
            elif cell_value == -1:
                if Manual_data[T].iloc[row_idx - 2][col_idx - 2] == -1:
                    cell.fill = orange_fill
                else:
                    cell.fill = gray_fill
            elif cell_value == 0:
                if isinstance(Manual_data[T].iloc[row_idx - 2][col_idx - 2], str):
                    if Manual_data[T].iloc[row_idx - 2][col_idx - 2] == "NotFlying":
                        cell.fill = blue_fill
                    else:
                        cell.fill = gray_fill
                else:
                    cell.fill = gray_fill
                cell.value = "NotFlying"
            elif isinstance(type(cell_value), type(str)):
                # print("N/A")
                # print(cell_value)
                if pd.isna(Manual_data[T].iloc[row_idx - 2][col_idx - 2]):
                    cell.fill = red_fill
                else:
                    cell.fill = gray_fill
                cell.value = 'N/A'
    # Save the Excel file
    excel_writer.save()
    print("Excel file has been created with modifications.")
def Create_DataSets_MetaData():
    DataSetsMetaData = dict()
    DataSetsMetaData["StarvedExperiment"] = dict()
    DataSetsMetaData["StarvedExperiment"]["Angles_Folder"] = r"C:\Users\agrawal-admin\Desktop\Anipose Predicted Data\Testing_Network_for_wing_angle-05-08-2024\Starved_fly_exp_analysis_result\angles"
    DataSetsMetaData["StarvedExperiment"]["Pose_3D_Folder"] = r"C:\Users\agrawal-admin\Desktop\Anipose Predicted Data\Testing_Network_for_wing_angle-05-08-2024\Starved_fly_exp_analysis_result\pose-3d"
    DataSetsMetaData["StarvedExperiment"]["Prediction_output_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\KinematicsAnalysis_Starved.xlsx"
    DataSetsMetaData["StarvedExperiment"]["Manual_LL_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\Starved_CTF.xlsx"
    DataSetsMetaData["StarvedExperiment"]["Analysis_Start_time"] = 450
    DataSetsMetaData["StarvedExperiment"]["Analysis_End_time"] = 1050
    DataSetsMetaData["StarvedExperiment"]["Actual_Video_time"] = 0
    DataSetsMetaData["StarvedExperiment"]["FPS"] = 250

    DataSetsMetaData["Control_T2_CTF_Experiment"] = dict()
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Angles_Folder"] = r"C:\Users\agrawal-admin\Desktop\Anipose Predicted Data\Testing_Network_for_wing_angle-05-08-2024\Control_T2_CTF-2024-05-10\angles"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Pose_3D_Folder"] = r"C:\Users\agrawal-admin\Desktop\Landing_3D-Wayne-2024-01-25\videos\pose-3d"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Prediction_output_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\KinematicsAnalysis.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Manual_LL_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\CorrectedLabeled_data.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Manual_MOC_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Platform_moc.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Manual_MOL_csv_file"] = r"C:\Users\agrawal-admin\Desktop\T2_CTF_All_Corrected.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Analysis_Start_time"] = 540
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Analysis_End_time"] = 1250
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Actual_Video_time"] = 250
    DataSetsMetaData["Control_T2_CTF_Experiment"]["FPS"] = 300

    DataSetsMetaData["KirExperiment"] = dict()
    DataSetsMetaData["KirExperiment"]["Angles_Folder"] = r"C:\Users\agrawal-admin\Desktop\Kristen Data\KirControl-TTa\Angle Data"
    DataSetsMetaData["KirExperiment"]["Pose_3D_Folder"] = r"C:\Users\agrawal-admin\Desktop\Kristen Data\KirControl-TTa\3D Data"
    DataSetsMetaData["KirExperiment"]["DestinationFolder"] = r"C:\Users\agrawal-admin\Desktop\Kristen Data\KirControl-TTa\Graphs"
    DataSetsMetaData["KirExperiment"]["Analysis_Start_time"] = 300
    DataSetsMetaData["KirExperiment"]["Analysis_End_time"] = 900
    DataSetsMetaData["KirExperiment"]["Actual_Video_time"] = 250
    DataSetsMetaData["KirExperiment"]["FPS"] = 300
    return DataSetsMetaData
def Read_Manual_Data(file_path):
    Trial_num = 20
    Trial_num_list = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    Manual_data = pd.read_excel(file_path)[Trial_num_list]
    return Manual_data
def Calculate_Median_MOC(kinematic_data, angle_data, manual_platform_moc, lower_bound_percentile, upper_bound_percentile):
    global Analysis_start
    global Analysis_end
    i = 0
    j = 0
    filtered_moc_platform_distances = []
    moc_time_points = []
    for key in kinematic_data.keys():
        t = 0
        for k, p in (zip(kinematic_data[key], angle_data[key])):
            Data = TraceData_Preprocessing(p, k, Analysis_start, Analysis_end)
            moment_of_contact = manual_platform_moc.iloc[int(key) - 1][f"Trial_{t + 1}"]
            if not (isinstance(moment_of_contact, str) or pd.isna(moment_of_contact) or moment_of_contact < 0):
                moment_of_contact = int(moment_of_contact) - Analysis_start
                moc_time_points.append(moment_of_contact)
            t += 1
    lower_bound = np.percentile(moc_time_points, lower_bound_percentile)
    upper_bound = np.percentile(moc_time_points, upper_bound_percentile)
    filtered_moc_time_point = []

    for key in kinematic_data.keys():
        t = 0
        for k, p in (zip(kinematic_data[key], angle_data[key])):
            Data = TraceData_Preprocessing(p, k, Analysis_start, Analysis_end)
            moment_of_contact = manual_platform_moc.iloc[int(key) - 1][f"Trial_{t + 1}"]
            if not (isinstance(moment_of_contact, str) or pd.isna(moment_of_contact) or moment_of_contact < 0):
                moment_of_contact = int(moment_of_contact) - Analysis_start
                if lower_bound <= moment_of_contact <= upper_bound:
                    filtered_moc_time_point.append(moment_of_contact)
                    filtered_moc_platform_distances.append(np.mean(Data["platform"][moment_of_contact - 5:moment_of_contact + 5]))
            t += 1
    platform_idx_min = min(filtered_moc_time_point)
    platform_idx_max = max(filtered_moc_time_point)
    median_moc = np.median(filtered_moc_platform_distances)
    return median_moc, platform_idx_min, platform_idx_max
def find_linear_best_fit_line(X, Y):
    x = np.array(X).reshape(-1, 1)
    y = np.array(Y)
    model = LinearRegression()
    try:
        model.fit(x, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        line = (slope * x + intercept).flatten()
        x_flat = x.flatten()
        print(f"Slope {slope}, Intercept: {intercept}")
        return x_flat, line
    except ValueError as v:
        print(f"Encountered: {v}")
        pass
def determine_floating_threshold(baseline, slope, intercept):
    return slope * baseline + intercept
def add_column_to_csv(filename, new_column_name, new_column_data):
    # Check if the file exists and is not empty
    try:
        with open(filename, 'r') as f:
            if f.read().strip():
                df = pd.read_csv(filename)
            else:
                df = pd.DataFrame()
    except FileNotFoundError:
        df = pd.DataFrame()
    # Add the new column to the DataFrame
    new_length = len(new_column_data)
    if new_length > len(df):
        df = df.reindex(range(new_length))
    df[new_column_name] = pd.Series(new_column_data)

    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)
def sigmoid(x, L, x0, k):
    return L / (1 + np.exp(-k * (x - x0)))
def Fit_sigmoid(X, Y):
    x_data = np.array(X)
    y_data = np.array(Y)
    # Initial guess for the parameters
    if x_data.shape[0] != y_data.shape[0]:
        raise ValueError("x_data and y_data must have the same length")
    L_initial = max(y_data)
    x0_initial = np.median(x_data)
    k_initial = 1.0

    initial_guess = [L_initial, x0_initial, k_initial]

    # Curve fitting
    params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_guess)

    # Extracting the parameters
    L_fit, x0_fit, k_fit = params

    # Generating y values using the fitted sigmoid function
    y_fit = sigmoid(x_data, L_fit, x0_fit, k_fit)
    return x_data, y_fit
def group_files_by_fly(file_names):
    # Regular expression to extract the relevant parts of the file name
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2})-\d{2}-\d{2}-\d{2}\.\d+.*?_Fly_(\d+)_Trial_\d+_")
    print(pattern)
    # Dictionary to map unique combinations to "Fly_N"
    unique_combinations = {}
    grouped_files = {}

    current_fly_number = 1  # Counter for Fly_N keys

    for file in file_names:
        match = pattern.search(file)
        if match:
            date = match.group(1)
            fly_number = match.group(2)
            unique_id = (date, fly_number)  # Unique identifier based on date and fly number

            # Assign a new Fly_N key if the combination is not seen before
            if unique_id not in unique_combinations:
                unique_combinations[unique_id] = f"Fly_{current_fly_number}"
                current_fly_number += 1

            # Get the Fly_N key
            fly_key = unique_combinations[unique_id]

            # Add the file to the corresponding Fly_N group
            if fly_key not in grouped_files:
                grouped_files[fly_key] = []
            grouped_files[fly_key].append(file)

    return grouped_files
def Calculate_distance_between_points(x, y, z, x1, y1, z1):
    return np.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
def Calculate_segment_length(threeD_data, skeletons):
    collected_seg_length_data = dict()
    for seg in skeletons:
        if f"{seg[0]}_{seg[1]}" not in collected_seg_length_data.keys():
            collected_seg_length_data[f"{seg[0]}_{seg[1]}"] = []
        for f in range(len(threeD_data)):
            collected_seg_length_data[f"{seg[0]}_{seg[1]}"].append(Calculate_distance_between_points(
                threeD_data[f"{seg[0]}_x"][f], threeD_data[f"{seg[0]}_y"][f], threeD_data[f"{seg[0]}_z"][f],
                threeD_data[f"{seg[1]}_x"][f], threeD_data[f"{seg[1]}_y"][f], threeD_data[f"{seg[1]}_z"][f]))
    collected_seg_length_data = pd.DataFrame(collected_seg_length_data)
    return collected_seg_length_data
def calculate_angle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    # Define points as numpy arrays
    pt1 = np.array([x1, y1, z1])
    pt2 = np.array([x2, y2, z2])
    pt3 = np.array([x3, y3, z3])

    # Define vectors
    vecA = pt1 - pt2
    vecB = pt3 - pt2

    # Calculate dot product and magnitudes
    dot_product = np.dot(vecA, vecB)
    magnitude_A = np.linalg.norm(vecA)
    magnitude_B = np.linalg.norm(vecB)

    # Calculate angle in radians
    angle_rad = np.arccos(dot_product / (magnitude_A * magnitude_B))

    # Convert to degrees if needed
    angle_deg = np.degrees(angle_rad)

    return angle_deg
def Calculate_joint_angle(threeD_data, angles):
    collected_angle_data = dict()
    for ag in angles:
        if f"{ag[1]}" not in collected_angle_data.keys():
            collected_angle_data[f"{ag[1]}"] = []
        for f in range(len(threeD_data)):
            angle = calculate_angle(
                threeD_data[f"{ag[0]}_x"][f], threeD_data[f"{ag[0]}_y"][f], threeD_data[f"{ag[0]}_z"][f],
                threeD_data[f"{ag[1]}_x"][f], threeD_data[f"{ag[1]}_y"][f], threeD_data[f"{ag[1]}_z"][f],
                threeD_data[f"{ag[2]}_x"][f], threeD_data[f"{ag[2]}_y"][f], threeD_data[f"{ag[2]}_z"][f])
            collected_angle_data[f"{ag[1]}"].append(angle)
    return collected_angle_data
def TransposeData(df):
    df = pd.DataFrame(df)
    df = df.T
    return df
def Calculate_derivative(data):
    if len(data) < 2:
        raise ValueError("The input list must contain at least two elements to calculate a derivative.")

    # Compute the differences between consecutive elements
    data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
    data = [abs(x) for x in data]
    return data
def plane_from_points(p1, p2):
    # Compute the normal vector of the plane using two points
    v1 = np.array(p2) - np.array(p1)
    normal = np.cross(v1, [0, 0, 1])  # Assume a vertical normal projection
    d = -np.dot(normal, p1)
    return normal, d
def line_plane_intersection(p1, p2, normal, d):
    # Line represented as p(t) = p1 + t * (p2 - p1)
    direction = np.array(p2) - np.array(p1)
    denom = np.dot(normal, direction)

    if abs(denom) < 1e-6:  # Parallel case
        return None

    t = -(np.dot(normal, p1) + d) / denom
    if 0 <= t <= 1:  # Ensure intersection is within the segment
        return p1 + t * direction
    return None
def is_inside_circle(intersection, center, radius):
    return np.linalg.norm(intersection - center) <= radius
def check_leg_platform_intersection(leg_p1, leg_p2, center_traces):
    # Compute platform radius
    radius = 0.38
    # Compute the plane equation
    centroid, platform_direction = best_fit_line_3d(center_traces)

    d = -np.dot(platform_direction, center_traces[-1])

    # Find intersection point
    intersection = line_plane_intersection(np.array(leg_p1), np.array(leg_p2), platform_direction, d)

    if intersection is not None and is_inside_circle(intersection, np.array(center_traces[-1]), radius):
        return True
    return False
def ReadCoordsAll(threeD_data, fnum):
    points = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip", "platform-tip", "L-platform-tip",
              "R-platform-tip", "platform-axis", "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT", "R-mBC", "R-mCT", "R-mFT",
              "R-mTT", "R-mLT", "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT", "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
              "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT", "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]
    coords = dict()
    for p in points:
        coords[p] = np.asarray([threeD_data[f"{p}_x"][fnum], threeD_data[f"{p}_y"][fnum], threeD_data[f"{p}_z"][fnum]])
    return coords
def plot_motion_vector_with_plane(platform_ctr_pts_traces, coords):
    keypoint_pairs = [
        ["L-wing", "L-wing-hinge"], ["R-wing", "R-wing-hinge"], ["abdomen-tip"],
        ["platform-tip"], ["L-platform-tip"], ["R-platform-tip"], ["platform-axis"],
        ["R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT"], ["R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT"],
        ["R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"], ["L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT"],
        ["L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT"], ["L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]
    ]

    platform_ctr_pts_traces = np.array(platform_ctr_pts_traces)
    centroid, direction = best_fit_line_3d(platform_ctr_pts_traces)

    # Generate points along the best-fit line
    t_vals = np.linspace(-10, 10, 100)
    line_points = centroid + np.outer(t_vals, direction)

    # Create color gradient based on the order of the points
    num_points = len(platform_ctr_pts_traces)
    colors = plt.cm.Greys(np.linspace(0, 1, num_points))

    # Generate a normal plane to the direction vector at the centroid
    normal_vector = direction
    # Create two perpendicular vectors using cross products
    if np.allclose(normal_vector, [1, 0, 0]):  # Handle edge case if aligned with x-axis
        perp_vector1 = np.cross(normal_vector, [0, 1, 0])
    else:
        perp_vector1 = np.cross(normal_vector, [1, 0, 0])

    perp_vector1 /= np.linalg.norm(perp_vector1)  # Normalize

    perp_vector2 = np.cross(normal_vector, perp_vector1)
    perp_vector2 /= np.linalg.norm(perp_vector2)  # Normalize

    radius = 0.4  # Radius of the circular plane

    # Generate a circular grid
    u_vals = np.linspace(-radius, radius, 50)
    v_vals = np.linspace(-radius, radius, 50)
    U, V = np.meshgrid(u_vals, v_vals)

    # Convert to polar coordinates to filter for a circular region
    mask = U ** 2 + V ** 2 <= radius ** 2  # Boolean mask for circle

    # Apply mask to keep only circular region
    U = U[mask]
    V = V[mask]

    plane_points = platform_ctr_pts_traces[-1] + U[..., None] * perp_vector1 + V[..., None] * perp_vector2

    # 3D Plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Loop through the connections and plot lines
    Colors = [
        "#FF0000", "#008000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#000000",
         "#808080", "#A9A9A9", "#D3D3D3", "#FFA500", "#800080", "#A52A2A",
        "#FFC0CB", "#ADD8E6", "#00FF00", "#4B0082", "#EE82EE", "#FFD700", "#C0C0C0",
        "#D2B48C", "#FF7F50", "#006400", "#00008B", "#8B0000", "#FF8C00", "#8B008B",
        "#708090", "#FF6347", "#008080"
    ]
    """for g, group in enumerate(keypoint_pairs):
        for i in range(len(group) - 1):  # Connect points in the group
            p1 = coords[group[i]]
            p2 = coords[group[i + 1]]

            # Plot a line between p1 and p2
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], marker='o', color=Colors[g])"""

    ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector1, color='r', arrow_length_ratio=0.1)
    ax.quiver(*platform_ctr_pts_traces[-1], *perp_vector2, color='r', arrow_length_ratio=0.1)
    # Plot the trajectory with color gradient
    for i in range(num_points - 1):
        ax.plot(platform_ctr_pts_traces[i:i + 2, 0], platform_ctr_pts_traces[i:i + 2, 1], platform_ctr_pts_traces[i:i + 2, 2], color=colors[i], linewidth=6)

    # Plot the best-fit line
    ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], 'r--', label="Best-Fit Line")

    # Highlight the centroid
    # ax.scatter(centroid[0], centroid[1], centroid[2], color='black', s=100, label="Centroid", edgecolors='k')

    # Plot the normal plane
    ax.plot_trisurf(plane_points[:, 0], plane_points[:, 1], plane_points[:, 2], color='cyan', alpha=0.5)


    # Labels and legend
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Motion with Normal Plane")
    axis_limit = 2  # Adjust this value based on your data range
    ax.set_xlim([-axis_limit, axis_limit])
    ax.set_ylim([-axis_limit, axis_limit])
    ax.set_zlim([-axis_limit, axis_limit])
    ax.legend()

    azim = np.arctan2(normal_vector[1], normal_vector[0]) * 180 / np.pi

    # Elevation is calculated based on the z-component of the vector
    plt.gca().set_aspect('equal')
    ax.view_init(elev=90, azim=0)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))  # Make panes transparent
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.set_axis_off()  # This removes everything including the frame
    plt.show(block=True)
def best_fit_line_3d(points):
    points = np.array(points)
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    _, _, Vt = np.linalg.svd(centered_points)
    direction = Vt[0]  # First principal component
    return centroid, direction

Angles = [["R-mBC", "R-mCT", "R-mFT"],
          ["R-mCT", "R-mFT", "R-mTT"],
          ["R-mFT", "R-mTT", "R-mLT"]]
# skeletons = [["R-mTT", "L-platform-tip"], ["R-mTT", "R-platform-tip"], ["R-mTT", "platform-tip"]]
skeletons = [["R-mLT", "L-platform-tip"], ["R-mLT", "R-platform-tip"], ["R-mLT", "platform-tip"]]
skeletons = [["R-mLT", "platform-tip"]]
DataDirPath = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data\WT-Control_T2-TiTa_ImprovedNetwork"
MOCfilePath = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data\WT-Control_T2-TiTa_ImprovedNetwork\T2-TiTaLPDataMOC.xlsx"
MOLfilePath = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data\WT-Control_T2-TiTa_ImprovedNetwork\T2-TiTaLPDataMOL.xlsx"
Trials = [f"Trial_{i + 1}" for i in range(20)]
AllFiles = []
for root, dirs, files in os.walk(DataDirPath):
    for file in files:
        if file.endswith(".csv"):
            input_file_path = os.path.join(root, file)
            AllFiles.append(input_file_path)
moc_data = pd.read_excel(MOCfilePath)[Trials]
grouped_data_path = group_files_by_fly(AllFiles)



"""mean_moc = []
for index, r in moc_data[Trials].iterrows():
    for i, t in enumerate(r):
        if not isinstance(t, str) and t > -1:
            print(t, f"Fly {index + 1}", f"Trial {i + 1}")
            data = pd.read_csv(grouped_data_path[f"Fly_{index + 1}"][i])
            seg_length = Calculate_segment_length(data, skeletons)
            # seg_length = TransposeData(seg_length)
            # column_means = seg_length.mean(axis=0)
            mean_moc.append(np.mean(seg_length["R-mLT_platform-tip"][int(t) - 2:int(t) + 2]))
sns.stripplot(mean_moc, size=5, alpha=0.5)
plt.xlabel(r"R-mLT --> platform tip")
plt.ylabel(f"Distance at MOC (mm)")
plt.savefig("distance at moc RmLT.pdf")
plt.show()"""

"""fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 16))
i = 0
j = 0
t = 0
for d in grouped_data_path["Fly_1"]:
    t += 1
    data = pd.read_csv(d)[200:800]
    data = data.reset_index()

    seg_length = Calculate_segment_length(data, skeletons)
    # seg_length = TransposeData(seg_length)

    # column_means = seg_length.mean(axis=0)
    # column_means_derivative = Calculate_derivative(column_means)

    angles = Calculate_joint_angle(data, Angles)

    if i % 5 == 0:
        j += 1
        i = 1
    else:
        i += 1
    seconds = [x/200 for x in range(200, 800)]
    # print(seconds)
    sns.lineplot(x=seconds, y=seg_length["R-mTT_platform-tip"], legend=False, ax=axs[i - 1, j - 1])
    # print(moc)
    moc = moc_data.iloc[0][t - 1]
    if not isinstance(moc, str) and moc > -1:
        axs[i - 1, j - 1].axvline(moc/200, color="black")
    axs[i - 1, j - 1].set_ylim(-0.1, 3)
    axs[i - 1, j - 1].set_title(f"Trial {t}")
    axs[i - 1, j - 1].set_ylabel("Distance (mm)")
    axs[i - 1, j - 1].set_xlabel("Seconds (mm)")
    print(f"Processing Trial {t}")
    # ax2 = axs[i - 1, j - 1].twinx()
    # ax2.set_ylim(0, 200)
    # sns.lineplot(column_means_derivative, legend=False, ax=ax2, color="orange")
    # sns.lineplot(angles["R-mCT"], legend=False, ax=ax2, color="green")
    # sns.lineplot(angles["R-mTT"], legend=False, ax=ax2, color="red")

plt.tight_layout()
plt.savefig("R-mTT platform distance.pdf")
plt.show()"""




moc_error = []
for index, r in moc_data[Trials].iloc[:2].iterrows():
    for i, t in enumerate(r):
        if not isinstance(t, str) and t > -1:
            print(f"Fly {index + 1}", f"Trial {i + 1}")
            data = pd.read_csv(grouped_data_path[f"Fly_{index + 1}"][i])
            start = 200
            end = 800

            center_points = np.asarray(
                [data["platform-tip_x"].tolist(), data["platform-tip_y"].tolist(), data["platform-tip_z"].tolist()])
            R_mTT_points = np.asarray([data["R-mTT_x"].tolist(), data["R-mTT_y"].tolist(), data["R-mTT_z"].tolist()])
            R_mLT_points = np.asarray([data["R-mLT_x"].tolist(), data["R-mLT_y"].tolist(), data["R-mLT_z"].tolist()])

            center_points = np.transpose(center_points)
            R_mTT_points = np.transpose(R_mTT_points)
            R_mLT_points = np.transpose(R_mLT_points)

            for i in range(start, end):
                if check_leg_platform_intersection(R_mTT_points[i], R_mLT_points[i], center_points[i - start:i]):
                    name_width = 8
                    num_width = 3
                    name = "Prediction:"
                    name1 = "Manual:"
                    name2 = "Error:"
                    print(f"{name:<{name_width}} {str(i):>{num_width}} {name1:<{name_width}} {str(t):>{num_width}} {name2:<{name_width}} {str(i - t):>{num_width}}")
                    moc_error.append(i - t)
                    if abs(i - t) > 20:
                        coords = ReadCoordsAll(data, i)
                        plot_motion_vector_with_plane(center_points[i - start:i], coords)
                    break
sns.stripplot(moc_error)
plt.show()

"""start = 200
end = 800
# Example usage
data = pd.read_csv(grouped_data_path["Fly_1"][0])
# coords = ReadCoordsAll(data, 400)

center_points = np.asarray([data["platform-tip_x"].tolist(), data["platform-tip_y"].tolist(), data["platform-tip_z"].tolist()])
R_mTT_points = np.asarray([data["R-mTT_x"].tolist(), data["R-mTT_y"].tolist(), data["R-mTT_z"].tolist()])
R_mLT_points = np.asarray([data["R-mLT_x"].tolist(), data["R-mLT_y"].tolist(), data["R-mLT_z"].tolist()])

center_points = np.transpose(center_points)
R_mTT_points = np.transpose(R_mTT_points)
R_mLT_points = np.transpose(R_mLT_points)

for i in range(start, end):
    if check_leg_platform_intersection(R_mTT_points[i], R_mLT_points[i], center_points[i - start:i]):
        print(i)
        break"""
# plot_motion_vector_with_plane(center_points[:400], coords)


