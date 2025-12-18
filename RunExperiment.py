# Import necessary package
import pypylon.pylon as py
import time
from imageio import get_writer
from subprocess import Popen
import subprocess
import os
import concurrent.futures
import datetime
import pandas as pd
import random
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

"""
Send a string command to subprocess
"""
def send_command(subprocess_instance, command):
    """

    Args:
        subprocess_instance: The subprocess to communicate with
        command: The command in string

    Returns:

    """
    try:
        # If the subprocess is still running
        if subprocess_instance.poll() is None:

            # Send the string command
            subprocess_instance.stdin.write(command + '\n')
            subprocess_instance.stdin.flush()
        else:
            print("Subprocess has terminated with return code:", subprocess_instance.returncode)
            out, err = subprocess_instance.communicate()
            if out:
                print("Subprocess output:", out)
            if err:
                print("Subprocess error:", err)
    except IOError as e:
        print(f"Error writing to subprocess: {e}")
"""
Save videos to designated folder
"""
def save_video(cam_img):
    """

    Args:
        cam_img: Images/Video data

    Returns:

    """
    global filename
    global FPS
    global Fly_Folder

    writer = get_writer(
        os.path.join(Fly_Folder, filename) + cam_img[0] + '.mp4',
        fps=FPS,
        codec='libx264',  # When used properly, this is basically
        # "PNG for video" (i.e. lossless)
        quality=None,  # disables variable compression...0 to 10
        bitrate=None,  # 1000000, # set bit rate
        pixelformat='yuv420p',  # widely used
        macro_block_size=None,
        ffmpeg_params=['-preset', 'ultrafast', '-crf', '20', '-tune', 'zerolatency'],  # crf:0-51 or tune: fastdecode
        input_params=None
    )

    # write video
    for img in cam_img[1]:
        writer.append_data(img)

    # close writer
    writer.close()
    return cam_img[0] + ' saved'
"""
Write data to designated metadata file
"""
def add_column_to_csv(filename, new_column_name, new_column_data):
    """
    Adds a new column to an existing CSV file or creates a new one if the file does not exist.

    Args:
        filename (str): The path to the CSV file to be updated or created.
        new_column_name (str): The name of the new column to add.
        new_column_data (list or pandas.Series): The data to populate the new column.
    """
    # Check if the file exists and is not empty
    try:
        with open(filename, 'r') as f:
            if f.read().strip():  # If the file contains data
                df = pd.read_csv(filename)  # Load the existing data into a DataFrame
            else:
                df = pd.DataFrame()  # Create an empty DataFrame if the file is empty
    except FileNotFoundError:
        df = pd.DataFrame()  # Create an empty DataFrame if the file does not exist

    # Add the new column to the DataFrame
    new_length = len(new_column_data)  # Length of the new column data
    if new_length > len(df):  # If the new data has more rows than the current DataFrame
        df = df.reindex(range(new_length))  # Expand the DataFrame to match the new data length
    df[new_column_name] = pd.Series(new_column_data)  # Assign the new column data to the DataFrame

    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)  # Save the DataFrame to the file without including the index
"""
Save frames grabbed time stamp data
"""
def SaveGrabTimeStamp(filename, frames_timestamp_data):

    # open the existing metadata file
    try:
        existing_df = pd.read_csv(filename)
    except FileNotFoundError:
        existing_df = pd.DataFrame()  # Create an empty DataFrame if the file doesn't exist

    # Initialize the data to be stored
    frames_time_data = dict()

    # Appending the storing data
    for i in range(len(frames_timestamp_data)):
        frames_time_data[f"Trial_{i + 1}_FramesTimeStamp"] = frames_timestamp_data[i]

    # Convert to dataframe
    df = pd.DataFrame(frames_time_data)

    # Find the maximum length between the existing DataFrame and the new DataFrame
    max_length = max(len(existing_df), len(df))

    # Pad both DataFrames to the same length with NaN
    existing_df = existing_df.reindex(range(max_length))
    df = df.reindex(range(max_length))

    # Merge the DataFrames by concatenating them column-wise
    merged_df = pd.concat([existing_df, df], axis=1)

    # Save the updated DataFrame back to the CSV file
    merged_df.to_csv(filename, index=False)
