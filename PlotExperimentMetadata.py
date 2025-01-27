import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

frames_timestamp = pd.read_csv(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\TrainingData\T3_TTa\2025-01-15\Fly_3\TrainingData_T3_TTa_2025-01-15_Fly_3_Metadata.csv")
# AI_timestamp = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\DataFolder\RecordingIssueTesting\FrameTriggerWait\2024-10-04\Fly_1\RecordingIssueTesting_FrameTriggerWait_2024-10-04_Fly_1_Camera_Signal_Metadata.csv")
frames_timestamp = frames_timestamp["FramesGrabbedTimeStamp"]


for t in frames_timestamp:
    plt.axvline(t)
plt.show()