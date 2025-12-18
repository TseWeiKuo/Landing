import os
import numpy as np
import pandas as pd
from natsort import natsorted
import warnings
import re
warnings.filterwarnings(action="ignore", category=FutureWarning)

def group_files_by_fly(file_names):
    # Regular expression to extract the relevant parts of the file name
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2})-\d{2}-\d{2}-\d{2}\.\d+.*?_Fly_(\d+)_Trial_(\d+)_")
    # Dictionary to map unique combinations to "Fly_N"
    unique_combinations = {}
    grouped_files = {}

    current_fly_number = 1  # Counter for Fly_N keys
    for file in file_names:
        match = pattern.search(file)
        if match:
            date = match.group(1)
            fly_number = match.group(2)
            trial_number = match.group(3)
            unique_fly_id = (date, fly_number)  # Unique identifier based on date and fly number

            if unique_fly_id not in unique_combinations:
                unique_combinations[unique_fly_id] = current_fly_number
                current_fly_number += 1

            grouped_files[f"F{unique_combinations[unique_fly_id]}T{trial_number}"] = file
    return grouped_files
def Get3D_path(source_folder):
    AllFiles = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".csv"):
                input_file_path = os.path.join(root, file)
                AllFiles.append(input_file_path)

    AllFiles = natsorted(AllFiles)
    grouped_data_path = group_files_by_fly(AllFiles)
    return grouped_data_path

# Individual point's data
class Point:
    def __init__(self, name="point", x=None, y=None, z=None):
        self.name = name
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
# Individual trial's data
class Trial:
    # Initialize each trial's data
    def __init__(self, fly_number=0, trial_number=0, fps=0, total_frames_number=0,
                 landing_latency=0, moc=0, mol=0, group_name="NoName", trial_data_path="NoPath", joints=None):
        # The index of the fly number in manual data
        self.fly_number = fly_number

        # The index of the trial number in manual data
        self.trial_number = trial_number

        # Frame rate of the kinematic data
        self.fps = fps

        # Total number of frames in kinematic data
        self.total_frames_number = total_frames_number

        # Name of the fly group
        self.group_name = group_name

        # Landing latency of this trial
        self.landing_latency = landing_latency

        # Moment of contact of this trial
        self.moc = moc

        # Moment of landing of this trial
        self.mol = mol

        # Average L FT angle of stable flying posture
        self.L_stable_FT_angle = np.nan

        # Average R FT angle of stable flying posture
        self.R_stable_FT_angle = np.nan

        # Individual leg movement start latency
        self.movement_start_latency = np.nan

        # Name of joints data that will be extracted
        self.joints = joints

        # Trial's kinematic data
        self.trial_data = self.read_trial_data(data_path=trial_data_path)

        self.data_path = trial_data_path
    # Read the trial data
    def read_trial_data(self, data_path):
        kine_data = pd.read_csv(data_path)
        data = dict()
        for j in self.joints:
            data[j] = Point(name=j,
                            x=kine_data[f"{j}_x"],
                            y=kine_data[f"{j}_y"],
                            z=kine_data[f"{j}_z"])
        return data
