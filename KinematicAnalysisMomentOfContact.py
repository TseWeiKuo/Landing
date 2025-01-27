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
import matplotlib.patches as mpatches
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
"""
These functions are responsible for preprocessing of angle data and 3D pose data
"""
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
    for p_x, p_y, p_z, C_x, C_y, C_z in zip(threeD_data[f"{keypoint1}_x"], threeD_data[f"{keypoint1}_y"],
                                            threeD_data[f"{keypoint1}_z"], threeD_data[f"{keypoint2}_x"],
                                            threeD_data[f"{keypoint2}_y"], threeD_data[f"{keypoint2}_z"]):
        platform_coxa_distance.append(np.sqrt((p_x - C_x) ** 2 + (p_y - C_y) ** 2 + (p_z - C_z) ** 2))
    # sns.lineplot(x=range(len(threeD_data)), y=platform_coxa_distance)
    return platform_coxa_distance
"""
These functions are responsible for detecting various characteristic of the angle and 3D data
"""
def detect_moment_of_contact(data, threshold):
    window = 10
    for i in range(0, len(data), window):
        if np.average(data[i:i+window]) <= threshold:
            return i
    return 0
def determine_platform_threshold(baseline, slope, intercept):
    return slope * baseline + intercept
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
def Create_DataSets_MetaData():
    global Joints_index
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
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Pose_3D_Folder"] = r"C:\Users\agrawal-admin\Desktop\Anipose Predicted Data\Testing_Network_for_wing_angle-05-08-2024\Control_T2_CTF-2024-05-10\pose-3d"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Prediction_output_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\KinematicsAnalysis.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Manual_LL_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\CorrectedLabeled_data.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Manual_MOC_csv_file"] = r"C:\Users\agrawal-admin\Desktop\Platform_moc.xlsx"
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Analysis_Start_time"] = 200
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Analysis_End_time"] = 800
    DataSetsMetaData["Control_T2_CTF_Experiment"]["Actual_Video_time"] = 250
    DataSetsMetaData["Control_T2_CTF_Experiment"]["FPS"] = 250

    body_parts = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "platform", "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
     "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT", "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT", "R-fBC", "R-fCT",
     "R-fFT", "R-fTT", "R-fLT", "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT", "R-hBC", "R-hCT", "R-hFT", "R-hTT",
     "R-hLT"]
    for p in range(len(body_parts)):
        Joints_index[body_parts[p]] = p

    return DataSetsMetaData
def Read_Data(file_path):
    Trial_num = 20
    Trial_num_list = ["Trial_" + str(i + 1) for i in range(Trial_num)]
    Manual_data = pd.read_excel(file_path)[Trial_num_list]
    return Manual_data
def ExtractPoseLabelFromH5(group):
    global Data
    Total_frames_num = 1000
    for i in list(group.keys()):
        try:
            subgroup = group[i]
            if isinstance(subgroup, h5py.Group):
                ExtractPoseLabelFromH5(subgroup)
            elif isinstance(subgroup, h5py.Dataset):
                if subgroup.shape[0] == Total_frames_num:
                    for frame in subgroup:
                        frame_data = []
                        prev_data_ind = 0
                        for data_ind in range(3, len(frame[1]) + 1, 3):
                            frame_data.append(list(frame[1][prev_data_ind:data_ind]))
                            prev_data_ind = data_ind
                        Data.append(frame_data)
        except Exception as e:
            print(f"Error accessing {i}: {str(e)}")
def ConvertH5ToCoords(pose_data, joint_ind):
    x = []
    y = []
    coords = [c[joint_ind] for c in pose_data]
    for c in coords:
        if c[2] > 0.8:
            x.append(c[0])
            y.append(c[1])
        else:
            x.append(np.nan)
            y.append(np.nan)
    return x, y
def Calculate_distance(x1, y1, x2, y2):
    distance = []
    # print(len(x1), len(y1), len(x2), len(y2))
    for i in range(len(x1)):
        distance.append(np.sqrt((x1[i] - x2) ** 2 + (y1[i] - y2) ** 2))
    return distance
def find_derivative(y):
    return np.gradient(y, 1)
def exponential_func(x, a, b):
    return a * np.exp(-b * x)
def AdjustOffSet(data):
    end_baseline = np.average([a for a in data[300:] if not np.isnan(a)])
    adjusted_data = []
    for d in data:
        adjusted_data.append(d - end_baseline)
    return adjusted_data
