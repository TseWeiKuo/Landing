
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import json
import sys
import os
import seaborn as sns
from scipy.stats import sem
from matplotlib.gridspec import GridSpec
from scipy.stats import ttest_ind, ttest_rel
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
    return p_value < alpha, p_value, t_stat
def Calculate_distance_between_points(x, y, z, x1, y1, z1):
    return np.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
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
def Calculate_segment_length(threeD_data, skeletons):
    collected_seg_length_data = dict()
    for seg in skeletons:
        if f"{seg[0]}_{seg[1]}" not in collected_seg_length_data.keys():
            collected_seg_length_data[f"{seg[0]}_{seg[1]}"] = []
        for f in range(len(threeD_data)):
            collected_seg_length_data[f"{seg[0]}_{seg[1]}"].append(Calculate_distance_between_points(
                threeD_data[f"{seg[0]}_x"][f], threeD_data[f"{seg[0]}_y"][f], threeD_data[f"{seg[0]}_z"][f],
                threeD_data[f"{seg[1]}_x"][f], threeD_data[f"{seg[1]}_y"][f], threeD_data[f"{seg[1]}_z"][f]))
    return collected_seg_length_data
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
def Calculate_joint_angle_change(threeD_data, angles):
    global frames_num
    collected_angle_data = dict()
    for ag in angles:
        if f"{ag[0]}_{ag[1]}_{ag[2]}" not in collected_angle_data.keys():
            collected_angle_data[f"{ag[0]}_{ag[1]}_{ag[2]}"] = []
        for f in range(0, frames_num - 1):
            angle_change = calculate_angle(
                threeD_data[f"{ag[0]}_x"][f], threeD_data[f"{ag[0]}_y"][f], threeD_data[f"{ag[0]}_z"][f],
                threeD_data[f"{ag[1]}_x"][f], threeD_data[f"{ag[1]}_y"][f], threeD_data[f"{ag[1]}_z"][f],
                threeD_data[f"{ag[2]}_x"][f], threeD_data[f"{ag[2]}_y"][f], threeD_data[f"{ag[2]}_z"][f]) - \
                           calculate_angle(
                threeD_data[f"{ag[0]}_x"][f + 1], threeD_data[f"{ag[0]}_y"][f + 1], threeD_data[f"{ag[0]}_z"][f + 1],
                threeD_data[f"{ag[1]}_x"][f + 1], threeD_data[f"{ag[1]}_y"][f + 1], threeD_data[f"{ag[1]}_z"][f + 1],
                threeD_data[f"{ag[2]}_x"][f + 1], threeD_data[f"{ag[2]}_y"][f + 1], threeD_data[f"{ag[2]}_z"][f + 1])
            collected_angle_data[f"{ag[0]}_{ag[1]}_{ag[2]}"].append(angle_change)
    return collected_angle_data
def Detect_3D_inaccuracy_exceeding_threshold(Data):
    wind_size = 5
    baseline = np.average(Data[:200])
    inaccuracy_start_ind = []
    inaccuracy_stop_ind = []
    inaccurate_frames_count = 0
    repeat = False
    threshold_range = 0.1
    for i in range(0, len(Data), wind_size):
        # Detect change in segment length
        if (np.average(Data[i:i + wind_size]) > baseline * (1 + threshold_range)
                or np.average(Data[i:i + wind_size]) < baseline * (1 - threshold_range)):
            if not repeat:
                repeat = True
                inaccuracy_start_ind.append(i)
            inaccurate_frames_count += wind_size
        else:
            if repeat:
                repeat = False
                inaccuracy_stop_ind.append(i)
    return inaccurate_frames_count
def Detect_3D_inaccuracy_combined(SegLength, Velocities, Angles):
    wind_size = 5
    SegLength_baseline = np.average(SegLength[:200])
    Velocities_baseline = np.average(Velocities[:200])
    Angles_baseline = np.average(Angles[:200])
    inaccuracy_start_ind = []
    inaccuracy_stop_ind = []
    inaccurate_frames_count = 0
    repeat = False
    threshold_range = 0.1
    seg_threshold = 0.2
    for i in range(0, len(SegLength), wind_size):
        # Detect change in segment length
        if (np.average(SegLength[i:i + wind_size]) > SegLength_baseline * (1 + seg_threshold) or np.average(SegLength[i:i + wind_size]) < SegLength_baseline * (1 - seg_threshold)) and \
                (np.average(Velocities[i:i + wind_size]) > Velocities_baseline * (1 + threshold_range) or np.average(Velocities[i:i + wind_size]) < Velocities_baseline * (1 - threshold_range)) and \
                (np.average(Angles[i:i + wind_size]) > Angles_baseline * (1 + threshold_range) or np.average(Angles[i:i + wind_size]) < Angles_baseline * (1 - threshold_range)):
            if not repeat:
                repeat = True
                inaccuracy_start_ind.append(i)
            inaccurate_frames_count += wind_size
        else:
            if repeat:
                repeat = False
                inaccuracy_stop_ind.append(i)
    return inaccurate_frames_count
def Calculate_joint_velocity(threeD_data, joints):
    global frames_num
    frame_rate = 200
    collected_velocity_data = dict()
    for jt in joints:
        if jt not in collected_velocity_data.keys():
            collected_velocity_data[f"{jt}"] = []
        for f in range(0, frames_num - 1):
            collected_velocity_data[f"{jt}"].append(Calculate_distance_between_points(
                threeD_data[f"{jt}_x"][f], threeD_data[f"{jt}_y"][f], threeD_data[f"{jt}_z"][f],
                threeD_data[f"{jt}_x"][f + 1], threeD_data[f"{jt}_y"][f + 1], threeD_data[f"{jt}_z"][f + 1]) * 200)
    return collected_velocity_data
