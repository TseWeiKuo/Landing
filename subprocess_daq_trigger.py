# Import necessary package
import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)
import numpy as np
import sys

"""
Rotate an array by n unit
"""
def rotate_array(arr, n):
    return np.append(arr[n:], arr[:n])

# Initialize the FPS, trial num and recording mode based on parameters from the main script: RunExperiment.py
fps = int(sys.argv[1])
trial_num = int(sys.argv[2])
Continuous_recording = int(sys.argv[3])  # 1 means continuous recording for calibration video, 2 means trial recoridng

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
print(f"Light strobe duration: {((1000000/fps)/250) + 20} us")
samples_high_R = 4
start_R = samples_high_R
while start_R < n_samp:
    sig_R[start_R:start_R + samples_high_R] = TriggerVoltage
    start_R += interval_size_R

# rotate the trigger pulse such that the camera and light pulse align
sig = rotate_array(sig, samples_high - 1)
sig_R = rotate_array(sig_R, samples_high_R - 1)
sig = np.asarray(sig)
sig_R = np.asarray(sig_R)

# mode = 2 when the AO is sent trial by trial
if Continuous_recording == 2:

    # Configure and run the DAQ task
    with nidaqmx.Task() as task:
        try:

            # Add AO channels
            task.ao_channels.add_ao_voltage_chan("Dev2/ao1")
            task.ao_channels.add_ao_voltage_chan("Dev2/ao0")

            # Configure the task
            task.timing.cfg_samp_clk_timing(dac_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
            # Prepare the data for AO signal
            data = np.vstack([sig, sig_R])
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
                    task.write(data, auto_start=True)

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

            # Configure task
            task.timing.cfg_samp_clk_timing(dac_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

            # Prepare AO data
            data = np.vstack([sig, sig_R])

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
