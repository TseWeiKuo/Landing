import matplotlib.pyplot as plt
import pandas as pd
import re
from moviepy.editor import VideoFileClip, clips_array
import matplotlib
import seaborn as sns
import numpy as np

from moviepy.editor import VideoFileClip, clips_array
ca = 2
video_1 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_Cam1.mp4"
video_2 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_Cam2.mp4"
video_3 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_Cam3.mp4"
video_4 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_Cam4.mp4"
video_5 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_Cam5.mp4"
video_6 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-2d-proj\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_Cam6.mp4"
video_7 = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\videos\videos-3d\2024-10-29-15-10-33.92_TwoBarLight_Fly_4_Trial_1_.mp4"

# Load the four video clips
clip1 = VideoFileClip(video_1)
clip2 = VideoFileClip(video_2)
clip3 = VideoFileClip(video_3)
clip4 = VideoFileClip(video_4)
clip5 = VideoFileClip(video_5)
clip6 = VideoFileClip(video_6)
clip7 = VideoFileClip(video_7)
clips = [clip1, clip2, clip3, clip4, clip5, clip6]

# Resize videos to half their size (assuming they are the same resolution)
# clip1_resized = clip1.resize(0.5)
# clip2_resized = clip2.resize(0.5)
# clip3_resized = clip3.resize(0.5)
# clip4_resized = clip4.resize(0.5)

# Arrange clips in a 2x2 grid
final_clip = clips_array([[clips[ca - 1], clip7]])

# Write the result to a file
final_clip.write_videofile(f"combined_video_{ca}.mp4", fps=25)