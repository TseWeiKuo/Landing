import h5py
import cv2
import random
import os
import datetime
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import trange
def ExtractFramesValue(Vidfile):
    cap = cv2.VideoCapture(Vidfile)
    Frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if there are no more frames
        else:
            Frames.append(frame)
    return Frames
def FilterFrames(ExtractedF_Dir):
    os.chdir(ExtractedF_Dir)
    output_csv_file = ""
    global remaining_files
    for dir in os.listdir(ExtractedF_Dir):
        print(dir)
        if len(remaining_files) == 0:
            for Img in os.listdir(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\H5ToTrainingData\ExtractedFrames\1"):
                if Img.endswith(".png"):
                    print(Img)
                    remaining_files.append(Img)
        else:
            for Img in os.listdir(dir):
                #print(1)
                if Img.endswith(".png") and Img not in remaining_files:
                    print(1)
                    os.remove(os.path.join(dir, Img))
        """
        for file in os.listdir(dir):
            if file.endswith(".csv"):
                output_csv_file = os.path.join(dir, file)
        CSV_data = pd.read_csv(output_csv_file)
        CSV_data = CSV_data[CSV_data['filename'].isin(remaining_files)]
        CSV_data.reset_index(drop=True, inplace=True)
        CSV_data.to_csv(os.path.join(dir, "via_export_csv.csv"), index=False)
        """
def WriteCsv(Predicted_data_path, Vid_File_Paths, ExtractedF_Dir, bodyparts, cam_num):
    global Frame_Width
    global Frame_Height
    global ExtractedFrames
    scorer = "DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2800000"
    extract_time_range = [500, 800]
    CollectedData = []

    Frames_output_directory = os.path.join(ExtractedF_Dir, "CollectedData")
    Frames_output_directory = ExtractedF_Dir

    if not os.path.exists(Frames_output_directory):
        os.mkdir(Frames_output_directory)

    csv_file_path = os.path.join(ExtractedF_Dir, "CollectedData.csv")
    bodys = [b for b in bodyparts for _ in range(2)]
    header = [["scorer"] + ["scorer"] * len(bodyparts) * 2, ["bodyparts"] + bodys, ["coords"] + ["x", "y"] * len(bodyparts)]

    for ca in range(cam_num):
        Predicted_data_path = Predicted_data_path[:Predicted_data_path.find(scorer) - 1] + f"{ca+1}{scorer}.csv"
        print(Predicted_data_path)
        df = pd.read_csv(Predicted_data_path, header=[0, 1, 2])
        cam_data = dict()
        for point in bodyparts:
            cam_data[f"{point}_x"] = df[(scorer, point, "x")]
            cam_data[f"{point}_y"] = df[(scorer, point, "y")]
            cam_data[f"{point}_p"] = df[(scorer, point, "likelihood")]
        cam_data = pd.DataFrame(cam_data)

        Vid_File_Paths = Vid_File_Paths[:-5] + f"{ca + 1}.mp4"
        Video = ExtractFramesValue(Vid_File_Paths)
        cam_output_directory = os.path.join(Frames_output_directory, str(ca + 1))
        if not os.path.exists(cam_output_directory):
            print("create dir")
            os.mkdir(cam_output_directory)
        for i in range(len(ExtractedFrames)):

            output_file_path = os.path.join(cam_output_directory, f"img{ExtractedFrames[i]:04d}.png")

            # Save the frame as a PNG file
            # print(output_file_path)
            cv2.imwrite(output_file_path, Video[ExtractedFrames[i]])

            # Get the file size of the saved PNG file
            # file_size = os.path.getsize(output_file_path)

            x_coord = [10, 15, 20, 25, 30]
            y_coord = [10, 15, 20, 25, 30, 35, 40, 45]
            newLine = 0
            temp = [f"{ca + 1}/img{ExtractedFrames[i]:04d}.png"]
            for p, part in enumerate(bodyparts):

                x = cam_data[f"{part}_x"][ExtractedFrames[i]]
                y = cam_data[f"{part}_y"][ExtractedFrames[i]]
                confidence = cam_data[f"{part}_p"][ExtractedFrames[i]]
                if (x > Frame_Width or y > Frame_Height) or confidence < 0.9:
                    x = x_coord[p % 5]
                    y = y_coord[newLine]
                if (p + 1) % 5 == 0:
                    newLine += 1
                temp.append(int(x))
                temp.append(int(y))
            CollectedData.append(temp)
    df = pd.DataFrame(CollectedData, columns=header)

    # Save to CSV with multi-level header
    df.to_csv(csv_file_path, index=False, header=True)

def WriteCsv_2Dprojection(Predicted_data_path, Vid_File_Paths, ExtractedF_Dir, bodyparts, cam_num):
    global Frame_Width
    global Frame_Height

    scorer = "DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2550000"
    extract_time_range = [500, 800]
    CollectedData = []


    Frames_output_directory = os.path.join(ExtractedF_Dir, "CollectedData")

    if not os.path.exists(Frames_output_directory):
        os.mkdir(Frames_output_directory)

    csv_file_path = os.path.join(Frames_output_directory, "CollectedData.csv")
    bodys = [b for b in bodyparts for _ in range(2)]
    header = [["scorer"] + ["scorer"] * len(bodyparts) * 2, ["bodyparts"] + bodys, ["coords"] + ["x", "y"] * len(bodyparts)]

    for ca in range(cam_num):
        Predicted_data_path = Predicted_data_path[:Predicted_data_path.find(scorer) - 1] + f"{ca+1}{scorer}.csv"
        df = pd.read_csv(Predicted_data_path, header=[0, 1, 2])
        cam_data = dict()
        for point in bodyparts:
            cam_data[f"{point}_x"] = df[(scorer, point, "x")]
            cam_data[f"{point}_y"] = df[(scorer, point, "y")]
            cam_data[f"{point}_p"] = df[(scorer, point, "likelihood")]
        cam_data = pd.DataFrame(cam_data)

        Vid_File_Paths = Vid_File_Paths[:-5] + f"{ca + 1}.mp4"
        Video = ExtractFramesValue(Vid_File_Paths)
        cam_output_directory = os.path.join(Frames_output_directory, str(ca + 1))
        if not os.path.exists(cam_output_directory):
            print("create dir")
            os.mkdir(cam_output_directory)
        for i in range(extract_time_range[0], extract_time_range[1], 10):

            output_file_path = os.path.join(cam_output_directory, f"img{i:04d}.png")

            # Save the frame as a PNG file
            # print(output_file_path)
            cv2.imwrite(output_file_path, Video[i])

            # Get the file size of the saved PNG file
            # file_size = os.path.getsize(output_file_path)

            x_coord = [10, 15, 20, 25, 30]
            y_coord = [10, 15, 20, 25, 30, 35, 40, 45]
            newLine = 0
            temp = [f"{ca + 1}/img{i:04d}.png"]
            for p, part in enumerate(bodyparts):

                x = cam_data[f"{part}_x"][i]
                y = cam_data[f"{part}_y"][i]
                confidence = cam_data[f"{part}_p"][i]
                if (x > Frame_Width or y > Frame_Height) or confidence < 0.9:
                    x = x_coord[p % 5]
                    y = y_coord[newLine]
                if (p + 1) % 5 == 0:
                    newLine += 1
                temp.append(int(x))
                temp.append(int(y))
            CollectedData.append(temp)
    print(len(header[0]))
    print(len(CollectedData[0]))
    df = pd.DataFrame(CollectedData, columns=header)

    # Save to CSV with multi-level header
    df.to_csv(csv_file_path, index=False, header=True)
def ExtractPoseLabelFromH5(group):
    global Data
    global Total_frames_num
    global bodyparts
    for i in list(group.keys()):
        try:
            subgroup = group[i]
            if isinstance(subgroup, h5py.Group):
                ExtractPoseLabelFromH5(subgroup)
            elif isinstance(subgroup, h5py.Dataset):
                if subgroup.shape[0] == Total_frames_num:
                    # print(subgroup.shape[0])
                    for frame in subgroup:
                        frame_data = dict()
                        prev_data_ind = 0
                        # Data.append(frame[1])
                        bp = 0
                        for data_ind in range(3, len(frame[1]) + 1, 3):
                            frame_data[bodyparts[bp]] = (list(frame[1][prev_data_ind:data_ind]))
                            prev_data_ind = data_ind
                            bp += 1
                        Data.append(frame_data)
        except Exception as e:
            print(f"Error accessing {i}: {str(e)}")
def ExtractFrames(Video_files_path, ExtractedF_Dir, bodyparts):
    global Frames_Num
    global Frame_Height
    global Frame_Width
    global Total_frames_num
    global FolderName
    global ExtractedFrames
    extract_time_range = [400, 900]

    cam = 1
    unique_random_frame_ind = []
    extracted_frame_ind = []
    # Open the video file
    for key in Video_files_path.keys():
        Data = []
        Videos = []

        print(f"Processing {key}'s data")
        FlyNum = 0


        for Vid_file in Video_files_path[key]:
            print(Vid_file)
            FlyNum += 1
            Videos.extend(ExtractFramesValue(Vid_file))

        extracted_frame_ind = range(extract_time_range[0], extract_time_range[1], 5)

        Frames_output_directory = os.path.join(ExtractedF_Dir, FolderName + key)

        if not os.path.exists(Frames_output_directory):
            os.mkdir(Frames_output_directory)

        for f in range(FlyNum):
            for i in range(len(extracted_frame_ind)):
                output_file_path = os.path.join(Frames_output_directory, f"img{extracted_frame_ind[i]:04d}.png")
                cv2.imwrite(output_file_path, Videos[extracted_frame_ind[i] + f * Total_frames_num])
        cam += 1

Data = []
Root_dir = os.getcwd()
H5_Dir = os.path.join(Root_dir, "H5")
Vid_Dir = os.path.join(Root_dir, "vids")
CSV_Dir = os.path.join(Root_dir, "CSV")
ExtractedFPath = os.path.join(Root_dir, "ExtractedFrames")
Frame_Height = 616
Frame_Width = 816
H5_By_Cam = dict()
Vid_By_Cam = dict()
CSV_By_Cam = dict()


"""
for file in os.listdir(H5_Dir):
    cam_number = int(file.split("_Cam")[1].split(".")[0])
    # Add the file to the corresponding camera number key in the dictionary
    if str(cam_number) in H5_By_Cam.keys():
        H5_By_Cam[str(cam_number)].append(os.path.join(H5_Dir, file))
    else:
        H5_By_Cam[str(cam_number)] = [os.path.join(H5_Dir, file)]
"""


"""for file in os.listdir(Vid_Dir):
    cam_number = int(file.split("_Cam")[1].split(".")[0])
    # Add the file to the corresponding camera number key in the dictionary
    if str(cam_number) in Vid_By_Cam.keys():
        Vid_By_Cam[str(cam_number)].append(os.path.join(Vid_Dir, file))
    else:
        Vid_By_Cam[str(cam_number)] = [os.path.join(Vid_Dir, file)]
"""

bodyparts = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip", "platform-tip", "L-platform-tip", "R-platform-tip", "platform-axis",
             "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT", "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT",
             "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT", "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT",
             "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT", "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"]
