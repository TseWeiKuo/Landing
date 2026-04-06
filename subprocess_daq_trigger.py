# Import necessary package
import json
import time

import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)
import numpy as np
import sys
import matplotlib.pyplot as plt


"""
Rotate an array by n unit
"""
def rotate_array(arr, n):
    return np.append(arr[n:], arr[:n])

# Initialize the FPS, trial num and recording mode based on parameters from the main script: RunExperiment.py
make_plot = False
if not make_plot:
    fps = int(sys.argv[1])
    trial_num = int(sys.argv[2])
    Continuous_recording = int(sys.argv[3])  # 1 means continuous recording for calibration video, 2 means trial recording
    No_light_trials = json.loads(sys.argv[4])
    print(No_light_trials)
# Initialize the FPS, trial num and recording mode based on parameters from the main script: RunExperiment.py
else:
    fps = 250
    trial_num = 1
    Continuous_recording = 7
    No_light_trials = None

# The trial duration of generated AO signal
trial_duration = 7
trigger_duration = trial_duration + 1

# Set the trigger voltage value
TriggerVoltage = 5
# Set the AO dac rate
dac_rate = 100000

# Generate arrays to send out for AO signal
n_samp = int(trigger_duration * dac_rate)
# Initialize signal for camera trigger pulse
sig = np.zeros(n_samp)
# Initialize signal for IR light trigger pulse
sig_R = np.zeros(n_samp)
# Initialize signal for IR light trigger pulse
sig_R_f = np.zeros(n_samp)
# Initialize signal for IR light trigger pulse

light_duration = 2
light_start = 3
sig_RedLight = np.zeros(int(light_duration * dac_rate))

"""
Camera trigger pulse generation
"""
# The interval_size = number of AO data points per frame
interval_size = int(dac_rate * (1 / fps))
# Setting the duty cycle within the interval_size: 0.5
samples_high = round(interval_size / 2)
# Iterate through the array to set the voltage pulse in chunks
start_r = samples_high
while start_r < n_samp:
    sig[start_r:start_r + samples_high] = TriggerVoltage
    start_r += interval_size

"""
Ring light trigger pulse generation
"""
# The interval_size_R = number of AO data points per frame
interval_size_R = int(dac_rate * (1 / fps))
# Setting the duty cycle
samples_high_R = 8
start_R = samples_high_R
while start_R < n_samp:
    sig_R[start_R:start_R + samples_high_R] = TriggerVoltage
    start_R += interval_size_R

"""
Ring light trigger pulse generation
"""
# The interval_size_R = number of AO data points per frame
interval_size_R_f = int(dac_rate * (1 / fps))
# Setting the duty cycle
samples_high_R_f = 1
# samples_high_R_f = int(interval_size_R_f / 2)
start_R_f = samples_high_R_f
while start_R_f < n_samp:
    sig_R_f[start_R_f:start_R_f + samples_high_R_f] = TriggerVoltage
    start_R_f += interval_size_R_f
"""
Red light trigger pulse generation
"""
light_fps = 30
# The interval_size_R = number of AO data points per frame
interval_size_RedLight = int(dac_rate * (1 / light_fps))
# Setting the duty cycle
samples_high_RedLight_cond1 = 200
samples_high_RedLight_cond2 = 500
samples_high_RedLight_cond3 = 1500
samples_high_RedLight_cond4 = 2200

# samples_high_RedLight_to_use = samples_high_RedLight_cond1
# samples_high_RedLight_to_use = samples_high_RedLight_cond2
# samples_high_RedLight_to_use = samples_high_RedLight_cond3
samples_high_RedLight_to_use = samples_high_RedLight_cond4

# samples_high_R_f = int(interval_size_R_f / 2)
start_RedLight = samples_high_RedLight_to_use
r = 0
# print(len(sig_RedLight))
while start_RedLight < len(sig_RedLight):
    # print(start_RedLight)
    sig_RedLight[start_RedLight:start_RedLight + samples_high_RedLight_to_use] = 3
    start_RedLight += interval_size_RedLight

# sig_RedLight = rotate_array(sig_RedLight, start_RedLight - 1)

