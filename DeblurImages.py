from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import shutil
import cv2
import numpy as np

def trim_video(input_file, output_file, start_time, end_time):
    ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)



source_folder = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\LPAcrossLegsJoints\T2-TiTa\2025-01-30"
dest_folder = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\pose-2d"


"""
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".mp4"):
            # Get the full path of the input file
            input_file_path = os.path.join(root, file)
            print(input_file_path)
            # Create the corresponding path in the destination folder
            relative_path = os.path.relpath(input_file_path, source_folder)
            # print(relative_path)
            output_file_path = os.path.join(dest_folder, relative_path)
            print(output_file_path)
            # Create any necessary subdirectories in the destination folder
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            # Trim the video and save to the destination folder
            trim_video(input_file_path, output_file_path, 1, 2)
"""

for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".h5"):
            # Get the full path of the input file
            input_file_path = os.path.join(root, file)
            print(input_file_path)
            output_file_path = os.path.join(dest_folder, file)
            print(output_file_path)
            new_filename = output_file_path[:output_file_path.find("Cam") + 4] + ".h5"
            new_destination_path = os.path.join(dest_folder, new_filename)
            print(new_destination_path)
            # Copy the file with the new name
            shutil.copy(input_file_path, new_destination_path)
            # Trim the video and save to the destination folder
            # trim_video(input_file_path, output_file_path, 1, 5)

#r"C:\Users\agrawal-admin\Desktop\Landing_3D-Wayne-2024-01-25\network\config.yaml"
# data_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\TestingFootage\TestPreviousCalibration\Starved_Fly_Experiment\Starved_TTa"

# os.chdir(data_path)
# fly_folder = [f"Fly_{i + 1}" for i in range(25)]
# for folder in fly_folder:
#     os.mkdir(os.path.join(data_path, folder))


r"""

# Example usage
input_file = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\2024-04-24-15-18-13.81_300FPS_Fly_1_Trial_3_Cam4.mp4"
output_file = "2024-04-24-15-18-13.81_300FPS_Fly_1_Trial_3_Cam4_trimmed.mp4"
start_frame = 500  # Start frame number
end_frame = 1250    # End frame number

ffmpeg_extract_subclip(input_file, 1, 4, targetname=output_file)
"""