def PlotH5Data(H5_Dir, fly_num, moc_data):
    global Data
    global platform_distance_at_moc
    global moc_error
    global collected_platform_distance_baseline
    global collected_platform_distance_at_moc
    global slopes
    global intercepts
    global Cams_Enable
    avg_trace_cam_data = ExtractH5Data(H5_Dir, fly_num)
    trial_num = 20
    cam_num = 6
    clip_start = 200
    clip_end = 800
    files = os.listdir(H5_Dir)
    fig, axes = plt.subplots(nrows=5, ncols=4, figsize=(20, 16))
    row_ind = 0
    col_ind = 0
    for i in range(trial_num):
        print(f"Trial {i + 1}")
        if i % 5 == 0:
            col_ind += 1
            row_ind = 1
        else:
            row_ind += 1
        axes[row_ind - 1, col_ind - 1].set_title(f"Trial {i + 1} Cam 4")
        axes[row_ind - 1, col_ind - 1].set_ylabel("Pixels")
        axes[row_ind - 1, col_ind - 1].set_xlabel("Second")
        axes[row_ind - 1, col_ind - 1].set_yticks([0, 10, 20, 30, 40])
        axes[row_ind - 1, col_ind - 1].set_ylim(-10, 50)
        collected_cam_data = []
        for j in range(cam_num):
            Data = []
            if Cams_Enable[j]:
                data_to_plot = Calculate_platform_data_from_H5(os.path.join(H5_Dir, files[i * cam_num + j]), clip_start, clip_end)
                # sns.lineplot(avg_trace_cam_data[j], color=Colors[j], linestyle="dashed", ax=axes[row_ind - 1, col_ind - 1])

                # Filter the data if the first 200 frames contain too many nan data points
                if (sum(np.isnan(dtp) for dtp in data_to_plot[:200]) / len(data_to_plot[:200])) < 0.2:

                    # Smooth the data to plot
                    data_to_plot = determine_smooth_amplify_curve(data_to_plot, 1, True)

                    # Calculate the baseline of the data to plot
                    contact_baseline = np.average([a for a in data_to_plot[400:] if not np.isnan(a)])
                    axes[row_ind - 1, col_ind - 1].axhline(contact_baseline, linestyle="dashed", color=Colors[j])

                    # if the baseline is not nan
                    if not np.isnan(contact_baseline):
                        # if the manual data is valid
                        if not (isinstance(moc_data.iloc[fly_num - 1][i], str) or pd.isna(moc_data.iloc[fly_num - 1][i]) or moc_data.iloc[fly_num - 1][i] < 0):
                            # Get the value of platform distance - baseline at manual moc
                            # (The distance between moc distance and baseline)

                            camera_moc_values = data_to_plot[int(moc_data.iloc[fly_num - 1][i]) - clip_start] - contact_baseline
                            moc_value = camera_moc_values

                            # if the moc distance - baseline is valid
                            if not np.isnan(moc_value):
                                predicted_moc = detect_moment_of_contact(data_to_plot, determine_platform_threshold(contact_baseline, slopes_trial[j], intercepts_trial[j]) + contact_baseline)
                                # axes[row_ind - 1, col_ind - 1].axvline(predicted_moc / FPS, color=Colors[j])
                                moc_error[j].append((moc_data.iloc[fly_num - 1][i] - clip_start - predicted_moc) / FPS)
                                # append the moc_value for camera j
                                collected_platform_distance_at_moc[j].append(moc_value)
                                # Append the baseline for camera j
                                collected_platform_distance_baseline[j].append(contact_baseline)

                    # data_to_plot = AdjustOffSet(data_to_plot)
                    collected_cam_data.append(data_to_plot)
                    sns.lineplot(x=[f / FPS for f in range(len(data_to_plot))],y=data_to_plot, color=Colors[j], linestyle="solid", ax=axes[row_ind - 1, col_ind - 1])

        # Transpose the collected data from each camera to take the average
        np_matrix = np.array(collected_cam_data)
        transposed_matrix = np_matrix.T
        average_trace = []
        for frame_data in transposed_matrix:
            average_trace.append(np.average([f for f in frame_data if not np.isnan(f)]))
        average_trace = determine_smooth_amplify_curve(average_trace, 5, True)

        contact_baseline = np.average([a for a in average_trace[400:] if not np.isnan(a)])
        # axes[row_ind - 1, col_ind - 1].axhline(contact_baseline, color="pink")
        # Plot the average trace data
        # sns.lineplot(average_trace, color=Colors[-1], linestyle="solid", ax=axes[row_ind - 1, col_ind - 1])

        # If available, plot the manually determined moc
        if not (isinstance(moc_data.iloc[fly_num - 1][i], str) or pd.isna(moc_data.iloc[fly_num - 1][i]) or moc_data.iloc[fly_num - 1][i] < 0):
            axes[row_ind - 1, col_ind - 1].axvline((moc_data.iloc[fly_num - 1][i] - clip_start) / FPS)
            if not np.isnan(contact_baseline):
                collected_platform_distance_at_moc[6].append(average_trace[int(moc_data.iloc[fly_num - 1][i]) - clip_start] - contact_baseline)
                collected_platform_distance_baseline[6].append(contact_baseline)
                predicted_moc = detect_moment_of_contact(average_trace, determine_platform_threshold(contact_baseline, slopes[6], intercepts[6]) + contact_baseline)
                # axes[row_ind - 1, col_ind - 1].axvline(predicted_moc, color="gray")
                moc_error[6].append((moc_data.iloc[fly_num - 1][i] - clip_start - predicted_moc) / FPS)

    plt.suptitle(f"Fly {fly_num}")
    plt.tight_layout()
    print(f"Processing Fly {fly_num}'s data")
    plt.savefig(f"Fly {fly_num}")
    plt.close()
