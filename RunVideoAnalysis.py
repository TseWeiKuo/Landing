import deeplabcut
import time
import tensorflow as tf
import subprocess
import os
import shutil
import re
from natsort import natsorted

def getVideoPaths(video_folder, filetype):
    video_paths = []
    for root, dirs, files in os.walk(video_folder):
        for file in files:
            if file.endswith(filetype):
                # Get the full path of the input file
                input_file_path = os.path.join(root, file)
                video_paths.append(input_file_path)

    video_paths = natsorted(video_paths)
    return video_paths



Anipose_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-03-14"
DLC_analyzed_data_folder = r"C:\Users\agrawal-admin\DLCData\Network-03-14"
DLC_config_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\network\config.yaml"
Data_folder = r"C:\Users\agrawal-admin\Desktop\DataFolder\HCS+_UASKir2.1eGFP\CSS-0048_T2-TiTa"
video_paths = getVideoPaths(Data_folder, ".mp4")

# comps = base_dir.split('\\')

unique_fly_combinations = {}
patter = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2})\\Fly_(?P<fly_num>\d+)\\(?P<TimeStamp>\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.\d+)_(?P<experiment>[\w]+)_(?P<group_name>[\w-]+)_(?P<joint_name>[\w-]+)_Fly_\d+_Trial_\d+')
# patter = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2})\\Fly_(?P<fly_num>\d+)\\(?P<TimeStamp>\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.\d+)_(?P<experiment>[^_]+(?:_[^_]+)*)_(?P<group_name>[^_]+_[^_]+)_(?P<joint_name>[\w-]+)_Fly_\d+_Trial_\d+')
destinations = {}
grouped_files = {}
Anipose_Data_Folders = {}
GroupType = {}
Fly_counter = 0
# Iterate through the file paths
for file_path in video_paths:
    parts = file_path.split("\\")
    experiment = parts[-5]
    group_name = parts[-4]
    date = parts[-3]
    fly_folder = parts[-2]
    fly_num = fly_folder.split("_")[1]  # gets "7"
    # match = patter.search(file_path)

    if group_name not in GroupType:
        GroupType[group_name] = True
        unique_fly_combinations = {}
        Fly_counter = 0

    # print(group_name)
    # Combine date and fly number to create a unique key for each (date, fly number) combination
    unique_key = f"{group_name}\\{date}\\Fly_{fly_num}"

    # If the combination is unique, create a new folder (increment the counter)
    if unique_key not in unique_fly_combinations:
        Fly_counter += 1
        unique_fly_combinations[unique_key] = Fly_counter

    fly_key = f"Fly_{unique_fly_combinations[unique_key]}"
    # Get the fly folder number (F1, F2, ...)
    fly_folder_number = unique_fly_combinations[unique_key]


    # Create the experiment folder if it doesn't exist
    experiment_folder = os.path.join(DLC_analyzed_data_folder, experiment)
    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder, exist_ok=True)
        print(f"Created experiment folder: {experiment_folder}")

    group_folder = os.path.join(experiment_folder, group_name)
    if not os.path.exists(group_folder):
        os.makedirs(group_folder, exist_ok=True)
        print(f"Created group folder: {group_folder}")

    # Create the group + fly folder
    # Build the unique fly folder name based on the date and fly number

    fly_folder_name = f"{group_name}-F{fly_folder_number}"
    fly_folder = os.path.join(group_folder, fly_folder_name)

    if unique_key not in destinations:
        destinations[unique_key] = fly_folder

    if not os.path.exists(fly_folder):
        os.makedirs(fly_folder, exist_ok=True)
        print(f"Created folder: {fly_folder}")

    # Add the file to the corresponding Fly_N group
    if unique_key not in grouped_files:
        grouped_files[unique_key] = []
    grouped_files[unique_key].append(file_path)


    Anipose_Experiment_folder = os.path.join(Anipose_path, experiment)
    if not os.path.exists(Anipose_Experiment_folder):
        os.makedirs(Anipose_Experiment_folder, exist_ok=True)

    Anipose_group_folder = os.path.join(Anipose_Experiment_folder, group_name)
    if not os.path.exists(Anipose_group_folder):
        os.makedirs(Anipose_group_folder, exist_ok=True)


    Anipose_fly_folder = os.path.join(Anipose_group_folder, os.path.join(fly_folder_name, r"pose-2d"))
    if unique_key not in Anipose_Data_Folders:
        Anipose_Data_Folders[unique_key] = Anipose_fly_folder

    if not os.path.exists(Anipose_fly_folder):
        os.makedirs(Anipose_fly_folder, exist_ok=True)



print(tf.config.list_physical_devices("GPU"))
start_time = time.perf_counter()
try:
    for k in destinations.keys():
        # print(grouped_files[k])
        print(destinations[k])
        print(Anipose_Data_Folders[k])
        deeplabcut.analyze_videos(DLC_config_path, grouped_files[k], save_as_csv=False, destfolder=destinations[k], videotype="mp4")
except KeyboardInterrupt:
    print("Video analysis interrupted")


for k in destinations.keys():
    for root, dirs, files in os.walk(destinations[k]):
        for file in files:
            if file.endswith(".h5"):
                # Get the full path of the input file
                input_file_path = os.path.join(root, file)
                print(input_file_path)
                output_file_path = os.path.join(Anipose_Data_Folders[k], file)
                new_filename = output_file_path[:output_file_path.find("Cam") + 4] + ".h5"
                new_destination_path = os.path.join(Anipose_Data_Folders[k], new_filename)
                # print(len(new_destination_path))

                if os.path.isfile(new_destination_path):
                    print("File exists.")
                else:
                    shutil.copy(input_file_path, new_destination_path)
                    print("File does not exist.")
                # Copy the file with the new name


# Run 'anipose filter' command in the specified directory
subprocess.run(["anipose", "filter"], cwd=Anipose_path)

print(f"Total analysis time {time.perf_counter() - start_time}")