def ObtainDataPath(source_folder):
    paths = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".csv"):
                input_file_path = os.path.join(root, file)
                paths.append(input_file_path)
    return paths
def Calculate_3D_data_metrics(paths, skeletons, angles, KeyPoints):
    Collected_metrics_data = dict()
    Collected_metrics_data["Seg_Length"] = dict()
    Collected_metrics_data["Angles"] = dict()
    Collected_metrics_data["Velocities"] = dict()
    Collected_metrics_data["Combined"] = dict()
    for p in paths:
        data = pd.read_csv(p)

        Collected_segment_lengths = Calculate_segment_length(data, skeletons)
        for sk in skeletons:
            if f"{sk[0]}_{sk[1]}" not in Collected_metrics_data["Seg_Length"].keys():
                Collected_metrics_data["Seg_Length"][f"{sk[0]}_{sk[1]}"] = []
            error_counts = Detect_3D_inaccuracy_exceeding_threshold(Collected_segment_lengths[f"{sk[0]}_{sk[1]}"])
            Collected_metrics_data["Seg_Length"][f"{sk[0]}_{sk[1]}"].append(error_counts)


        Collected_velocities = Calculate_joint_velocity(data, KeyPoints)
        for jt in KeyPoints:
            if jt not in Collected_metrics_data["Velocities"].keys():
                Collected_metrics_data["Velocities"][f"{jt}"] = []
            error_counts = Detect_3D_inaccuracy_exceeding_threshold(Collected_velocities[f"{jt}"])
            Collected_metrics_data["Velocities"][f"{jt}"].append(error_counts)


        Collected_angles = Calculate_joint_angle_change(data, angles)
        for ag in angles:
            if f"{ag[0]}_{ag[1]}_{ag[2]}" not in Collected_metrics_data["Angles"].keys():
                Collected_metrics_data["Angles"][f"{ag[0]}_{ag[1]}_{ag[2]}"] = []
            error_counts = Detect_3D_inaccuracy_exceeding_threshold(Collected_angles[f"{ag[0]}_{ag[1]}_{ag[2]}"])
            Collected_metrics_data["Angles"][f"{ag[0]}_{ag[1]}_{ag[2]}"].append(error_counts)

            if f"{ag[1]}" not in Collected_metrics_data["Combined"].keys():
                Collected_metrics_data["Combined"][f"{ag[1]}"] = []
            error_counts = Detect_3D_inaccuracy_combined(Collected_segment_lengths[f"{ag[1]}_{ag[2]}"], Collected_velocities[f"{ag[2]}"],
                                                         Collected_angles[f"{ag[0]}_{ag[1]}_{ag[2]}"])
            Collected_metrics_data["Combined"][f"{ag[1]}"].append(error_counts)

    return Collected_metrics_data
def ConstructLabelsForXTicks(metrics, skeletons, angles, KeyPoints):
    collected_labels = dict()
    for m in metrics:
        collected_labels[m] = []
    for sk in skeletons:
        collected_labels["Seg_Length"].append(f"{sk[0]}_{sk[1]}")
    for ag in angles:
        collected_labels["Angles"].append(f"{ag[0]}_{ag[1]}_{ag[2]}")
        collected_labels["Combined"].append(f"{ag[1]}")
    for jt in KeyPoints:
        collected_labels["Velocities"].append(f"{jt}")
    return collected_labels
def normalize_list(data, method="min-max"):
    if method == "min-max":
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            raise ValueError("Cannot perform Min-Max normalization when all values are the same.")
        return [(x - min_val) / (max_val - min_val) for x in data]
def average_sublists(list_of_lists):
    if not list_of_lists:
        raise ValueError("The input list is empty.")

    # Check that all sublists have the same length
    sublist_length = len(list_of_lists[0])
    if not all(len(sublist) == sublist_length for sublist in list_of_lists):
        raise ValueError("All sublists must have the same length.")

    # Initialize a list to store the sum of elements
    sum_list = [0] * sublist_length

    # Calculate the sum of elements at each position
    for sublist in list_of_lists:
        for i in range(sublist_length):
            sum_list[i] += sublist[i]

    # Divide each sum by the number of sublists to compute the average
    num_sublists = len(list_of_lists)
    avg_list = [total / num_sublists for total in sum_list]

    return avg_list
def get_min_and_max(list_of_lists):
    data = np.array(list_of_lists)

    # Calculate average, min, and max along each column (axis=0)
    avg = np.mean(data, axis=0)
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    sem = np.std(data, axis=0, ddof=1) / np.sqrt(data.shape[0])
    return avg, avg - sem, avg + sem
def Calculate_derivative(data):
    if len(data) < 2:
        raise ValueError("The input list must contain at least two elements to calculate a derivative.")

    # Compute the differences between consecutive elements
    data = [data[i + 1] - data[i] for i in range(len(data) - 1)]
    data = [abs(x) for x in data]
    return data
def calculate_velocity(x, y, z, dt=1):
    if len(x) != len(y) or len(y) != len(z):
        raise ValueError("All input lists must have the same length.")

    # Compute differences between consecutive points
    dx = np.diff(x)
    dy = np.diff(y)
    dz = np.diff(z)

    # Compute velocity magnitudes
    velocities = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2) / dt

    # Return as a list
    return velocities.tolist()
def Determine_movement_start(data):
    win_size = 3
    for i in range(0, len(data)):
        if np.mean(data[i:i + win_size]) > 0.05:
            return i
    return -moc_start
def Determine_movement_stop(data, data1):
    win_size = 3
    for i in range(len(data)):
        if np.mean(data[i:i+win_size]) < 0.05 and np.mean(data1[i:i+win_size]) < 0.1:
            return i
    return -moc_start

