
import cv2

import numpy as np
import pandas as pd
import toml
import matplotlib.pyplot as plt

meta_data = pd.read_csv(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder\TrainingData\T3_TTa\2025-01-19\Fly_1\TrainingData_T3_TTa_2025-01-19_Fly_1_Metadata.csv")
for t in meta_data["Trial_15_FramesTimeStamp"]:
    plt.axvline(t)
plt.show()