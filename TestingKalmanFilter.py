import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

other_meta = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\DataFolder\Test\TestingCamSynch\2025-06-03\Fly_3\Test_TestingCamSynch_2025-06-03_Fly_3_Metadata.csv")
camera_signal_meta = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\DataFolder\Test\TestingCamSynch\2025-06-03\Fly_3\Test_TestingCamSynch_2025-06-03_Fly_3_Camera_Signal_Metadata.csv")

ref = other_meta["Trial_1_FramesTimeStamp"][0]

for f in other_meta["Trial_1_FramesTimeStamp"]:
    plt.axvline(f, color="black")
sns.lineplot(x=camera_signal_meta["Trial_1_Timestamp"], y=camera_signal_meta["AI_1_Trial_1"])
sns.lineplot(x=camera_signal_meta["Trial_1_Timestamp"], y=camera_signal_meta["AI_2_Trial_1"])
sns.lineplot(x=camera_signal_meta["Trial_1_Timestamp"], y=camera_signal_meta["AI_3_Trial_1"])
sns.lineplot(x=camera_signal_meta["Trial_1_Timestamp"], y=camera_signal_meta["AI_4_Trial_1"])
sns.lineplot(x=camera_signal_meta["Trial_1_Timestamp"], y=camera_signal_meta["AI_5_Trial_1"])
sns.lineplot(x=camera_signal_meta["Trial_1_Timestamp"], y=camera_signal_meta["AI_6_Trial_1"])
plt.show()
