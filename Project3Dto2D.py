import threading
from subprocess import Popen
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from simple_pid import PID
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import animation
from moviepy.editor import VideoFileClip, clips_array
import time
from pykalman import KalmanFilter
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
import pypylon.pylon as py
import numpy as np
import cv2
import subprocess
import os
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
    return collected_seg_length_data
def update(frame):
    print(frame)
    marker_x.set_data(t[frame], x[frame])
    marker_y.set_data(t[frame], y[frame])
    marker_z.set_data(t[frame], z[frame])
    return marker_x, marker_y, marker_z
Skeletons = [["R-hTT", "R-hLT"]]
Angles = [["L-mBC", "L-mCT", "L-mFT"], ["L-mCT", "L-mFT", "L-mTT"], ["L-mFT", "L-mTT", "L-mLT"]]
KinematicVideoPath = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-3d\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_.mp4"
KinematicDataPath = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\pose-3d\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_.csv"
AngleDataPath = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\angles\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_.csv"
KinematicData = pd.read_csv(KinematicDataPath)
AngleData = pd.read_csv(AngleDataPath)
leg_length = Calculate_segment_length(KinematicData, Skeletons)

duration = 7
fps = 200
SaveVid = True
os.environ["PATH"] = r"C:\ffmpeg\bin" + ";" + os.environ["PATH"]
Collected_joint_angle = Calculate_joint_angle(KinematicData, Angles)
# Generate sample data
t = np.linspace(0, duration, duration * fps)  # 10 seconds of data at 200 fps (2000 data points)
x = Collected_joint_angle["L-mCT"]
y = Collected_joint_angle["L-mFT"]
z = Collected_joint_angle["L-mTT"]

observations = np.column_stack([x, y, z])

# Define Kalman filter
kf = KalmanFilter(initial_state_mean=[0, 0, 0, 0, 0, 0],
                  initial_state_covariance=1e-4 * np.eye(6),
                  transition_matrices=np.array([[1, 0, 0, 1, 0, 0],
                                                [0, 1, 0, 0, 1, 0],
                                                [0, 0, 1, 0, 0, 1],
                                                [0, 0, 0, 1, 0, 0],
                                                [0, 0, 0, 0, 1, 0],
                                                [0, 0, 0, 0, 0, 1]]),
                  observation_matrices=np.array([[1, 0, 0, 0, 0, 0],
                                                  [0, 1, 0, 0, 0, 0],
                                                  [0, 0, 1, 0, 0, 0]]))

# Apply Kalman filter
filtered_state_means, _ = kf.filter(observations)

# Replace mistracked data
corrected_data = np.where(np.isnan(observations), filtered_state_means[:, :3], observations)
corrected_data = np.transpose(corrected_data)

print(np.shape(corrected_data))
# Create the figure and line plot
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))

axs[0].plot(t, x, color='blue')
axs[0].plot(t, corrected_data[0], color='blue', linestyle="--")
axs[1].plot(t, y, color='orange')
axs[1].plot(t, corrected_data[1], color='orange', linestyle="--")
axs[2].plot(t, z, color='green')
axs[2].plot(t, corrected_data[2], color='green', linestyle="--")
axs[0].set_ylim(0, 180)
axs[1].set_ylim(0, 180)
axs[2].set_ylim(0, 180)

marker_x = 0
marker_y = 0
marker_z = 0
# Update function for the animation
# plt.show()


if SaveVid:
    marker_x, = axs[0].plot(0, 0, 'ro', markersize=10)  # Marker for subplot 1
    marker_y, = axs[1].plot(0, 0, 'ro', markersize=10)  # Marker for subplot 2
    marker_z, = axs[2].plot(0, 0, 'ro', markersize=10)  # Marker for subplot 3

    # Create the animation
    frames = len(t)
    # Update function for the animation
    ani = FuncAnimation(fig, update, frames=frames, interval=5, blit=True)
    writer = FFMpegWriter(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("animation.mp4", writer=writer)

    videos = [
        VideoFileClip(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_Cam1.mp4"),
        VideoFileClip(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_Cam2.mp4"),
        VideoFileClip(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_Cam3.mp4"),
        VideoFileClip(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-11-17-16-41-03.45_Kir_Control_Fly_2_Trial_2_Cam4.mp4")
    ]

    # Arrange in a 2x3 grid
    combined_projection = clips_array([
        [videos[0], videos[1]],
        [videos[2], videos[3]]
    ])

    # Save the combined projection video
    combined_projection.write_videofile("combined_projection.mp4", fps=200)
    # Show the animation
    combined_projection = VideoFileClip("combined_projection.mp4")

    video2 = VideoFileClip("animation.mp4")
    # Resize the videos to have the same height
    video2 = video2.resize(height=combined_projection.h)

    # Combine videos side by side
    combined = clips_array([[combined_projection, video2]])

    # Write the combined video to a file
    combined.write_videofile("Final_video.mp4", fps=200)