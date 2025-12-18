
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

Segments = [["L-wing", "L-wing-hinge"], ["R-wing", "R-wing-hinge"], ["abdomen-tip"],
              ["platform-tip", "L-platform-tip", "R-platform-tip", "platform-axis"],
              ["R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT"], ["R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT"],
              ["R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT"], ["L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT"],
              ["L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT"], ["L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]]
Key_points = ["L-wing", "L-wing-hinge", "R-wing", "R-wing-hinge", "abdomen-tip",
              "platform-tip", "L-platform-tip", "R-platform-tip", "platform-axis",
              "R-fBC", "R-fCT", "R-fFT", "R-fTT", "R-fLT", "R-mBC", "R-mCT", "R-mFT", "R-mTT", "R-mLT",
              "R-hBC", "R-hCT", "R-hFT", "R-hTT", "R-hLT", "L-fBC", "L-fCT", "L-fFT", "L-fTT", "L-fLT",
              "L-mBC", "L-mCT", "L-mFT", "L-mTT", "L-mLT", "L-hBC", "L-hCT", "L-hFT", "L-hTT", "L-hLT"]
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
frame_index = 700

import h5py
h5file = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\Network-07-04\Optogenetics\ANxGTACR-Max\ANxGTACR-Max-F1\pose-2d\2025-10-20-11-47-27.21_Optogenetics_ANxGTACR-Max_NL_Fly_1_Trial_1_Cam4.h5"
# Open the HDF5 file (read mode)
with h5py.File(h5file, "r") as f:
    # List all groups and datasets
    def print_h5_structure(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"Dataset: {name}, shape: {obj.shape}, dtype: {obj.dtype}")
        elif isinstance(obj, h5py.Group):
            print(f"Group: {name}")

    f.visititems(print_h5_structure)

    data = f["df_with_missing/table"][:]  # load all data
    frames_data = []
    point_predictions = []
    single_prediction = dict()
    k = 0
    for i in range(len(data[frame_index][1])):
        if (i + 1) % 60 == 0:
            single_prediction[Key_points[k]] = point_predictions
            k += 1
            point_predictions = []
        if (i + 1) % 3 == 0:
            point_predictions.append((float(data[frame_index][1][i - 2]), float(data[frame_index][1][i - 1]), float(data[frame_index][1][i])))

video_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\Optogenetics\ANxGTACR-Max\2025-10-20\Fly_1\2025-10-20-11-47-27.21_Optogenetics_ANxGTACR-Max_NL_Fly_1_Trial_1_Cam4.mp4"
import cv2

# ---------- Grab frame ----------
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise RuntimeError(f"Could not open {video_path}")
# Jump to desired frame and read
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
ok, frame_bgr = cap.read()
cap.release()
if not ok:
    raise RuntimeError(f"Could not read frame {frame_index} from {video_path}")

# Convert BGR (OpenCV) -> RGB (matplotlib)
# frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
frame = frame_bgr
h, w = frame.shape[:2]


for segment in Segments:
    plt.figure(figsize=(8, 8))
    plt.imshow(frame, origin="upper")
    points_to_plot = []
    # ---------- Prepare data ----------
    for s in segment:
        points_to_plot.extend(single_prediction[s])


    pts = np.array(points_to_plot, dtype=float)  # shape (N, 3)
    xs, ys, conf = pts[:, 0], pts[:, 1], pts[:, 2]

    # Clip points to image bounds (optional safety)
    mask = (xs >= 0) & (xs < w) & (ys >= 0) & (ys < h)
    xs, ys, conf = xs[mask], ys[mask], conf[mask]

    score_map = np.zeros((h, w), dtype=np.float32)

    # Parameters for the soft blob
    sigma = 7  # controls blob width (in pixels)
    radius = int(3 * sigma)  # local patch size

    for x, y, c in zip(xs, ys, conf):
        if c <= 0:
            continue  # skip zero-confidence points
        ix, iy = int(round(x)), int(round(y))
        # Bounding box for local patch
        x_min, x_max = max(0, ix - radius), min(w, ix + radius + 1)
        y_min, y_max = max(0, iy - radius), min(h, iy + radius + 1)

        # Create coordinate grid relative to the point
        yy, xx = np.mgrid[y_min:y_max, x_min:x_max]
        g = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma ** 2))
        g *= c  # scale by confidence (peak = confidence value)

        # Blend with existing map — keep max at each pixel
        score_map[y_min:y_max, x_min:x_max] = np.maximum(
            score_map[y_min:y_max, x_min:x_max],
            g
        )

    # Normalize 0..1 for visualization
    mmin, mmax = score_map.min(), score_map.max()
    if mmax > mmin:
        score_vis = (score_map - mmin) / (mmax - mmin)
    else:
        score_vis = score_map  # all zeros case

    # Use default colormap; alpha controls overlay strength
    plt.imshow(score_map, origin="upper", alpha=0.5)

    plt.title(f"Score-map overlay (frame {frame_index})")
    plt.axis("off")
    plt.show()