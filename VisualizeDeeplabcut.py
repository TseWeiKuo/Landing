
import os
import random

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import cm
import math
from scipy.ndimage import gaussian_filter1d
def replace_in_list(lst, threshold):
    return [np.nan if x < threshold else x for x in lst]
def Calculate_distance_between_points(x, y, z, x1, y1, z1):
    return np.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
def CalculateDistance(X, Y, X1, Y1):
    distances = []
    for x1_i, y1_i, x2_i, y2_i in zip(X, Y, X1, Y1):
        distance = math.sqrt((x2_i - x1_i) ** 2 + (y2_i - y1_i) ** 2)
        distances.append(distance)
    return distances
def detect_velocity_jumps(x_coords, y_coords):
    velocities = []
    jumps = []
    for i in range(1, len(x_coords)):
        velocity = np.sqrt((x_coords[i] - x_coords[i-1])**2 + (y_coords[i] - y_coords[i-1])**2)
        velocities.append(velocity)
        if velocity > 50:
            jumps.append(i)
    return velocities, jumps
# Angular Displacement Method
def angle_between_points(x1, y1, x2, y2, x3, y3):
    vec1 = [x2 - x1, y2 - y1]
    vec2 = [x3 - x2, y3 - y2]
    dot_prod = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    cos_theta = dot_prod / (norm1 * norm2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))  # Clip to handle numerical precision issues
    return np.degrees(angle)
def detect_angle_jumps(x_coords, y_coords, angle_threshold):
    jumps = []
    angles = []
    distance_threshold = 20
    for i in range(1, len(x_coords) - 1):
        distance1 = np.sqrt((x_coords[i] - x_coords[i - 1]) ** 2 + (y_coords[i] - y_coords[i - 1]) ** 2)
        distance2 = np.sqrt((x_coords[i + 1] - x_coords[i]) ** 2 + (y_coords[i + 1] - y_coords[i]) ** 2)
        # Only calculate the angle if both distances are above the threshold
        if distance1 > distance_threshold and distance2 > distance_threshold:
            angle = angle_between_points(x_coords[i - 1], y_coords[i - 1],
                                         x_coords[i], y_coords[i],
                                         x_coords[i + 1], y_coords[i + 1])
            angles.append(angle)
            if angle < angle_threshold or angle > (180 - angle_threshold):  # Detect sharp turns
                jumps.append(i)
        else:
            angles.append(np.nan)
    return angles, jumps
def detect_derivative_jumps(x_coords, y_coords):
    derivative_x = np.diff(x_coords)
    derivative_y = np.diff(y_coords)
    velocity = np.sqrt(derivative_x**2 + derivative_y**2)

    return velocity
def detect_confident_jumps(x_coords, y_coords, confidence_score):
    velocities = []
    jumps = []
    for i in range(1, len(x_coords)):
        velocity = np.sqrt((x_coords[i] - x_coords[i-1])**2 + (y_coords[i] - y_coords[i-1])**2)
        velocities.append(velocity)
        if velocity > 50 and confidence_score[i] > 0.9:
            jumps.append(i)
    return velocities, jumps
def detect_jumps_zscore(x_coords, y_coords, threshold=2.0):
    from scipy.stats import zscore
    """
    Detect jumps in 2D coordinates based on Z-score of distances between consecutive points.

    Parameters:
    - x_coords (list): List of x coordinates.
    - y_coords (list): List of y coordinates.
    - threshold (float): Z-score threshold to detect a jump (default is 2.0).

    Returns:
    - List of indices where jumps are detected.
    """
    # Calculate distances between consecutive points
    distances = np.sqrt(np.diff(x_coords) ** 2 + np.diff(y_coords) ** 2)

    # Calculate Z-scores for the distances
    z_scores = zscore(distances)
    return z_scores