def get_csv_file_paths(parent_folder):
    """
    Traverse the given parent folder and return a list of sublists.
    Each sublist contains paths to CSV files in a subfolder.

    Parameters:
        parent_folder (str): The path to the parent folder.

    Returns:
        list: A list of sublists, each containing paths to CSV files in a subfolder.
    """
    all_csv_paths = []

    # Iterate over subdirectories in the parent folder
    for root, dirs, files in os.walk(parent_folder):
        # Filter out CSV files in the current directory
        csv_files = [os.path.join(root, file) for file in files if file.endswith('.csv')]

        # Only add sublists for directories containing CSV files
        if csv_files:
            all_csv_paths.append(csv_files)

    return all_csv_paths
def sum_dataframes(df1, df2):
    """
    Takes in two data frames (df1, df2) and returns a data frame (df3)
    where each element in df3 is the sum of the corresponding elements in df1 and df2.

    Parameters:
        df1 (pd.DataFrame): The first data frame.
        df2 (pd.DataFrame): The second data frame.

    Returns:
        pd.DataFrame: A data frame where each element is the sum of the corresponding elements in df1 and df2.
    """
    # Ensure the two data frames have the same shape
    if df1.shape != df2.shape:
        raise ValueError("The two data frames must have the same shape.")
    # Trials = [f"Trial_{i + 1}" for i in range(20)]
    # Element-wise addition
    df3 = df1 + df2
    return df3
def dataframe_to_filtered_sublists(df):
    """
    Convert a DataFrame into a list of sublists where each sublist corresponds to
    the values of each row, excluding N/A data and strings.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        list: A list of sublists containing numerical values for each row.
    """
    Trials = [f"Trial_{i + 1}" for i in range(20)]
    sublists = []
    for _, row in df[Trials].iterrows():
        # Filter row to include only numerical values and exclude NaN or strings
        filtered_row = [int(value) for value in row if pd.notna(value) and isinstance(value, (int, float))]
        sublists.append(filtered_row)
    return sublists
def reshape_df(df):
    # Reshape the DataFrame
    reshaped_df = df.reset_index().melt(id_vars=["index"],
                                                        var_name="GroupName",
                                                        value_name="values")

    # Rename columns to match desired output
    reshaped_df.rename(columns={"index": "0"}, inplace=True)
    return reshaped_df
def RunTTest(CollectedData):
    for i in range(len(CollectedData.keys())):
        for j in range(i + 1):
            if i != j:
                print(type(CollectedData[list(CollectedData.keys())[i]]))
                data1 = np.asarray(CollectedData[list(CollectedData.keys())[i]])
                data1 = data1[~np.isnan(CollectedData[list(CollectedData.keys())[i]])]
                data2 = np.asarray(CollectedData[list(CollectedData.keys())[j]])
                data2 = data2[~np.isnan(CollectedData[list(CollectedData.keys())[j]])]
                RejectNull, p_value, t_stat = perform_t_test(data1, data2)
                print("*" * 20)
                print(RejectNull, p_value, t_stat)
                print(list(CollectedData.keys())[i], list(CollectedData.keys())[j])
def Get_file_path(source_folder):
    file_paths = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".csv"):
                # Get the full path of the input file
                input_file_path = os.path.join(root, file)
                file_paths.append(input_file_path)
                # file_paths.append(input_file_path.split("\\"))
    return file_paths


def rename_files_in_directory(source_folder, target, replacement, modify):
    # Walk through the directory
    for root, _, files in os.walk(source_folder):
        for file in files:
            # Check if the target string is in the file name
            if file.endswith(".pickle"):
                if target in file:
                    old_file_path = os.path.join(root, file)
                    # Replace the target string with the replacement string
                    new_file_name = file.replace(target, replacement)
                    new_file_path = os.path.join(root, new_file_name)
                    print(old_file_path)
                    print(new_file_path)
                    if modify:
                        try:
                            # Rename the file
                            os.rename(old_file_path, new_file_path)
                            print(f"Renamed: {old_file_path} -> {new_file_path}")
                        except Exception as e:
                            print(f"Error renaming {old_file_path}: {e}")
def DetermineFlying(WingAngleData):
    return np.max(WingAngleData[:100]) > 100
source_folder_kine = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data"
source_folder_ang = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\Kir Experiment\WT_Control\2024-11-14\Fly_1\Angles"
bodyparts = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip", "platform-tip",
             "L-platform-tip", "R-platform-tip", "platform-axis" ,
             "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT", "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT",
             "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT", "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT",
             "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT", "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"]
bodyparts = ["L-fBC", "L-mBC", "L-hBC",
             "L-fCT", "L-mCT", "L-hCT",
             "L-fFT", "L-mFT", "L-hFT",
             "L-fTT", "L-mTT", "L-hTT",
             "L-fLT", "L-mLT", "L-hLT",
             "R-fBC", "R-mBC", "R-hBC",
             "R-fCT", "R-mCT", "R-hCT",
             "R-fFT", "R-mFT", "R-hFT",
             "R-fTT", "R-mTT", "R-hTT",
             "R-fLT", "R-mLT", "R-hLT"]

Angles = [["R-fBC", "R-fCT", "R-fFT"],
          ["R-mBC", "R-mCT", "R-mFT"],
          ["R-hBC", "R-hCT", "R-hFT"],
          ["L-fBC", "L-fCT", "L-fFT"],
          ["L-mBC", "L-mCT", "L-mFT"],
          ["L-hBC", "L-hCT", "L-hFT"],

          ["R-fCT", "R-fFT", "R-fTT"],
          ["R-mCT", "R-mFT", "R-mTT"],
          ["R-hCT", "R-hFT", "R-hTT"],
          ["L-fCT", "L-fFT", "L-fTT"],
          ["L-mCT", "L-mFT", "L-mTT"],
          ["L-hCT", "L-hFT", "L-hTT"],

          ["R-fFT", "R-fTT", "R-fLT"],
          ["R-mFT", "R-mTT", "R-mLT"],
          ["R-hFT", "R-hTT", "R-hLT"],
          ["L-fFT", "L-fTT", "L-fLT"],
          ["L-mFT", "L-mTT", "L-mLT"],
          ["L-hFT", "L-hTT", "L-hLT"]]