"""
Count the number of frames to record
"""
def CountFrames (Frames_Per_Second, Motor_Extend_time, Motor_Retract_time, Platform_stop_duration):
    return (Motor_Extend_time + Motor_Retract_time + Platform_stop_duration) * Frames_Per_Second
"""
Create the necessary folder and file for storing video and metadata and return the metadata file path
"""
def InitializeDataFolder(DataFolderPath, Experiment, GroupName, Date):
    global Fly_Folder

    # Join the path of the data folder with experiment name
    save_folder = os.path.join(DataFolderPath, Experiment)

    # Check if the experiment name already exist in the data folder
    if Experiment not in os.listdir(DataFolderPath):

        # if not, create one
        os.mkdir(save_folder)

    # Change cwd to the experiment folder
    os.chdir(save_folder)

    # Join the path of experiment folder with group name
    Group_Folder = os.path.join(save_folder, GroupName)

    # Check if the group name already exist in the experiment folder
    if GroupName not in os.listdir(save_folder):

        # If not, create one
        os.mkdir(Group_Folder)

    # Change the cwd to the group folder
    os.chdir(Group_Folder)

    # Join the group folder path with current today's date
    Date_Folder = os.path.join(Group_Folder, str(Date))

    # Check if the date already exist
    if str(Date) not in os.listdir(Group_Folder):

        # If not, create one
        os.mkdir(Date_Folder)

    # Change the cwd to date folder
    os.chdir(Date_Folder)

    # Check how many flies have been recorded on that particular date and + that number by 1
    Fly_num = "Fly_" + str(len([dirs for dirs in os.listdir(Date_Folder) if os.path.isdir(dirs)]) + 1)

    # Join the date folder with the number of flies recorded on that date
    Fly_Folder = os.path.join(Date_Folder, Fly_num)

    # Create the fly data folder
    os.mkdir(Fly_Folder)

    # Change cwd to that folder
    os.chdir(Fly_Folder)

    # Create the metadata file name based on experiment, group, date, fly number
    MetaData_csv_file = Experiment + "_" + Group_name + "_" + str(Date) + "_" + Fly_num + "_" + "Metadata.csv"
    Camera_signal_csv_file = Experiment + "_" + Group_name + "_" + str(
        Date) + "_" + Fly_num + "_" + "Camera_Signal_Metadata.csv"

    # Initialize empty metadata files in the cwd
    with open(MetaData_csv_file, 'w', newline='') as csvfile:
        pass
    with open(Camera_signal_csv_file, 'w', newline='') as sig_csvfile:
        pass

    # Get the absolute path of the metadata files
    MetaData_csv_file = os.path.join(Fly_Folder, MetaData_csv_file)
    Camera_signal_csv_file = os.path.join(Fly_Folder, Camera_signal_csv_file)

    return MetaData_csv_file, Camera_signal_csv_file, Fly_num
"""
Initialize the camera acquisition setting
"""
def InitializeCamera(Device, ExposureTime, sharpness, noise_reduction_value, Buffer):
    Cropped = False
    print("Camera: " + str(Device.GetSerialNumber()))
    Camera = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(Device))
    if Cropped:
        Camera.Open()
        Camera.Width.SetValue(640)
        Camera.Height.SetValue(550)
        Camera.OffsetX = 128
        Camera.OffsetY = 43
        Camera.PgiMode.Value = "On"
        Camera.NoiseReduction.Value = noise_reduction_value
        Camera.SensorReadoutMode.Value = "Fast"
        Camera.SharpnessEnhancement.Value = sharpness
        Camera.ExposureTime = ExposureTime
        Camera.LineSelector = "Line4"
        Camera.LineMode = "Output"
        Camera.LineInverter = False
        Camera.LineSource = "FrameTriggerWait"
        Camera.Gain = Camera.Gain.Max
        Camera.MaxNumBuffer = 100
        Camera.LineSelector = "Line3"
        Camera.LineMode = "Input"
        Camera.TriggerSelector = "FrameStart"
        Camera.TriggerSource = "Line3"
        Camera.TriggerActivation = "RisingEdge"
        Camera.TriggerDelay = 0
        Camera.TriggerMode = "On"
    else:
        Camera.Open()
        Camera.Width.SetValue(Camera.Width.GetMax())
        Camera.Height.SetValue(Camera.Height.GetMax())
        Camera.PgiMode.Value = "On"
        Camera.NoiseReduction.Value = noise_reduction_value
        Camera.SharpnessEnhancement.Value = sharpness
        Camera.SensorReadoutMode.Value = "Fast"
        Camera.ExposureTime = ExposureTime
        Camera.LineSelector = "Line4"
        Camera.LineMode = "Output"
        Camera.LineInverter = False
        Camera.LineSource = "ExposureActive"
        Camera.Gain = Camera.Gain.Max
        Camera.MaxNumBuffer = Buffer
        Camera.LineSelector = "Line3"
        Camera.LineMode = "Input"
        Camera.TriggerSelector = "FrameStart"
        Camera.TriggerSource = "Line3"
        Camera.TriggerActivation = "RisingEdge"
        Camera.TriggerDelay = 0
        Camera.TriggerMode = "On"
    return Camera