start = np.zeros(int(light_start * dac_rate))
end = np.zeros(int((trigger_duration - light_duration - light_start) * dac_rate))
light_on = np.full(int(light_duration * dac_rate), 3)

sig_RedLight = np.concatenate((start, sig_RedLight))
sig_RedLight = np.concatenate((sig_RedLight, end))

constant_light = np.concatenate((start, light_on))
constant_light = np.concatenate((constant_light, end))

light_to_use = sig_RedLight
# light_to_use = constant_light
No_light = np.full(int(trigger_duration * dac_rate), 0)

# rotate the trigger pulse such that the camera and light pulse align
sig = rotate_array(sig, samples_high - 1)
sig_R = rotate_array(sig_R, samples_high_R - 1)
sig_R_f = rotate_array(sig_R_f, samples_high_R_f - 1)
light_to_use = rotate_array(light_to_use, samples_high_RedLight_to_use - 1)

sig = np.asarray(sig)
sig_R = np.asarray(sig_R)
sig_R_f = np.asarray(sig_R_f)
light_to_use = np.asarray(light_to_use)

duration = 30

if make_plot:
    # plt.plot(sig)
    # plt.plot(sig_R)
    # plt.plot(sig_R_f)
    plt.plot(light_to_use)
    plt.show()

# mode = 2 when the AO is sent trial by trial
if Continuous_recording == 2:

    # Configure and run the DAQ task
    with nidaqmx.Task() as task:
        try:

            # Add AO channels
            task.ao_channels.add_ao_voltage_chan("Dev2/ao1")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao2")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao3")
            # Configure the task
            task.timing.cfg_samp_clk_timing(dac_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
            # Prepare the data for AO signal
            data = np.vstack([sig, sig_R, sig_R_f, light_to_use])
            no_light_data = np.vstack([sig, sig_R, sig_R_f, No_light])
            t = 0

            # Showing subprocess is ready for experiment
            print("AO subprocess ready!")

            # Send AO signal for each trial
            while t < trial_num:

                # Listen to main strip for command: RunExperiment.py
                trigger_command = sys.stdin.readline().strip()

                # If command is to send signal
                if trigger_command == "SendSignal":

                    # Write data to all channels simultaneously
                    if (t + 1) in No_light_trials:
                        print("No Light")
                        task.write(no_light_data, auto_start=True)
                    else:
                        print("Light on")
                        task.write(data, auto_start=True)
                    # task.write(data, auto_start=True)

                    # Wait while the command is still send signal and stop when being told to stop
                    while sys.stdin.readline().strip() != "StopSendingSignal":
                        pass

                    # Stop the task
                    task.stop()
                    t += 1

            # Close the task
            task.close()
        except KeyboardInterrupt:
            task.stop()
            task.close()
            print("Keyboard Interrupt")
# mode = 1 when recording long calibration video
elif Continuous_recording == 1:

    # Configure daq task
    with nidaqmx.Task() as task:
        try:
            # Add AO channels
            task.ao_channels.add_ao_voltage_chan("Dev2/ao1")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao0")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao2")

            # Configure task
            task.timing.cfg_samp_clk_timing(dac_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Prepare AO data
            data = np.vstack([sig, sig_R, sig_R_f])

            # Write data to multiple channels
            task.write(data, auto_start=True)

            # Wait for stop signal
            while sys.stdin.readline().strip() != "StopSendingSignal":
                pass

            # Stop and close the task
            task.stop()
            task.close()
        except KeyboardInterrupt:
            task.stop()
            task.close()
            print("Keyboard Interrupt")
elif Continuous_recording == 3:
    # Configure daq task
    with nidaqmx.Task() as task:
        try:
            # Add AO channels
            task.ao_channels.add_ao_voltage_chan("Dev2/ao1")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao0")

            # Configure task
            task.timing.cfg_samp_clk_timing(dac_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Prepare AO data
            data = np.vstack([sig, sig_R])

            # Write data to multiple channels
            task.write(data, auto_start=True)

            start_time = time.perf_counter()
            # Wait for stop signal
            while time.perf_counter() - start_time < duration:
                pass

            # Stop and close the task
            task.stop()
            task.close()
        except KeyboardInterrupt:
            task.stop()
            task.close()
            print("Keyboard Interrupt")