def Calculate_platform_data_from_H5(file_path, clip_start, clip_end):
    global Data
    Data = []
    group_data = h5py.File(file_path, 'r')
    ExtractPoseLabelFromH5(group_data)
    group_data.close()
    X, Y = ConvertH5ToCoords(Data[clip_start:clip_end], Joints_index["platform"])
    X1, Y1 = ConvertH5ToCoords(Data[clip_start:clip_end], Joints_index["R-mCT"])
    # Calculate the average coordinate of target joint
    average_spot_x = np.average(X1[:20])
    average_spot_y = np.average(Y1[:20])

    # Calculate the distance of the platform to the average coordinate
    distance = Calculate_distance(X, Y, average_spot_x, average_spot_y)

    # Calculate the distance of platform to the average coordinate using only y coordinates
    Y = [y - average_spot_y for y in Y]

    data_to_plot = Y
    data_to_plot = determine_smooth_amplify_curve(data_to_plot, 3, True)
    return data_to_plot
def ExtractH5Data(H5_Dir, fly_num):
    global Data
    global Colors
    global Joints_index
    global Cams_Enable
    clip_start = 200
    clip_end = 800
    vid_num = 120
    fly_num = 0
    trial_num = 20
    cam_num = 6
    axs = None
    file_list = os.listdir(H5_Dir)
    files = os.listdir(H5_Dir)
    Camera_Data_files_path = [[0 for t in range(trial_num)] for _ in range(cam_num)]
    for i in range(trial_num):
        for j in range(cam_num):
            if Cams_Enable[j]:
                Camera_Data_files_path[j][i] = os.path.join(H5_Dir, files[i * cam_num + j])

    Camera_average_trace = [[] for _ in range(cam_num)]
    for i, cam in enumerate(Camera_Data_files_path):
        collected_trace = []
        for j, trial_data_file in enumerate(cam):
            try:
                data_to_plot = Calculate_platform_data_from_H5(trial_data_file, clip_start, clip_end)

                # sns.lineplot([i + j for i in data_to_plot], color='red')
                # Filter the data if the first 200 frames contain too many nan data points
                if (sum(np.isnan(dtp) for dtp in data_to_plot[:300]) / len(data_to_plot[:300])) < 0.2:
                    collected_trace.append(data_to_plot)
            except TypeError as t:
                collected_trace.append([])

        np_matrix = np.array(collected_trace)
        transposed_matrix = np_matrix.T
        average_trace = []
        for frame_data in transposed_matrix:
            average_trace.append(np.average([f for f in frame_data if not np.isnan(f)]))

        Camera_average_trace[i] = average_trace
        # sns.lineplot(average_trace, color="black")
        # plt.show()
        # plt.close()


    return Camera_average_trace
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