"""
Close subprocess
"""
def CloseSubproess(SubProcessInstance):
    while SubProcessInstance.poll() != 0:
        continue
    SubProcessInstance.kill()
    SubProcessInstance.wait()

# Initialize the designated data folder for storing video data and experiment metadata
Data_Folder_Path = r"C:\Users\agrawal-admin\Desktop\DataFolder"

# Specify the name of the experiment
Experiment = "Optogenetics"

# Specify the name of the group of the experiment
Group_name = "GTACRx49541-Max"

# Initialize the date of the experiment
Date = datetime.datetime.now().date()

# Initialize folder to store fly video
Fly_Folder = ""

# Use light?
Use_Light = True

# Initialize the needed data folder and metadata
Experiment_meta_data_file, Cameras_Signal_metadata_file, Fly_num = \
    InitializeDataFolder(Data_Folder_Path, Experiment, Group_name, Date)

# Initialize an array to record the timestamp when each frame is grabbed
Frames_grabbed_time_stamp = []
Frames_grabbed_trial_time_stamp = []

# Set the camera acquisition setting
FPS = 250  # Frame rate
ExposureTime = 75  # Exposure time
noise_reduction_value = 1  # Noise reduction
Buffer = 4000  # Recording buffer
sharpness = 3.5  # Sharpness
print(f"ExposureTime: {ExposureTime} us")

# Initialize the camera based on acquisition setting
tlFactory = py.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()