# Fly group's data
class Group:
    # Initialize the group class
    def __init__(self, moc_data_path="NoPath", mol_data_path="NoPath", ll_data_path="NoPath",
                 fly_kinematic_data_path="NoPath", group_name="NoName", joints=None, angles=None, segments=None,
                 total_fly_number=0,  fps=None, trial_num=20, video_duration=7, trials_offset=0):
        # Directory to the kinematic data directory
        self.fly_kinematic_data_path = Get3D_path(fly_kinematic_data_path)

        # Directory to moment of contact file
        self.moc_data_path = moc_data_path
        # Directory to moment of landing file
        self.mol_data_path = mol_data_path
        # Directory to landing latency data file
        # Directory to landing latency data file
        self.ll_data_path = ll_data_path

        # List of joints to extract the kinematic data
        self.joints = joints
        self.angles = angles
        self.segment = segments
        # Total number of fly's data to read
        self.total_fly_number = total_fly_number
        # The name of the fly's group
        self.group_name = group_name

        # Total number of trials to read
        self.trials_index = [f"Trial_{i + 1 + trials_offset}" for i in range(trial_num - trials_offset)]
        self.trial_num = trial_num
        self.trial_offset = trials_offset

        self.landing_trial_index = []
        self.flying_trial_index = []
        self.not_flying_trial_index = []
        self.NA_trial_index = []
        self.good_fly_index = list(range(1, self.total_fly_number + 1))

        # Frame rate of the kinematic data
        self.fps = fps
        # Video duration of the kinematic data
        self.video_duration = video_duration

        # Landing latency data
        self.ll_data = self.read_manual_data(self.ll_data_path)
        # Moment of landing data
        self.mol_data = self.read_manual_data(self.mol_data_path)
        # Moment of contact data
        self.moc_data = self.read_manual_data(self.moc_data_path)

        # Kinematic data
        self.fly_kinematic_data = dict()
        # Predicted data by algorithms
        self.predicted_data = dict()

    # Read the manual data such as moc, mol and latency from the corresponding file.
    def read_manual_data(self, data_path):
        if data_path != "NoPath":
            return pd.read_excel(data_path)[self.trials_index].iloc[:self.total_fly_number]
        else:
            return None
    # Read the kinematic data of landing trial based on the number of fly specified
    def read_landing_trial_data(self):
        for i in range(self.total_fly_number):
            for t in range(self.trial_num - self.trial_offset):
                offset_adjusted_trial = t + 1 + self.trial_offset
                if f"F{i + 1}T{offset_adjusted_trial}" not in self.fly_kinematic_data_path:
                    break
                if not isinstance(self.ll_data.iloc[i][t], str) and not pd.isna(self.ll_data.iloc[i][t]) and not self.ll_data.iloc[i][t] < 0 and not self.ll_data.iloc[i][t] > self.fps[i]:
                    # print(f"F{i + 1}T{offset_adjusted_trial}")
                    self.fly_kinematic_data[f"F{i + 1}T{offset_adjusted_trial}"] = Trial(fly_number=i + 1,
                                                                                         trial_number=offset_adjusted_trial,
                                                                                         fps=self.fps[i],
                                                                                         total_frames_number=self.fps[i] * self.video_duration,
                                                                                         landing_latency=int(self.ll_data.iloc[i][t]),
                                                                                         moc=int(self.moc_data.iloc[i][t]),
                                                                                         mol=int(self.mol_data.iloc[i][t]),
                                                                                         group_name=self.group_name + "-Landing",
                                                                                         trial_data_path=self.fly_kinematic_data_path[f"F{i + 1}T{offset_adjusted_trial}"],
                                                                                         joints=self.joints)
                    self.landing_trial_index.append((i + 1, offset_adjusted_trial))
                    # print(f"Flying trial: Fly {i + 1}, Trial {t + 1}")
    # Read the kinematic data of flying trial based on the number of fly specified
    def read_flying_trial_data(self):
        for i in range(self.total_fly_number):
            for t in range(self.trial_num - self.trial_offset):
                offset_adjusted_trial = t + 1 + self.trial_offset
                if f"F{i + 1}T{offset_adjusted_trial}" not in self.fly_kinematic_data_path:
                    break
                if not isinstance(self.ll_data.iloc[i][t], str) and not pd.isna(self.ll_data.iloc[i][t]) and (self.ll_data.iloc[i][t] == -1 or self.ll_data.iloc[i][t] > self.fps[i]):
                    self.fly_kinematic_data[f"F{i + 1}T{offset_adjusted_trial}"] = Trial(fly_number=i + 1,
                                                                                         trial_number=offset_adjusted_trial,
                                                                                         fps=self.fps[i],
                                                                                         total_frames_number=self.fps[i] * self.video_duration,
                                                                                         landing_latency=int(self.ll_data.iloc[i][t]),
                                                                                         moc=int(self.moc_data.iloc[i][t]),
                                                                                         mol=int(self.mol_data.iloc[i][t]),
                                                                                         group_name=self.group_name + "-Flying",
                                                                                         trial_data_path=self.fly_kinematic_data_path[f"F{i + 1}T{offset_adjusted_trial}"],
                                                                                         joints=self.joints)
                    self.flying_trial_index.append((i + 1, offset_adjusted_trial))
                    # print(f"Flying trial: Fly {i + 1}, Trial {t + 1}")
    # Read the kinematic data of not flying trial based on the number of fly specified
    def read_not_flying_trial_data(self):
        for i in range(self.total_fly_number):
            for t in range(self.trial_num - self.trial_offset):
                offset_adjusted_trial = t + 1 + self.trial_offset
                if f"F{i + 1}T{offset_adjusted_trial}" not in self.fly_kinematic_data_path:
                    break
                if isinstance(self.ll_data.iloc[i][t], str):
                    self.fly_kinematic_data[f"F{i + 1}T{offset_adjusted_trial}"] = Trial(fly_number=i + 1,
                                                                                         trial_number=offset_adjusted_trial,
                                                                                         fps=self.fps[i],
                                                                                         total_frames_number=self.fps[i] * self.video_duration,
                                                                                         landing_latency=self.ll_data.iloc[i][t],
                                                                                         moc=self.moc_data.iloc[i][t],
                                                                                         mol=self.mol_data.iloc[i][t],
                                                                                         group_name=self.group_name + "-NF",
                                                                                         trial_data_path=self.fly_kinematic_data_path[f"F{i + 1}T{offset_adjusted_trial}"],
                                                                                         joints=self.joints)
                    self.not_flying_trial_index.append((i + 1, offset_adjusted_trial))
                    # print(f"NF trial: Fly {i + 1}, Trial {t + 1}")
    # Read the kinematic data of N/A trial based on the number of fly specified
    def read_NA_trial_data(self):
        for i in range(self.total_fly_number):
            for t in range(self.trial_num - self.trial_offset):
                offset_adjusted_trial = t + 1 + self.trial_offset
                if f"F{i + 1}T{offset_adjusted_trial}" not in self.fly_kinematic_data_path:
                    break
                if pd.isna(self.ll_data.iloc[i][t]):
                    self.fly_kinematic_data[f"F{i + 1}T{offset_adjusted_trial}"] = Trial(fly_number=i + 1,
                                                                                         trial_number=offset_adjusted_trial,
                                                                                         fps=self.fps[i],
                                                                                         total_frames_number=self.fps[i] * self.video_duration,
                                                                                         landing_latency=self.ll_data.iloc[i][t],
                                                                                         moc=self.moc_data.iloc[i][t],
                                                                                         mol=self.mol_data.iloc[i][t],
                                                                                         group_name=self.group_name + "-NA",
                                                                                         trial_data_path=self.fly_kinematic_data_path[f"F{i + 1}T{offset_adjusted_trial}"],
                                                                                         joints=self.joints)
                    self.NA_trial_index.append((i + 1, offset_adjusted_trial))
                    # print(f"NA trial: Fly {i + 1}, Trial {t + 1}")
    # Read all type of trial data
    def read_all_data(self):
        self.read_landing_trial_data()
        print("Read landing data")
        self.read_flying_trial_data()
        print("Read flying data")
        self.read_not_flying_trial_data()
        print("Read NF data")
        self.read_NA_trial_data()
        print("Read N/A data")

    def get_targeted_trials(self, trial_types):
        merge_trial = []
        if "NA" in trial_types:
            merge_trial = sorted(merge_trial + self.NA_trial_index)
        if "NF" in trial_types:
            merge_trial = sorted(merge_trial + self.not_flying_trial_index)
        if "Landing" in trial_types:
            merge_trial = sorted(merge_trial + self.landing_trial_index)
        if "Flying" in trial_types:
            merge_trial = sorted(merge_trial + self.flying_trial_index)
        merge_trial = [trial for trial in merge_trial if trial[0] in self.good_fly_index]
        return merge_trial

    def filter_nan_fly(self):
        good_data_threshold = 10
        self.good_fly_index = []
        for f in range(self.total_fly_number):
            f_values = [trial_data for trial_key, trial_data in self.fly_kinematic_data.items() if f"F{f + 1}" in trial_key]
            good_data_num = len([x for x in f_values if "Landing" in x.group_name or "Flying" in x.group_name])
            if good_data_num >= good_data_threshold:
                self.good_fly_index.append(f + 1)

    def convert_to_output_data(self):
        for index in self.get_targeted_trials(["NF"]):
            self.predicted_data[f"F{index[0]}T{index[1]}"] = "NF"
        for index in self.get_targeted_trials(["NA"]):
            self.predicted_data[f"F{index[0]}T{index[1]}"] = "N/A"

        collected_landing_data = []
        for f in range(self.total_fly_number):
            if (f + 1) in self.good_fly_index:
                fly_landing_data = []
                for t in range(self.trial_num):
                    if f"F{f + 1}T{t + 1}" in self.predicted_data:
                        fly_landing_data.append(self.predicted_data[f"F{f + 1}T{t + 1}"])
                    else:
                        fly_landing_data.append("N/A")
                collected_landing_data.append(fly_landing_data)
        return collected_landing_data

    def read_all_trials(self):
        for i in range(self.total_fly_number):
            for t in range(self.trial_num - self.trial_offset):
                offset_adjusted_trial = t + 1 + self.trial_offset
                if f"F{i + 1}T{offset_adjusted_trial}" not in self.fly_kinematic_data_path:
                    break
                self.fly_kinematic_data[f"F{i + 1}T{offset_adjusted_trial}"] = Trial(fly_number=i + 1,
                                                                                     trial_number=offset_adjusted_trial,
                                                                                     fps=self.fps[i],
                                                                                     total_frames_number=self.fps[i] * self.video_duration,
                                                                                     group_name=self.group_name,
                                                                                     trial_data_path=self.fly_kinematic_data_path[f"F{i + 1}T{offset_adjusted_trial}"],
                                                                                     joints=self.joints)
                self.landing_trial_index.append((i + 1, offset_adjusted_trial))
                print(f"Fly {i + 1}, Trial {t + 1}")
