# Import necessary package
import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)
import pandas as pd
import time
import sys
"""
Functions to store data analog input signal to a designated CSV metadata file.
"""
def Save_AI_Data(Start_Recording_Timestamp, ai_data, meta_data_file):
    global sample_rate
    """
    Args:
        Start_Recording_Timestamp: a list of the recording start timestamp for each trial of experiment.
        ai_data: a list of AI data from each camera, each list is composed of AI data from each trial.
        meta_data_file: the csv file path to store the metadata.
    """
    adjusted_timestamp = []

    # Adjust the time stamp of each recorded AI data point according to the start timestamp of each trial
    for i, trial_signal in enumerate(ai_data[0]):
        adjusted_timestamp.append([(j/sample_rate) + Start_Recording_Timestamp[i] for j in range(len(trial_signal))])

    # Create the data that will be stored.
    data_to_record = dict()
    # Iterate through all cams' AI data trial by trial
    for i in range(len(ai_data[0])):
        # Add the timestamp of data point for trial i + 1
        data_to_record[f"Trial_{i + 1}_Timestamp"] = adjusted_timestamp[i]

        # Iterate through the cams' data in the same trial
        for j in range(len(ai_data)):
            # Add the trial AI data for camera j + i to the data frame
            data_to_record[f"AI_{j + 1}_Trial_{i + 1}"] = ai_data[j][i]

    # Convert the dictionary to pd data frame and save it to the metadata file
    df = pd.DataFrame(data_to_record)
    df.to_csv(meta_data_file, index=False)

# Read the parameter passed from the main script: RunExperiment.py
Trial = int(sys.argv[1])
reference_time_stamp = float(sys.argv[2])
meta_data_file_path = str(sys.argv[3])

# Initialize the array to store AI data from each camera
ai_1_data = []
ai_2_data = []
ai_3_data = []
ai_4_data = []
ai_5_data = []
ai_6_data = []

# Initializing the data acquisition task
read_task_1 = nidaqmx.Task()
sample_rate = 20000
# Adding the AI channels, refer to actual wiring for specifying channels
read_task_1.ai_channels.add_ai_voltage_chan("Dev2/ai1:6",
                                            terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
# Initializing sample rate and mode
read_task_1.timing.cfg_samp_clk_timing(rate=sample_rate,
                                       sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                       source="OnboardClock")

start_recording_time_stamps = []
t = 0
trigger_command = ""
# Start the task
try:
    buffer_size = 10000

    # Showing subprocess is ready for experiment
    print("AI subprocess ready!")

    # Recording AI data in each trial
    while t < Trial:

        # Read the command from main script: RunExperiment.py
        trigger_command = sys.stdin.readline().strip()

        # If the command is StartAcquiring, starting recording AI data
        if trigger_command == "StartAcquiring":
            t += 1

            # Initialize the AI data from each trial
            ai_1_trial_data = []
            ai_2_trial_data = []
            ai_3_trial_data = []
            ai_4_trial_data = []
            ai_5_trial_data = []
            ai_6_trial_data = []

            # Start the task
            read_task_1.start()

            # Record the start time stamp when recording AI data
            start = time.perf_counter()
            start_recording_time_stamps.append(time.perf_counter() + reference_time_stamp)

            # Record the AI data for 10 second
            while time.perf_counter() - start < 10:
                try:
                    # Read the actual t + 1 trial data from each camera.
                    data = read_task_1.read(number_of_samples_per_channel=buffer_size)

                    # Extend the trial AI data for every second of recorded data
                    ai_1_trial_data.extend(data[0])
                    ai_2_trial_data.extend(data[1])
                    ai_3_trial_data.extend(data[2])
                    ai_4_trial_data.extend(data[3])
                    ai_5_trial_data.extend(data[4])
                    ai_6_trial_data.extend(data[5])
                except nidaqmx.errors.DaqReadError:
                    print("Read Error")
            # stop the recording task
            read_task_1.stop()

            # Append the trial AI data to the collected AI data for each camera. [[], [] ....]
            ai_1_data.append(ai_1_trial_data)
            ai_2_data.append(ai_2_trial_data)
            ai_3_data.append(ai_3_trial_data)
            ai_4_data.append(ai_4_trial_data)
            ai_5_data.append(ai_5_trial_data)
            ai_6_data.append(ai_6_trial_data)

    # close the task
    read_task_1.close()
except KeyboardInterrupt:
    read_task_1.stop()
    read_task_1.close()
    # Handle if the user interrupts the program (e.g., with Ctrl+C)
    print("Data acquisition interrupted.")

# Save the collected AI data from each camera to a csv metadata file.
Save_AI_Data(start_recording_time_stamps, [ai_1_data, ai_2_data, ai_3_data, ai_4_data, ai_5_data, ai_6_data], meta_data_file_path)