Segements = [["L-wing", "L-wing-hinge"], ["R-wing", "R-wing-hinge"],
             ["L-fBC", "L-fCT"], ["L-fCT", "L-fFT"], ["L-fFT", "L-fTT"], ["L-fTT", "L-fLT"],
             ["L-mBC", "L-mCT"], ["L-mCT", "L-mFT"], ["L-mFT", "L-mTT"], ["L-mTT", "L-mLT"],
             ["L-hBC", "L-hCT"], ["L-hCT", "L-hFT"], ["L-hFT", "L-hTT"], ["L-hTT", "L-hLT"],
             ["R-fBC", "R-fCT"], ["R-fCT", "R-fFT"], ["R-fFT", "R-fTT"], ["R-fTT", "R-fLT"],
             ["R-mBC", "R-mCT"], ["R-mCT", "R-mFT"], ["R-mFT", "R-mTT"], ["R-mTT", "R-mLT"],
             ["R-hBC", "R-hCT"], ["R-hCT", "R-hFT"], ["R-hFT", "R-hTT"], ["R-hTT", "R-hLT"]]

Frames_Num = 1000
Total_frames_num = 1400
extract_range = [300, 500]
step = 10
remaining_files = []
FolderName = ""
Filter = False
csv_data = r"C:\Users\agrawal-admin\Desktop\Landing\Data\2025-03-17-15-06-52.70_HCS+_UASKir2.1eGFP_G115-Iav_T2-TiTa_Fly_5_Trial_2_Cam1DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2800000.csv"
video_path = r"C:\Users\agrawal-admin\Desktop\Landing\Data\2025-03-17-15-06-52.70_HCS+_UASKir2.1eGFP_G115-Iav_T2-TiTa_Fly_5_Trial_2_Cam1.mp4"
extract_path = r"C:\Users\agrawal-admin\Desktop\Landing\frames"
ExtractedFrames = list(range(extract_range[0], extract_range[1], step))
WriteCsv(csv_data, video_path, extract_path, bodyparts, 6)
# ExtractFrames(Vid_By_Cam, ExtractedFPath, bodyparts)
# FilterFrames(ExtractedFPath)

