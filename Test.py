
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
video_folder = r"C:\Users\agrawal-admin\Desktop\DataFolder\videos-raw"
os.chdir(video_folder)
for dir in os.listdir(video_folder):
    video_files = os.path.join(video_folder, dir)
    os.chdir(video_files)
    for file in os.listdir(video_files):
        if 'Fly' not in file:
            new_name = file[:10] + "_" + dir + file[10:]
            os.rename(file, new_name)