# Camera 1 initialization
camera1 = InitializeCamera(devices[0], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

# Camera 2 initialization
camera2 = InitializeCamera(devices[1], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

# Camera 3 initialization
camera3 = InitializeCamera(devices[2], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

# Camera 4 initialization
camera4 = InitializeCamera(devices[3], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

# Camera 5 initialization
camera5 = InitializeCamera(devices[4], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

# Camera 6 initialization
camera6 = InitializeCamera(devices[5], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

# Change the cwd to the where the main script RunExperiment.py is, to run the subprocess
os.chdir(r"C:\Users\agrawal-admin\Desktop\Landing")

# Set motor parameters
Target_V = 2  # Motor stop position
Initial_V = 1  # Motor start position
Trial_num = 30 # Number of trials
Platform_stop_duration = 1  # Motor stop time
inter_stim_wait_time = [10] * Trial_num  # Inter trial wait time 10s
MotorExtendTime = 3  # Maximum motor extending time
MotorRetractTime = 3  # Maximum motor retracting time
Videos_recording_time = []  # Resulting recording time of each trial
Continuous_recording = 2  # Recording mode, 2 = experiment, 1 = calibration

# Randomize light on generation
NL_trials = []
if Use_Light:
    NL_trials = sorted(random.sample(range(1, Trial_num), 15))
    # NL_trials = []


# Count the number of frames to record for each trial
frames_to_grab = CountFrames(Platform_stop_duration=Platform_stop_duration, Motor_Extend_time=MotorExtendTime, Motor_Retract_time=MotorRetractTime, Frames_Per_Second=FPS)

# Start the subprocess to acquire AI signal from cameras
Acquiring_signal_process = Popen(['python', 'acquiring_cam_signal.py', str(Trial_num), str(time.perf_counter()), str(Cameras_Signal_metadata_file)], stdin=subprocess.PIPE, text=True)

# Start the subprocess to send AO signal to camera
Send_signal_process = Popen(['python', 'subprocess_daq_trigger.py', str(FPS), str(Trial_num), str(Continuous_recording), json.dumps(NL_trials)], stdin=subprocess.PIPE, text=True)

# Create json data for motor parameters
metadata = {"Target_V": Target_V, "Initial_V": Initial_V, "Trial_Num": Trial_num, "Platform_stop_time": [1] * Trial_num}
json_data = json.dumps(metadata)

# Pass the needed parameters to the motor subprocess
command = ["python", "Run_Motor_Subprocess.py", str(json_data), str(Experiment_meta_data_file), str(time.perf_counter())]
Run_Motor = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)

# Wait for all subprocess to get ready
time.sleep(5)

# Initialize fly trial videos' filename
filename = ""

Exit = False
T = 0
try:

    # Set camera wait time
    wait_time = 5000

    # Run recording for each trial
    while not Exit:
        images_grabbed = 0

        # Initialize temporary list for storing trial video data
        camera1_videos_seg = []
        camera2_videos_seg = []
        camera3_videos_seg = []
        camera4_videos_seg = []
        camera5_videos_seg = []
        camera6_videos_seg = []

        # Initialize frames grab time stamp
        Frames_grabbed_trial_time_stamp = []

        # Start each camera
        camera1.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera2.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera3.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera4.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera5.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera6.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        print("Start grabbing videos")

        # Start sending AO signal
        send_command(Send_signal_process, "SendSignal")

        # Start acquiring AI signal
        send_command(Acquiring_signal_process, "StartAcquiring")

        # Wait half second for AO and AI subprocess to be ready
        # time.sleep(0.5)

        # Run the motor
        send_command(Run_Motor, "RunMotor")

        # Start of video recording timestamp
        cam_start = time.perf_counter()

        # Start recording
        while images_grabbed < frames_to_grab:
            try:
                # Grab image from each camera
                grabResult1 = camera1.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
                grabResult2 = camera2.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
                grabResult3 = camera3.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
                grabResult4 = camera4.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
                grabResult5 = camera5.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
                grabResult6 = camera6.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
                # if (images_grabbed + 1) % FPS == 0:
                    # print(int((images_grabbed + 1) / FPS))
                # If grab succeed
                if grabResult1.GrabSucceeded() and grabResult2.GrabSucceeded() and grabResult3.GrabSucceeded()\
                        and grabResult4.GrabSucceeded() and grabResult5.GrabSucceeded() and grabResult6.GrabSucceeded():

                    # Record current frame number
                    images_grabbed += 1

                    # Record the grab timestamp
                    Frames_grabbed_trial_time_stamp.append(time.perf_counter())

                    # Record the image data
                    camera1_videos_seg.append(grabResult1.Array)
                    camera2_videos_seg.append(grabResult2.Array)
                    camera3_videos_seg.append(grabResult3.Array)
                    camera4_videos_seg.append(grabResult4.Array)
                    camera5_videos_seg.append(grabResult5.Array)
                    camera6_videos_seg.append(grabResult6.Array)

                # Release the image
                grabResult1.Release()
                grabResult2.Release()
                grabResult3.Release()
                grabResult4.Release()
                grabResult5.Release()
                grabResult6.Release()
            except py.TimeoutException as e:

                # In case of time out exception, close all cameras
                camera1.Close()
                camera2.Close()
                camera3.Close()
                camera4.Close()
                camera5.Close()
                camera6.Close()
                print(f"Timeout exception: {e}")
                break

        # Once the trial end, stop the motor
        send_command(Run_Motor, "StopMotor")

        # Once the trial end, stop sending AO signal
        send_command(Send_signal_process, "StopSendingSignal")

        # Once the trial end, stop the AI acquisition
        send_command(Acquiring_signal_process, "StopAcquiring")

        # Showing video recording has stopped
        print("Stop Grabbing")

        # Print and record the trial recording duration
        recording_duration = time.perf_counter() - cam_start
        Videos_recording_time.append(recording_duration)
        print(f"Recording time: {recording_duration}")

        # Stop the image grabbing
        camera1.StopGrabbing()
        camera2.StopGrabbing()
        camera3.StopGrabbing()
        camera4.StopGrabbing()
        camera5.StopGrabbing()
        camera6.StopGrabbing()

        # Record frames grab time stamp
        Frames_grabbed_time_stamp.append(Frames_grabbed_trial_time_stamp)

        # Display the current trial number
        T += 1
        print(f"Trial {T}")

        # Wait for half of inter trial wait time
        time.sleep(inter_stim_wait_time[T - 1] / 2)

        # Modify name with according to light
        Light = ""
        if Use_Light:
            if T in NL_trials:
                Light = "NL_"
            else:
                Light = "LO_"


        # Get the current time stamp of recorded video
        tm = str(datetime.datetime.now().time())
        tm = tm.replace(":", "-")[:-4]

        # Get the current date of recorded video
        Date_and_time_of_exp = str(datetime.datetime.now().date()) + "-" + tm

        # Set the file name based on date, time, group name and fly number
        filename = Date_and_time_of_exp + "_" + Experiment + "_" + Group_name + "_" + Light + Fly_num + "_Trial_" + str(T)
        # print(len(camera1_videos_seg))
        # Prepare recorded data for saving
        cam_imgs = [['_Cam1', camera1_videos_seg], ['_Cam2', camera2_videos_seg], ['_Cam3', camera3_videos_seg],
                    ['_Cam4', camera4_videos_seg], ['_Cam5', camera5_videos_seg], ['_Cam6', camera6_videos_seg]]

        # Save the video
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            results = executor.map(save_video, cam_imgs)

        # Apply air puff in between trial
        print("Air puff time!")

        # Wait for half of the inter trial wait time
        time.sleep(inter_stim_wait_time[T - 1] / 2)

        # If all trials have finished recording
        if Trial_num <= T:
            print("Finish all trials")

            # Exit the loop
            Exit = True

            # Close cameras
            camera1.Close()
            camera2.Close()
            camera3.Close()
            camera4.Close()
            camera5.Close()
            camera6.Close()

            # Stop communicating with subprocesses
            Run_Motor.stdin.close()
            Send_signal_process.stdin.close()
            Acquiring_signal_process.stdin.close()
# In case of keyboard interrupt
except KeyboardInterrupt as k:
    print(f"Key board interrupt: {k}")

    # Close the camera
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()

    # Wait for motor subprocess to stop
    CloseSubproess(Run_Motor)

    # Wait for AO subprocess to stop
    CloseSubproess(Send_signal_process)

    # Wait for AI subprocess to stop
    CloseSubproess(Acquiring_signal_process)

# Close all subprocesses
print("Closing Subprocess")

# Close AO subprocess
CloseSubproess(Send_signal_process)

# Record start time of AI signal saving
s = time.perf_counter()

# Close AI signal subprocess
CloseSubproess(Acquiring_signal_process)

print(f"Time it took to save signal data {time.perf_counter() - s}")

# Close motor subprocess
CloseSubproess(Run_Motor)

# Save metadata to designated file
SaveGrabTimeStamp(Experiment_meta_data_file, Frames_grabbed_time_stamp)
add_column_to_csv(Experiment_meta_data_file, "Target_V", [Target_V])
add_column_to_csv(Experiment_meta_data_file, "Initial_V", [Initial_V])
add_column_to_csv(Experiment_meta_data_file, "Trial_Num", [Trial_num])
add_column_to_csv(Experiment_meta_data_file, "Platform_stop_time", metadata["Platform_stop_time"])
add_column_to_csv(Experiment_meta_data_file, "Inter_trial_wait_time", inter_stim_wait_time)
add_column_to_csv(Experiment_meta_data_file, "Trial_recording_time", Videos_recording_time)
if Use_Light:
    add_column_to_csv(Experiment_meta_data_file, "NoLightTrials", NL_trials)

