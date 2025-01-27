
import pypylon.pylon as py
import numpy as np
import time
from matplotlib import pyplot as plt
from imageio import get_writer
from subprocess import Popen, PIPE, STDOUT
import os
import concurrent.futures
import datetime
import scipy
import threading
import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)
n = 0
directory = r"C:\Users\agrawal-admin\Desktop\DataFolder\Starved_Fly_Experiment\Starved_CTF\2024-03-10"
ExperimentName = "_StarvedFlyExperiment"
GroupName = "_StarvedCTF"
Leg_and_Joints = "_T2CTF"
Fly_n_string = "_Fly_"


import pandas as pd

# Step 1: Read the CSV file
file_path = r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatformODLight-Wayne-2024-10-19\network\labeled-data\BF-T2-TTa-Data-11-15-20204-Cam6\via_export_csv.csv"
df = pd.read_csv(file_path)
print(df)
# Step 2: Modify the desired column
# Assuming you want to change the values in a column named 'column_name'
df['filename'] = df['filename'].str.replace('6/', '', regex=False)
print(df)
# Step 3: Save the changes back to the same file
df.to_csv(file_path, index=False)

r"""
# Load the CSV file
df = pd.read_csv(r"C:\Users\agrawal-admin\Desktop\TibiaTarsusPlatform-Wayne-2024-09-07\network\labeled-data\New-cam-placement\CollectedData_Wayne.csv")

# Modify the values in the first column for rows 2 to 100
# df.loc[2:1022, df.columns[0]] = df.loc[2:1022, df.columns[0]].apply(lambda x: r'labeled-data/New-cam-placement/' + str(x))

# Save the modified CSV
# df.to_csv(r'C:\Users\agrawal-admin\Desktop/modified_file.csv', index=False)

print("Rows 2 to 100 in the first column have been updated.")

df.to_hdf(os.path.join(r"C:\Users\agrawal-admin\Desktop", 'CollectedData_' + "Wayne" + '.h5'),
            'df_with_missing', format='table', mode='w')
"""
"""
for root, dirs, files in os.walk(directory):
    print("*" * 10)
    print(root)
    print(dirs)
    if len(dirs) == 0:
        n += 1

    for file in files:
        if file.endswith(".mp4"):
            old_path = os.path.join(root, file)
            # compents = file.split("_")
            # compents[5] = str(n)
            # file = compents[0] + "_" + compents[1] + "_" + compents[2] + "_" + compents[3] + "_" + compents[4] + "_" + compents[5] + "_" + compents[6] + "_" + compents[7] + "_" + compents[8]
            # print(file)
            # old_path = os.path.join(root, file)
            if n > 9:
                file = file[:22] + ExperimentName + GroupName + Leg_and_Joints + Fly_n_string + str(n) + file[41:]
            else:
                file = file[:22] + ExperimentName + GroupName + Leg_and_Joints + Fly_n_string + str(n) + file[40:]
            new_path = os.path.join(root, file)
            print(old_path)
            print(new_path)
            os.rename(old_path, new_path)
"""