Joints_index = dict()
DataSets = Create_DataSets_MetaData()
Analysis_start = DataSets["Control_T2_CTF_Experiment"]["Analysis_Start_time"]
Analysis_end = DataSets["Control_T2_CTF_Experiment"]["Analysis_End_time"]
FPS = 250
Fly_Num = 30
Data = []
platform_distance_at_moc = [[], [], [], [], [], []]
platform_distance_baseline = [[], [], [], [], [], []]
collected_platform_distance_at_moc = [[], [], [], [], [], [], []]
collected_platform_distance_baseline = [[], [], [], [], [], [], []]
Colors = ["blue", "red", "green", "orange", "brown", "black", "pink", "purple", "teal", "olive", "yellow", "gray"]
Analyze_data = True
Do_not_overwrite = True
Cams_Enable = [True, True, True, True, False, False]
moc_error = [[], [], [], [], [], [], []]
slopes = [-0.9259704946696065, -0.9322005032081596, -0.9633232392431816, -0.9118223342476077, 0, 0, -0.6920761411351276]
intercepts = [5.788340141331409, 12.059137484219592, 8.81510132252997, 7.63016269001471, 0, 0, 8.264675123483656]
slopes_trial = [-0.7730693121523116, -0.7275331055682598, -0.7194398352978458, -0.6790996843967286]
intercepts_trial = [5.818946253809424, 11.047558164825553, 8.059210137165543, 7.476001674985365]


moc_data = pd.read_excel(DataSets["Control_T2_CTF_Experiment"]["Manual_MOC_csv_file"])
h5_file_path = r"C:\Users\agrawal-admin\Desktop\Anipose Predicted Data\Testing_Network_for_wing_angle-05-08-2024\Control_T2_CTF-2024-05-10\H5_file"
Collected_correlation_data = dict()
correlation_data_file = ""

if Analyze_data:
    for f in range(Fly_Num):
        PlotH5Data(h5_file_path + f"\Fly{f + 1}", f + 1, moc_data[[f"Trial_{i + 1}" for i in range(20)]])

    if not Do_not_overwrite:
        correlation_data_file = os.path.join(os.getcwd(), "Cams_distance_vs_baseline.csv")
        with open(correlation_data_file, 'w', newline='') as sig_csvfile:
            pass
    col = 0
    for collected_moc, collected_baseline in zip(collected_platform_distance_at_moc, collected_platform_distance_baseline):
        col += 1
        if not Do_not_overwrite:
            Collected_correlation_data[f"Cam{col}_baseline"] = collected_baseline
            Collected_correlation_data[f"Cam{col}_distance"] = collected_moc
            add_column_to_csv(correlation_data_file, f"Cam{col}_baseline", collected_baseline)
            add_column_to_csv(correlation_data_file, f"Cam{col}_distance", collected_moc)
            sns.scatterplot(x=collected_baseline, y=collected_moc, color=Colors[col - 1], alpha=0.5)
            plt.ylabel("Motor distance - baseline (pixels)")
            plt.xlabel("Baseline (pixels)")
            x = np.array(collected_baseline).reshape(-1, 1)
            y = np.array(collected_moc)
            model = LinearRegression()
            try:
                model.fit(x, y)
                slope = model.coef_[0]
                intercept = model.intercept_
                line = (slope * x + intercept).flatten()
                x_flat = x.flatten()
                print(f"Cam {col}: Slope {slope}, Intercept: {intercept}")
                add_column_to_csv(correlation_data_file, f"Cam{col}_slope", [slope])
                add_column_to_csv(correlation_data_file, f"Cam{col}_intercept", [intercept])
                sns.lineplot(x=x_flat, y=line, color='black', label='Best fit line')
            except ValueError as v:
                print(f"Encountered: {v}")
                pass

            plt.savefig(f"{col}")
            plt.close()


# Create an empty list to store all data points and corresponding x-tick positions
data = []
positions = []

# Populate data and positions lists
for i, l in enumerate(moc_error):
    data.extend(l)
    positions.extend([i] * len(l))
add_column_to_csv("Moc_error_comparisons.csv", "Cam 1", moc_error[0])
add_column_to_csv("Moc_error_comparisons.csv", "Cam 2", moc_error[1])
add_column_to_csv("Moc_error_comparisons.csv", "Cam 3", moc_error[2])
add_column_to_csv("Moc_error_comparisons.csv", "Cam 4", moc_error[3])
add_column_to_csv("Moc_error_comparisons.csv", "2D Average", moc_error[6])
# Create the strip plot
sns.stripplot(x=positions, y=data, alpha=0.5)
plt.xticks(range(5), ["Cam 1", "Cam 2", "Cam 3", "Cam 4", "2D Average"])  # Optionally label the x-ticks
plt.xlabel("Camera")
plt.ylabel("Second")
plt.title("Moc prediction error")
plt.savefig("Moc error for each cam")
plt.show()