Angles = [["L-fBC", "L-fCT", "L-fFT"],
          ["L-mBC", "L-mCT", "L-mFT"],
          ["L-hBC", "L-hCT", "L-hFT"]]
Angles = [["L-wing", "L-wing-hinge", "R-wing-hinge"],
          ["R-wing", "R-wing-hinge", "L-wing-hinge"]]
wing_angles = ["LeftWingAngle", "RightWingAngle"]
skeletons = [["R-fFT", "platform-axis"], ["R-mFT", "platform-axis"], ["R-hFT", "platform-axis"],
             ["L-fFT", "platform-axis"], ["L-mFT", "platform-axis"], ["L-hFT", "platform-axis"],
             ["R-fFT", "L-platform-tip"], ["R-mFT", "L-platform-tip"], ["R-hFT", "L-platform-tip"],
             ["L-fFT", "L-platform-tip"], ["L-mFT", "L-platform-tip"], ["L-hFT", "L-platform-tip"],
             ["R-fFT", "R-platform-tip"], ["R-mFT", "R-platform-tip"], ["R-hFT", "R-platform-tip"],
             ["L-fFT", "R-platform-tip"], ["L-mFT", "R-platform-tip"], ["L-hFT", "R-platform-tip"],
             ["R-fFT", "platform-tip"], ["R-mFT", "platform-tip"], ["R-hFT", "platform-tip"],
             ["L-fFT", "platform-tip"], ["L-mFT", "platform-tip"], ["L-hFT", "platform-tip"]]

skeletons = [["R-fTT", "platform-axis"], ["R-mTT", "platform-axis"], ["R-hTT", "platform-axis"],
             ["L-fTT", "platform-axis"], ["L-mTT", "platform-axis"], ["L-hTT", "platform-axis"],
             ["R-fTT", "L-platform-tip"], ["R-mTT", "L-platform-tip"], ["R-hTT", "L-platform-tip"],
             ["L-fTT", "L-platform-tip"], ["L-mTT", "L-platform-tip"], ["L-hTT", "L-platform-tip"],
             ["R-fTT", "R-platform-tip"], ["R-mTT", "R-platform-tip"], ["R-hTT", "R-platform-tip"],
             ["L-fTT", "R-platform-tip"], ["L-mTT", "R-platform-tip"], ["L-hTT", "R-platform-tip"],
             ["R-fTT", "platform-tip"], ["R-mTT", "platform-tip"], ["R-hTT", "platform-tip"],
             ["L-fTT", "platform-tip"], ["L-mTT", "platform-tip"], ["L-hTT", "platform-tip"]]

"""skeletons = [["R-fLT", "platform-axis"], ["R-mLT", "platform-axis"], ["R-hLT", "platform-axis"],
             ["L-fLT", "platform-axis"], ["L-mLT", "platform-axis"], ["L-hLT", "platform-axis"],
             ["R-fLT", "L-platform-tip"], ["R-mLT", "L-platform-tip"], ["R-hLT", "L-platform-tip"],
             ["L-fLT", "L-platform-tip"], ["L-mLT", "L-platform-tip"], ["L-hLT", "L-platform-tip"],
             ["R-fLT", "R-platform-tip"], ["R-mLT", "R-platform-tip"], ["R-hLT", "R-platform-tip"],
             ["L-fLT", "R-platform-tip"], ["L-mLT", "R-platform-tip"], ["L-hLT", "R-platform-tip"],
             ["R-fLT", "platform-tip"], ["R-mLT", "platform-tip"], ["R-hLT", "platform-tip"],
             ["L-fLT", "platform-tip"], ["L-mLT", "platform-tip"], ["L-hLT", "platform-tip"]]"""


skeletons = [["L-fTT", "L-platform-tip"], ["L-mTT", "L-platform-tip"], ["L-hTT", "L-platform-tip"]]
KeyPoints = ["L-fFT", "L-fTT", "L-fLT"]
Average_distances_to_tip = ["L-fTT", "L-mTT", "L-hTT"]



kine_data_paths = []
for root, dirs, files in os.walk(source_folder_kine):
    for file in files:
        if file.endswith(".csv"):
            input_file_path = os.path.join(root, file)
            kine_data_paths.append(input_file_path)
ang_data_path = []
for root, dirs, files in os.walk(source_folder_ang):
    for file in files:
        if file.endswith(".csv"):
            input_file_path = os.path.join(root, file)
            ang_data_path.append(input_file_path)

Combined_velocity_data = dict()
Combined_kine_data = []
Combined_kine_data_deriva = []
Combined_ang_data = []
Combined_ang_data_deriva = []
Combined_data_for_display = []
Combined_data_for_display_deriva = []
Combined_wing_ang_data = dict()

Combined_wing_ang_data["LeftWingAngle"] = []
Combined_wing_ang_data["RightWingAngle"] = []
Combined_wing_ang_data["LeftWingAngle_deriva"] = []
Combined_wing_ang_data["RightWingAngle_deriva"] = []
metric_angles = []
metric_segments = []
for bp in bodyparts:
    Combined_velocity_data[bp] = []
for sk in skeletons:
    metric_segments.append(f"{sk[0]}_{sk[1]}")
for ag in Angles:
    metric_angles.append(f"{ag[1]}")