def ReadCamData(source_folder, scorer, KeyPoints, start, end):
    Group_Collected_Data = dict()
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".csv"):
                data_path = os.path.join(root, file)
                df = pd.read_csv(data_path, header=[0, 1, 2])
                data = dict()
                # print(f"Processing {data_path}'s data")
                for point in KeyPoints:
                    # print(f"Processing {point} key point")
                    data[f"{point}_x"] = df[(scorer, point, "x")]
                    data[f"{point}_y"] = df[(scorer, point, "y")]
                    data[f"{point}_p"] = df[(scorer, point, "likelihood")]
                    data = pd.DataFrame(data)
                    x_coord = data[f"{point}_x"].tolist()[start:end]
                    y_coord = data[f"{point}_y"].tolist()[start:end]
                    p_score = data[f"{point}_p"].tolist()[start:end]
                    # velocities, jumps = detect_confident_jumps(x_coord, y_coord, p_score)
                    velocities, jumps = detect_velocity_jumps(x_coord, y_coord)
                    if f"{point}" not in Group_Collected_Data.keys():
                        Group_Collected_Data[f"{point}"] = []
                    Group_Collected_Data[f"{point}"].append(len(jumps))
    FinalCollectedData = []
    for joint in KeyPoints:
        FinalCollectedData.append(Group_Collected_Data[joint])
    return FinalCollectedData
def Calculate_segment_length(threeD_data, skeletons):
    global frames_num
    collected_seg_length_data = dict()
    for seg in skeletons:
        if f"{seg[0]}_{seg[1]}" not in collected_seg_length_data.keys():
            collected_seg_length_data[f"{seg[0]}_{seg[1]}"] = []
        for f in range(frames_num):
            collected_seg_length_data[f"{seg[0]}_{seg[1]}"].append(Calculate_distance_between_points(
                threeD_data[f"{seg[0]}_x"][f], threeD_data[f"{seg[0]}_y"][f], threeD_data[f"{seg[0]}_z"][f],
                threeD_data[f"{seg[1]}_x"][f], threeD_data[f"{seg[1]}_y"][f], threeD_data[f"{seg[1]}_z"][f]))
    return collected_seg_length_data
def Calculate_key_point_distance(threedData, keypoint1, keypoint2):
    global frames_num
    distances = []
    for i in range(frames_num):
        distances.append(Calculate_distance_between_points(
            threedData[f"{keypoint1}_x"][i], threedData[f"{keypoint1}_y"][i], threedData[f"{keypoint1}_z"][i],
            threedData[f"{keypoint2}_x"][i], threedData[f"{keypoint2}_y"][i], threedData[f"{keypoint2}_z"][i]))
    return distances
# KeyPoints = ["L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT", "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT", "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]
KeyPoints = [ "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT", "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT", "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"]

"""

KeyPoints = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "platform",
              "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
              "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT",
              "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT",
              "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT",
              "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT",
              "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"]
"""
KeyPointsToPlot = [["L-fFT", "L-fTT", "L-fLT"], ["R-fFT", "R-fTT", "R-fLT"],
                   ["L-mFT", "L-mTT", "L-mLT"], ["R-mFT", "R-mTT", "R-mLT"],
                   ["L-hFT", "L-hTT", "L-hLT"], ["R-hFT", "R-hTT", "R-hLT"]]
skeleton = [["R-fTT", "R-fLT"], ["R-mTT", "R-mLT"], ["R-hTT", "R-hLT"]]


frames_num = 1400
leg = 5
joint = 1
start = 0
end = 1400
FrameIndex = [x for x in range(start, end)]


