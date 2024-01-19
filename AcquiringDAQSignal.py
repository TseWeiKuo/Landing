import pypylon.pylon as py
import numpy as np
import time
from matplotlib import pyplot as plt
from imageio import get_writer
from subprocess import Popen
import os
import concurrent.futures
import datetime
import scipy
import threading
import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)

read_task_1 = nidaqmx.Task()
ai_1_data = []
ai_2_data = []
ai_3_data = []
ai_4_data = []
ai_5_data = []
ai_6_data = []
global daq_start_time
global event_time_stamp
global ai_sample_rate
print("Start acquiring signal")
# Create a task for voltage measurement
read_task_1.ai_channels.add_ai_voltage_chan("Dev2/ai1:6",
                                            terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)  # Specify the channel

# Set the acquisition time to 5 seconds
read_task_1.timing.cfg_samp_clk_timing(rate=ai_sample_rate,
                                       sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                       source="OnboardClock")
# Start the task
read_task_1.start()
try:
    buffer_size = 10000
    event_time_stamp.append(0)
    daq_start_time = time.perf_counter()
    while not stop_daq:
        data = read_task_1.read(number_of_samples_per_channel=buffer_size)
        ai_1_data.extend(data[0])
        ai_2_data.extend(data[1])
        ai_3_data.extend(data[2])
        ai_4_data.extend(data[3])
        ai_5_data.extend(data[4])
        ai_6_data.extend(data[5])
    read_task_1.stop()
    read_task_1.close()
except KeyboardInterrupt:
    # Handle if the user interrupts the program (e.g., with Ctrl+C)
    print("Data acquisition interrupted.")

def Find_Peak(ai_data):
    return scipy.signal.find_peaks(ai_data, distance=95, prominence=[3, 5])