fps = 200
moc_start = 20
analysis_end = 200
fly_num = 9
metrics = None
Combined_data = None
Combined_derivative_data = None
angles = False
segments = True
datatype = ""
mk = ""
trial_num = 20
figsize = (5, 15)
latency_data = dataframe_to_filtered_sublists(pd.read_excel(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data\Landing_latency.xlsx"))
moc_data = dataframe_to_filtered_sublists(pd.read_excel(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data\Moment_of_contact.xlsx"))
mol_data = dataframe_to_filtered_sublists(pd.read_excel(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data\Moment_of_landing.xlsx"))
collected_data_path = get_csv_file_paths(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Kinematic_data")

os.chdir(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Agrawal_Lab\Graph")
moc_to_mv = []
moc_to_ms = []
ms_to_mol = []
total_trials = 0

# angles_paths = Get_file_path(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\angles")
# print(angles_paths)
angle_data_paths = Get_file_path(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\angles")
groups = ["5sInterval", "10sInterval", "30sInterval"]
angles_data_grouped = dict()
for g in groups:
    angles_data_grouped[g] = [d for d in angle_data_paths if g in d]
Flying = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\angles\2025-01-24-11-47-29.46_FlyingPosture_T2_TTa_5sInterval_Fly_5_Trial_1_.csv")
NotFlying = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\angles\2025-01-24-11-49-01.54_FlyingPosture_T2_TTa_5sInterval_Fly_5_Trial_7_.csv")


"""
for f in range(fly_num):
    Combined_kine_data.append([])
    Combined_kine_data_deriva.append([])
    Combined_kine_data[f] = dict()
    Combined_kine_data_deriva[f] = dict()

    Combined_data_for_display.append([])
    Combined_data_for_display[f] = dict()
    Combined_data_for_display_deriva.append([])
    Combined_data_for_display_deriva[f] = dict()

    Combined_ang_data.append([])
    Combined_ang_data_deriva.append([])
    Combined_ang_data[f] = dict()
    Combined_ang_data_deriva[f] = dict()

    for sk in skeletons:
        Combined_kine_data[f][f"{sk[0]}_{sk[1]}"] = []
        Combined_kine_data_deriva[f][f"{sk[0]}_{sk[1]}"] = []
        Combined_data_for_display[f][f"{sk[0]}_{sk[1]}"] = []
        Combined_data_for_display_deriva[f][f"{sk[0]}_{sk[1]}"] = []

    for ag in Angles:
        Combined_ang_data[f][f"{ag[1]}"] = []
        Combined_ang_data_deriva[f][f"{ag[1]}"] = []

    for t in range(len(collected_data_path[f])):
        total_trials += 1
        T2TTa_kine_data = pd.read_csv(collected_data_path[f][t])
        print(f"Reading data Fly: {f + 1}, Trial: {t + 1}")
        T2TTa_kine_data = T2TTa_kine_data[moc_data[f][t] - moc_start:moc_data[f][t] + analysis_end]
        T2TTa_kine_data = T2TTa_kine_data.reset_index(drop=True)

        Collected_segment_lengths_T2 = Calculate_segment_length(T2TTa_kine_data, skeletons)
        Collected_angle_T2 = Calculate_joint_angle(T2TTa_kine_data, Angles)
        for sk in skeletons:
            Combined_kine_data_deriva[f][f"{sk[0]}_{sk[1]}"].append(Calculate_derivative(normalize_list(
                Collected_segment_lengths_T2[f"{sk[0]}_{sk[1]}"][moc_start:moc_start + latency_data[f][t]])))

            Combined_kine_data[f][f"{sk[0]}_{sk[1]}"].append(normalize_list(
                Collected_segment_lengths_T2[f"{sk[0]}_{sk[1]}"][moc_start:moc_start + latency_data[f][t]]))

            Combined_data_for_display[f][f"{sk[0]}_{sk[1]}"].append(normalize_list(
                Collected_segment_lengths_T2[f"{sk[0]}_{sk[1]}"]))

            Combined_data_for_display_deriva[f][f"{sk[0]}_{sk[1]}"].append(Calculate_derivative(normalize_list(
                Collected_segment_lengths_T2[f"{sk[0]}_{sk[1]}"])))

        for ag in Angles:
            Combined_ang_data[f][f"{ag[1]}"].append(normalize_list(Collected_angle_T2[f"{ag[1]}"]))
            Combined_ang_data_deriva[f][f"{ag[1]}"].append(Calculate_derivative(normalize_list(Collected_angle_T2[f"{ag[1]}"])))
SingleFly_plot = False
SingleFly_metric = "L-mTT_L-platform-tip"
if SingleFly_plot:
    for t in range(len(Combined_kine_data[0][SingleFly_metric])):
        plt.figure(figsize=(15, 10), dpi=80)
        x = [x / fps for x in np.arange(len(Combined_data_for_display[0][SingleFly_metric][t][:120]))]
        sns.lineplot(x=x, y=Combined_data_for_display[0][SingleFly_metric][t][:120], color="black", linewidth=4)
        x = [x / fps for x in np.arange(len(Combined_data_for_display_deriva[0][SingleFly_metric][t][:120]))]
        sns.lineplot(x=x, y=Combined_data_for_display_deriva[0][SingleFly_metric][t][:120], color="lightgray", linewidth=4)
        plt.axvline(moc_start/fps, color="black", linestyle="dashed", linewidth=3)

        mst = Determine_movement_start(Combined_kine_data_deriva[0][SingleFly_metric][t])

        moc_to_mv.append(mst - moc_start)
        msp = Determine_movement_stop(Combined_kine_data_deriva[0][SingleFly_metric][t][mst:],
                                      Combined_kine_data[0][SingleFly_metric][t][mst:])
        moc_to_ms.append(msp + mst - moc_start)
        ms_to_mol.append(latency_data[0][t] - (msp + mst))

        plt.axvline((mst + moc_start) / fps, color="blue", linestyle="dashed", linewidth=3)
        if msp > 0:
            plt.axvline((msp + mst + moc_start) / fps, color="red", linestyle="dashed", linewidth=3)
        plt.axvline((latency_data[0][t] + moc_start) / fps, color="green", linestyle="dashed", linewidth=3)
        plt.ylabel("Normalized distance (T2 Ti/Ta to platform tip)", fontsize=30)
        # plt.xlim(-0.1, 1)
        plt.ylim(-0.2, 1.2)
        # Make the tick marks thicker
        plt.tick_params(axis='both', which='major', width=5, length=10)
        ax = plt.gca()
        for spine in ax.spines.values():
            spine.set_linewidth(5)
        # Despine the figure
        sns.despine(trim=True)
        plt.yticks(fontsize=30)
        plt.yticks(ticks=[0, 0.5, 1])
        plt.xticks(ticks=[0, 0.1, 0.6, 1.1], fontsize=30)
        plt.savefig("SingleTrialTrace.pdf")
        plt.show()
if angles:
    metrics = metric_angles
    Combined_data = Combined_ang_data
    Combined_derivative_data = Combined_ang_data_deriva
    datatype = "angles"
    mk = "D"
if segments:
    metrics = metric_segments
    Combined_data = Combined_kine_data
    Combined_derivative_data = Combined_kine_data_deriva
    datatype = "segments"
    mk = "o"

Combined_moc_to_mv = dict()
Combined_moc_to_ms = dict()
Combined_ms_to_mol = dict()
Combined_mv_to_mol = dict()
Combined_mol = []
Average_moc_to_mv = dict()
Average_moc_to_ms = dict()
Average_mol = []
for m, metric in enumerate(metrics):
    Combined_moc_to_mv[metric] = []
    Combined_moc_to_ms[metric] = []
    Combined_ms_to_mol[metric] = []
    Combined_mv_to_mol[metric] = []
    Average_moc_to_ms[metric] = []
    Average_moc_to_mv[metric] = []
    for f in range(fly_num):
        fly_moc_mv_data = []
        fly_moc_ms_data = []
        for t, (k, kd) in enumerate(zip(Combined_data[f][metric], Combined_derivative_data[f][metric])):
            mst = Determine_movement_start(kd)
            if mst >= latency_data[f][t] or mst < 0:
                Combined_moc_to_mv[metric].append(np.nan)
                Combined_moc_to_ms[metric].append(np.nan)
                Combined_mv_to_mol[metric].append(np.nan)
                Combined_ms_to_mol[metric].append(np.nan)
            else:
                fly_moc_mv_data.append(mst / fps)
                Combined_moc_to_mv[metric].append(mst / fps)
                Combined_mv_to_mol[metric].append((latency_data[f][t] - mst) / fps)
                Combined_mol.append(latency_data[f][t] / fps)
                msp = Determine_movement_stop(kd[mst:], k[mst:])
                if (msp + mst) >= latency_data[f][t] or msp < 0:
                    Combined_moc_to_ms[metric].append(np.nan)
                    Combined_ms_to_mol[metric].append(np.nan)
                else:
                    # print(f, t, (mst - moc_start) + msp + (latency_data[f][t] - (msp + mst)) + analysis_end - latency_data[f][t])
                    if latency_data[f][t] - (msp + mst) < 1:
                        Combined_ms_to_mol[metric].append(np.nan)
                        Combined_moc_to_ms[metric].append(np.nan)
                    else:
                        fly_moc_ms_data.append((msp + mst)/fps)
                        Combined_ms_to_mol[metric].append((latency_data[f][t] - (msp + mst)) / fps)
                        Combined_moc_to_ms[metric].append((msp + mst)/fps)
        if m == 0:
            Average_mol.append(np.mean(latency_data[f]) / fps)
        Average_moc_to_mv[metric].append(np.mean(fly_moc_mv_data))
        Average_moc_to_ms[metric].append(np.mean(fly_moc_ms_data))

Plotting_Choice = dict()
Plotting_Choice["Collected_moc_to_mvs"] = False
Plotting_Choice["Collected_moc_to_msp"] = True
Plotting_Choice["Collected_msp_to_mol"] = False
Plotting_Choice["Collected_mvs_to_mol"] = False
Plotting_Choice["Average_moc_to_mvs"] = False
Plotting_Choice["Average_moc_to_ms"] = False
Plotting_Choice["Heatmap"] = False
Temp = Combined_mol
if Plotting_Choice["Average_moc_to_ms"]:
    Average_moc_to_ms["Llatency"] = Average_mol
    RunTTest(Average_moc_to_ms)
    Average_moc_to_ms = pd.DataFrame(Average_moc_to_ms)
    Average_moc_to_ms = reshape_df(Average_moc_to_ms)
    Average_mol = pd.DataFrame({
        "GroupName": ["Llatency"] * len(Average_mol),
        "values": Average_mol
    })

    Combined_data = pd.concat([Average_moc_to_ms, Average_mol], ignore_index=True)

    group_stat = Combined_data.groupby('GroupName')['values'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    # Display the reshaped DataFrame
    plt.figure(figsize=(20, 15), dpi=80)
    sns.pointplot(x='GroupName', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2)
    plt.errorbar(x=group_stat['GroupName'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10)
    sns.stripplot(x="GroupName", y="values", data=Combined_data, size=25, alpha=0.4, marker=">")
    plt.ylabel("Movement start latency (s)", fontsize=30)
    plt.ylim(-0.2, 1.2)
    # Make the tick marks thicker
    plt.tick_params(axis='both', which='major', width=5, length=10)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(5)
    # Despine the figure
    sns.despine(trim=True)
    plt.yticks(fontsize=30)
    plt.yticks(ticks=[0, 0.5, 1])
    plt.xticks(fontsize=30)
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(f"Mean movement stop latency {datatype}.pdf")
    plt.show()
if Plotting_Choice["Average_moc_to_mvs"]:
    Average_moc_to_mv["Llatency"] = Average_mol
    RunTTest(Average_moc_to_mv)
    Average_moc_to_mv = pd.DataFrame(Average_moc_to_mv)
    Average_moc_to_mv = reshape_df(Average_moc_to_mv)
    print(len(Average_mol))
    Average_mol = pd.DataFrame({
        "GroupName": ["Llatency"] * len(Average_mol),
        "values": Average_mol
    })
    Combined_data = pd.concat([Average_moc_to_mv, Average_mol], ignore_index=True)

    group_stat = Combined_data.groupby('GroupName')['values'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    # Display the reshaped DataFrame
    plt.figure(figsize=(20, 15), dpi=80)
    sns.pointplot(x='GroupName', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2)
    plt.errorbar(x=group_stat['GroupName'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10)
    sns.stripplot(x="GroupName", y="values", data=Combined_data, size=25, alpha=0.4, marker=">")
    plt.ylabel("Movement start latency (s)", fontsize=30)
    plt.ylim(-0.2, 1.2)
    # Make the tick marks thicker
    plt.tick_params(axis='both', which='major', width=5, length=10)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(5)
    # Despine the figure
    sns.despine(trim=True)
    plt.yticks(fontsize=30)
    plt.yticks(ticks=[0, 0.5, 1])
    plt.xticks(fontsize=30)
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(f"Mean movement start latency {datatype}.pdf")
    plt.show()
if Plotting_Choice["Collected_moc_to_mvs"]:
    Combined_moc_to_mv["Llatency"] = Temp
    RunTTest(Combined_moc_to_mv)
    Combined_moc_to_mv = pd.DataFrame(Combined_moc_to_mv)
    Combined_moc_to_mv = reshape_df(Combined_moc_to_mv)
    Combined_mol = pd.DataFrame({
        "GroupName": ["Llatency"] * len(Temp),
        "values": Temp
    })
    Combined_data = pd.concat([Combined_moc_to_mv, Combined_mol], ignore_index=True)

    group_stat = Combined_data.groupby('GroupName')['values'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    # Display the reshaped DataFrame
    plt.figure(figsize=(20, 15), dpi=80)
    sns.pointplot(x='GroupName', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2)
    plt.errorbar(x=group_stat['GroupName'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10)
    sns.stripplot(x="GroupName", y="values", data=Combined_data, size=25, alpha=0.4, marker=mk)
    plt.ylabel("Movement start latency (s)", fontsize=30)
    plt.ylim(-0.2, 1.2)
    # Make the tick marks thicker
    plt.tick_params(axis='both', which='major', width=5, length=10)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(5)
    # Despine the figure
    sns.despine(trim=True)
    plt.yticks(fontsize=30)
    plt.yticks(ticks=[0, 0.5, 1])
    plt.xticks(fontsize=30)
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(f"movement start latency {datatype}.pdf")
    plt.show()
if Plotting_Choice["Collected_moc_to_msp"]:
    Combined_moc_to_ms["Llatency"] = Temp
    RunTTest(Combined_moc_to_ms)
    Combined_moc_to_ms = pd.DataFrame(Combined_moc_to_ms)
    Combined_moc_to_ms = reshape_df(Combined_moc_to_ms)
    Combined_mol = pd.DataFrame({
        "GroupName": ["Llatency"] * len(Temp),
        "values": Temp
    })
    Combined_data = pd.concat([Combined_moc_to_ms, Combined_mol], ignore_index=True)

    group_stat = Combined_data.groupby('GroupName')['values'].agg(['mean', 'std', 'count']).reset_index()
    group_stat['ci'] = 1.96 * group_stat['std'] / np.sqrt(group_stat['count'])

    # Display the reshaped DataFrame
    plt.figure(figsize=(20, 15), dpi=80)
    sns.pointplot(x='GroupName', y='mean', data=group_stat, color='black', linestyles=" ", markers="s", errorbar=None, scale=2)
    plt.errorbar(x=group_stat['GroupName'], y=group_stat['mean'], yerr=group_stat['ci'], fmt="none", color='black', capsize=10)
    sns.stripplot(x="GroupName", y="values", data=Combined_data, size=25, alpha=0.4, marker=mk)
    plt.ylabel("Movement stop latency (s)", fontsize=30)
    plt.ylim(-0.2, 1.2)
    # Make the tick marks thicker
    plt.tick_params(axis='both', which='major', width=5, length=10)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(5)
    # Despine the figure
    sns.despine(trim=True)
    plt.yticks(fontsize=30)
    plt.yticks(ticks=[0, 0.5, 1])
    plt.xticks(fontsize=30)
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(f"Movement stop latency {datatype}.pdf")
    plt.show()
if Plotting_Choice["Collected_msp_to_mol"]:
    Combined_ms_to_mol = pd.DataFrame(Combined_ms_to_mol)
    Combined_ms_to_mol = reshape_df(Combined_ms_to_mol)
    Combined_mol = pd.DataFrame({
        "GroupName": ["Llatency"] * len(Temp),
        "values": Temp
    })
    Combined_data = pd.concat([Combined_ms_to_mol, Combined_mol], ignore_index=True)

    # Display the reshaped DataFrame
    plt.figure(figsize=(20, 15), dpi=80)
    sns.stripplot(x="GroupName", y="values", data=Combined_mol, size=25, alpha=0.4, marker=mk)
    plt.ylabel("Wing stop latency (s)", fontsize=30)
    plt.ylim(-0.2, 1.2)
    # Make the tick marks thicker
    plt.tick_params(axis='both', which='major', width=5, length=10)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(5)
    # Despine the figure
    sns.despine(trim=True)
    plt.yticks(fontsize=30)
    plt.yticks(ticks=[0, 0.5, 1])
    plt.xticks(fontsize=30)
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(f"Wing stop latency {datatype}.pdf")
    plt.show()
if Plotting_Choice["Collected_mvs_to_mol"]:
    Combined_mv_to_mol = pd.DataFrame(Combined_mv_to_mol)
    Combined_mv_to_mol = reshape_df(Combined_mv_to_mol)
    Combined_mol = pd.DataFrame({
        "GroupName": ["Llatency"] * len(Temp),
        "values": Temp
    })
    Combined_data = pd.concat([Combined_mv_to_mol, Combined_mol], ignore_index=True)

    # Display the reshaped DataFrame
    plt.figure(figsize=(20, 15), dpi=80)
    sns.stripplot(x="GroupName", y="values", data=Combined_data, size=25, alpha=0.4, marker=mk)
    plt.ylabel("Movement start to Wing stop latency (s)", fontsize=30)
    plt.ylim(-0.2, 1.2)
    # Make the tick marks thicker
    plt.tick_params(axis='both', which='major', width=5, length=10)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_linewidth(5)
    # Despine the figure
    sns.despine(trim=True)
    plt.yticks(fontsize=30)
    plt.yticks(ticks=[0, 0.5, 1])
    plt.xticks(fontsize=30)
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(f"Movement start to Wing stop latency {datatype}.pdf")
    plt.show()
if Plotting_Choice["Heatmap"]:
    fig, ax1 = plt.subplots(nrows=len(metrics), ncols=1, figsize=(15, 20))
    KinwDataDeriv = dict()
    KineData = dict()
    for m, metric in enumerate(metrics):
        Data_to_plot = []
        KinwDataDeriv[metric] = []
        KineData[metric] = []
        for f in range(fly_num):
            for t, (k, kd) in enumerate(zip(Combined_data[f][metric], Combined_derivative_data[f][metric])):
                Data_to_plot.append(k[:120])
                KineData[metric].append(k)
                KinwDataDeriv[metric].append(kd)
        sns.heatmap(Data_to_plot, cmap="plasma", cbar=True, vmin=0, vmax=1, ax=ax1[m])
        ax1[m].tick_params(axis='both', which='major', width=3, length=5)
        ax1[m].set_yticks([1, len(Data_to_plot[:120])])
        ax1[m].set_xticks([0, 20, 120])
        comp = metric.split("_")
        if datatype != "angles":
            ax1[m].set_title(f'Normalized distance trace from {comp[0]} to {comp[1]}')
        else:
            ax1[m].set_title(f'Normalized angle trace from {metric}')
    plt.tight_layout()
    plt.savefig(f"RawDataHeatMap{datatype}.pdf")
    plt.show()

    fig, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(15, 20), gridspec_kw={'height_ratios': [2, 1]})
    ax1[0].set_ylabel("Normalized distance", fontsize=30)
    ax1[1].set_ylabel("Normalized Ti/Ta speed", fontsize=30)
    ax1[1].set_xlabel("Time (s)")
    ax1[0].tick_params(axis='both', which='major', width=5, length=10)
    ax1[1].tick_params(axis='both', which='major', width=5, length=10)
    for ax in ax1:  # Loop through both axes
        for spine in ax.spines.values():
            spine.set_linewidth(5)
    # Despine the figure
    sns.despine()
    ax1[0].set_yticks([0, 0.5, 1])  # Set y-ticks
    ax1[0].set_xticks([0, 0.1, 0.6, 1.1])  # Set x-ticks
    ax1[0].tick_params(axis='both', labelsize=30)  # Set font size for both axes

    ax1[1].set_yticks([0, 0.15])  # Set y-ticks
    ax1[0].set_xticks([0, 0.1, 0.6, 1.1])   # Set x-ticks
    ax1[1].tick_params(axis='both', labelsize=30)
    ax1[0].set_ylim(-0.2, 1.1)
    ax1[1].set_ylim(-0.05, 0.2)
    avg, semin, semax = get_min_and_max(KineData["L-fTT_L-platform-tip"])
    x = [x / fps for x in np.arange(len(avg))]
    sns.lineplot(x=x, y=avg, color="navy", linestyle="solid", ax=ax1[0])
    ax1[0].fill_between(x, semin, semax, color="navy", alpha=0.2)
    avg, semin, semax = get_min_and_max(KinwDataDeriv["L-fTT_L-platform-tip"])
    x = [x / fps for x in np.arange(len(avg))]
    sns.lineplot(x=x, y=avg, color="blue", linestyle="solid", ax=ax1[1])
    ax1[1].fill_between(x, semin, semax, color="blue", alpha=0.2)


    avg, semin, semax = get_min_and_max(KineData["L-mTT_L-platform-tip"])
    x = [x / fps for x in np.arange(len(avg))]
    sns.lineplot(x=x, y=avg, color="orange", linestyle="solid", ax=ax1[0])
    ax1[0].fill_between(x, semin, semax, color="orange", alpha=0.2)
    avg, semin, semax = get_min_and_max(KinwDataDeriv["L-mTT_L-platform-tip"])
    x = [x / fps for x in np.arange(len(avg))]
    sns.lineplot(x=x, y=avg, color="gold", linestyle="solid", ax=ax1[1])
    ax1[1].fill_between(x, semin, semax, color="gold", alpha=0.2)


    avg, semin, semax = get_min_and_max(KineData["L-hTT_L-platform-tip"])
    x = [x / fps for x in np.arange(len(avg))]
    sns.lineplot(x=x, y=avg, color="brown", linestyle="solid", ax=ax1[0])
    ax1[0].fill_between(x, semin, semax, color="brown", alpha=0.2)
    avg, semin, semax = get_min_and_max(KinwDataDeriv["L-hTT_L-platform-tip"])
    x = [x / fps for x in np.arange(len(avg))]
    sns.lineplot(x=x, y=avg, color="red", linestyle="solid", ax=ax1[1])
    ax1[1].fill_between(x, semin, semax, color="red", alpha=0.2)
    plt.tight_layout()

    sns.despine(trim=True)
    plt.savefig(f"TraceOverlap.pdf")


    plt.show()

"""

