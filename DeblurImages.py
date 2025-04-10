
import os
import shutil
import cv2
import numpy as np




source_folder = r"C:\Users\agrawal-admin\Desktop\DeeplabcutAnalyzedData\Network-03-14\G106-HP1_T2-TiTa_DLC_output"
dest_folder = r"C:\Users\agrawal-admin\Desktop\DeeplabcutAnalyzedData\Network-03-14\G106-HP1-T2-TiTa_H5"


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
            print(new_filename)
            new_destination_path = os.path.join(dest_folder, new_filename)
            print(new_destination_path)
            # Copy the file with the new name
            # shutil.copy(input_file_path, new_destination_path)
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