Cam = 1
r"""
for ca in range(Cam):
    FinalCollectedData = []
    source_folder_CTF = r"C:\Users\agrawal-admin\Desktop\Data_to_be_analyzed\CTF_2D_tracking\Cam" + str(ca + 1)
    scorer_CTF = "DLC_resnet50_Landing_3DJan25shuffle1_1600000"

    source_folder_ODL_old = r"C:\Users\agrawal-admin\Desktop\Data_to_be_analyzed\ODL_Network-10-18-2024-TwoBarLight\Cam" + str(ca + 1)
    scorer_ODL_old = "DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2050000"

    source_folder_ODL_new = r"C:\Users\agrawal-admin\Desktop\Data_to_be_analyzed\ODL_Network-10-28-2024-TwoBarLight\Cam" + str(ca + 1)
    scorer_ODL_new = "DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2550000"

    FinalCollectedData.extend(ReadCamData(source_folder_CTF, scorer_CTF, KeyPoints, 0, 1000))
    FinalCollectedData.extend(ReadCamData(source_folder_ODL_old, scorer_ODL_old, KeyPoints, 200, 1000))
    FinalCollectedData.extend(ReadCamData(source_folder_ODL_new, scorer_ODL_new, KeyPoints, 200, 1000))

    print(len(FinalCollectedData[0]))
    Groups = ["Group1", "Group2", "Group3"]
    videos_per_cam = 20

    Label_ticks = [i * 15 + 3 for i in range(len(KeyPoints))]
    X_ticks = [i * 15 + k * 3 for i in range(len(KeyPoints)) for k in range(len(Groups))]


    Scatter_Xticks = []

    for i, t in enumerate(X_ticks):
        Scatter_Xticks.append(np.random.uniform(t - 0.3, t + 0.3, videos_per_cam))
    RandomY = []

    for k in range(len(Groups) * len(KeyPoints)):
        RandomY.append(np.random.randint(k, k + 20, videos_per_cam).tolist())

    palette = sns.color_palette("plasma", len(KeyPoints) * len(Groups) * 3)
    c = 0
    markers = ["o", "s", "d", "s"]
    plt.figure(figsize=(30, 18))
    plt.suptitle(f"Cam {ca + 1}", fontsize=50)
    print(len(Scatter_Xticks[0]))
    for j in range(len(Groups)):
        for i in range(j, len(KeyPoints) * len(Groups), len(Groups)):
            sns.scatterplot(x=Scatter_Xticks[i][:len(FinalCollectedData[c])], y=FinalCollectedData[c], color=palette[(i - j) * 3], marker=markers[j], s=300, edgecolor='black', linewidth=1, alpha=0.5)
            c += 1
    plt.xticks(ticks=Label_ticks, labels=KeyPoints, rotation=90, fontsize=30)
    plt.yticks(ticks=[0, 200, 400, 600], fontsize=30)
    plt.ylim(-30, 800)
    sns.despine(top=True, right=True)
    plt.tick_params(width=4, length=15)
    plt.ylabel(ylabel="# of jumps detected", fontsize=30)
    plt.gca().spines['bottom'].set_linewidth(4)
    plt.gca().spines['left'].set_linewidth(4)
    plt.savefig(f"Jumps_in_joints_cam{ca + 1}")
    plt.tight_layout()
    # plt.show()
"""
r"""
data_path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\TestingData\TwoBarLight\2024-10-29\Fly_3\2024-10-29-15-03-32.44_TwoBarLight_Fly_3_Trial_3_Cam4DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2550000.csv"
scorer = "DLC_resnet50_TibiaTarsusPlatformODLightOct19shuffle1_2550000"
df = pd.read_csv(data_path, header=[0, 1, 2])
data = dict()
for point in KeyPoints:
    # print(f"Processing {point} key point")
    data[f"{point}_x"] = df[(scorer, point, "x")]
    data[f"{point}_y"] = df[(scorer, point, "y")]
    data[f"{point}_p"] = df[(scorer, point, "likelihood")]
data = pd.DataFrame(data)
x_coord = data["L-fLT_x"]
y_coord = data["L-fLT_y"]
p_score = data["L-fLT_p"]

velocities, jumps = detect_velocity_jumps(x_coord, y_coord, p_score)
print(jumps)
confident_jumps = detect_confident_jumps(x_coord, y_coord, p_score)
print(confident_jumps)
sns.pointplot(x=FrameIndex, y=velocities, join=False, markersize=2)
# sns.pointplot(x=FrameIndex, y=y_coord, join=False, markersize=2)
plt.xticks([0, 200, 400, 600, 800, 1000, 1200, 1400])
plt.tight_layout()
# plt.show()
"""


palette = ["gray", "y", "cyan"]
data = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\network\dlc-models\iteration-Network-01-10-2024\TibiaTarsusPlatformODLightOct19-trainset95shuffle1\train\learning_stats.csv")

sns.lineplot(data["loss"])

plt.show()

