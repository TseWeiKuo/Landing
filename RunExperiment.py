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

def save_video(cam_img):
    global filename
    global FPS

    # print(save_path + filename + cam_img[0] +'.mp4')
    writer = get_writer(
        save_path + filename + cam_img[0] + '.mp4',  # .mp4, mkv players often support H.264, Camera1
        # test harddrive speed
        # 'E:/Brandon_Test/'+ filename +'.avi',
        # use .avi (not .mp4) format because can be opened in virtualdub
        fps=FPS,  # FPS is in units Hz; should be real-time...playback...set to actual
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



def ListeningCam():
    read_task_1 = nidaqmx.Task()
    global ai_1_data
    global ai_2_data
    global ai_3_data
    global ai_4_data
    global daq_start_time
    global event_time_stamp
    global ai_sample_rate
    print("Start acquiring signal")
    # Create a task for voltage measurement
    read_task_1.ai_channels.add_ai_voltage_chan("Dev2/ai1:4",
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
        read_task_1.stop()
        read_task_1.close()
    except KeyboardInterrupt:
        # Handle if the user interrupts the program (e.g., with Ctrl+C)
        print("Data acquisition interrupted.")

def Plot_AI_Data(ai_data):
    return
def Find_Peak(ai_data):
    return scipy.signal.find_peaks(ai_data, distance=95, prominence=[3, 5])

def CountFrames (Frames_Per_Second, Motor_Extend_time, Motor_Retract_time, Platform_stop_duration):
    return (Motor_Extend_time + Motor_Retract_time + Platform_stop_duration) * Frames_Per_Second

mk_dir = 1
if mk_dir == 1:
    dir_path = r"C:\Users\agrawal-admin\Desktop\DataFolder"
    dir_path_vid = r"C:\Users\agrawal-admin\Desktop\DataFolder\videos-raw"
    # Create target Directory if don't exist
    if not os.path.exists(dir_path_vid):
        os.mkdir(dir_path)
        os.mkdir(dir_path_vid)
        save_path = dir_path_vid + '/'
    else:
        save_path = dir_path_vid + '/'
else:
    print("Directory not created")
    # save_path='D:/Sarah/Data/Videos/'
    save_path = r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\DataFolder\videos-raw"

event_time_stamp = []
camera_start_time_stamp = []
camera_end_time_stamp = []

video_frames = []
video_frames2 = []
video_frames3 = []
video_frames4 = []

camera1_videos = []
camera2_videos = []
camera3_videos = []
camera4_videos = []

stop_daq = False
daq_start_time = 0
ai_4_data = []
ai_3_data = []
ai_2_data = []
ai_1_data = []
ai_sample_rate = 20000


T = 0
FPS = 200
ExposureTime = ((1/FPS)*1000000) - 500
print(f"ExposureTime: {ExposureTime} us")

"""
Set up and configure camera
"""
tlFactory = py.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()
print("Camera 1: " + str(devices[0].GetSerialNumber()))
print("Camera 2: " + str(devices[1].GetSerialNumber()))
print("Camera 3: " + str(devices[2].GetSerialNumber()))
print("Camera 4: " + str(devices[3].GetSerialNumber()))

camera1 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[0]))
camera1.Open()
camera1.Width.SetValue(camera1.Width.GetMax())
camera1.ExposureTime = ExposureTime
camera1.LineSelector = "Line4"
camera1.LineMode = "Output"
camera1.LineInverter = False
camera1.LineSource = "ExposureActive"
camera1.Gain = camera1.Gain.Max
camera1.MaxNumBuffer = 100
camera1.LineSelector = "Line3"
camera1.LineMode = "Input"
camera1.TriggerSelector = "FrameStart"
camera1.TriggerSource = "Line3"
camera1.TriggerActivation = "RisingEdge"
camera1.TriggerDelay = 0


camera2 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[1]))
camera2.Open()
camera2.Width.SetValue(camera1.Width.GetMax())
camera2.ExposureTime = ExposureTime
camera2.LineSelector = "Line4"
camera2.LineMode = "Output"
camera2.LineInverter = False
camera2.LineSource = "ExposureActive"
camera2.Gain = camera2.Gain.Max
camera2.MaxNumBuffer = 100
camera2.LineSelector = "Line3"
camera2.LineMode = "Input"
camera2.TriggerSelector = "FrameStart"
camera2.TriggerSource = "Line3"
camera2.TriggerActivation = "RisingEdge"
camera2.TriggerDelay = 0


camera3 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[2]))
camera3.Open()
camera3.Width.SetValue(camera1.Width.GetMax())
camera3.ExposureTime = ExposureTime
camera3.LineSelector = "Line4"
camera3.LineMode = "Output"
camera3.LineInverter = False
camera3.LineSource = "ExposureActive"
camera3.Gain = camera3.Gain.Max
camera3.MaxNumBuffer = 100
camera3.LineSelector = "Line3"
camera3.LineMode = "Input"
camera3.TriggerSelector = "FrameStart"
camera3.TriggerSource = "Line3"
camera3.TriggerActivation = "RisingEdge"
camera3.TriggerDelay = 0


camera4 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[3]))
camera4.Open()
camera4.Width.SetValue(camera1.Width.GetMax())
camera4.ExposureTime = ExposureTime
camera4.LineSelector = "Line4"
camera4.LineMode = "Output"
camera4.LineInverter = False
camera4.LineSource = "ExposureActive"
camera4.Gain = camera4.Gain.Max
camera4.MaxNumBuffer = 100
camera4.LineSelector = "Line3"
camera4.LineMode = "Input"
camera4.TriggerSelector = "FrameStart"
camera4.TriggerSource = "Line3"
camera4.TriggerActivation = "RisingEdge"
camera4.TriggerDelay = 0



TriggerM = True
if not TriggerM:
    camera1.TriggerMode = "Off"
    camera2.TriggerMode = "Off"
    camera3.TriggerMode = "Off"
    camera4.TriggerMode = "Off"
else:
    camera1.TriggerMode = "On"
    camera2.TriggerMode = "On"
    camera3.TriggerMode = "On"
    camera4.TriggerMode = "On"


# Arguments to pass to the subprocess
Target_V = 2.3
Initial_V = 1
Trial_num = 3
Platform_stop_duration = 1
inter_stim_wait_time = 5
MotorExtendTime = 2
MotorRetractTime = 2
frames_to_grab = CountFrames(Platform_stop_duration=Platform_stop_duration,
                             Motor_Extend_time=MotorExtendTime,
                             Motor_Retract_time=MotorRetractTime,
                             Frames_Per_Second=FPS)
print(f"# of frames to grab: {frames_to_grab}")


# Launch the subprocess
Send_signal_process = Popen(['python', 'subprocess_daq_trigger.py', str(FPS)])
Run_Motor = Popen(["python", "Run_Motor_Subprocess.py", str(Target_V), str(Initial_V), str(Trial_num), str(Platform_stop_duration), str(inter_stim_wait_time)])
DaqInputThread = threading.Thread(target=ListeningCam)
DaqInputThread.start()
time.sleep(1)
filename = ""


Exit = False
try:
    while not Exit:
        images_grabbed = 0

        # Clear previous video segment
        camera1_videos.clear()
        camera2_videos.clear()
        camera3_videos.clear()
        camera4_videos.clear()

        # Start the camera
        camera1.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera2.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera3.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        camera4.StartGrabbing(py.GrabStrategy_LatestImageOnly)

        # Start of video time stamp
        print("Start grabbing videos")
        camera_start_time_stamp.append((time.perf_counter() - daq_start_time) * ai_sample_rate)
        cam_start = time.perf_counter()
        # Start grabbing video
        while images_grabbed < frames_to_grab:
            try:
                grabResult = camera1.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                grabResult2 = camera2.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                grabResult3 = camera3.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                grabResult4 = camera4.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded() and grabResult2.GrabSucceeded() and grabResult3.GrabSucceeded() and grabResult4.GrabSucceeded():
                    images_grabbed += 1
                    event_time_stamp.append(time.perf_counter() - daq_start_time)
                    camera1_videos.append(grabResult.Array)
                    camera2_videos.append(grabResult2.Array)
                    camera3_videos.append(grabResult3.Array)
                    camera4_videos.append(grabResult4.Array)

                grabResult.Release()
                grabResult2.Release()
                grabResult3.Release()
                grabResult4.Release()
            except py.TimeoutException as e:
                camera1.Close()
                camera2.Close()
                camera3.Close()
                camera4.Close()
                print(f"Timeout exception: {e}")
        # End of video time stamp
        camera_end_time_stamp.append((time.perf_counter() - daq_start_time) * ai_sample_rate)
        print(f"Recording duration: {time.perf_counter() - cam_start}")

        video_frames.append(camera1_videos)
        video_frames2.append(camera2_videos)
        video_frames3.append(camera3_videos)
        video_frames4.append(camera4_videos)

        # Stop the camera
        camera1.StopGrabbing()
        camera2.StopGrabbing()
        camera3.StopGrabbing()
        camera4.StopGrabbing()

        T += 1
        time.sleep(inter_stim_wait_time)

        if Trial_num <= T:
            print("Finish all trials")
            Exit = True
            camera1.Close()
            camera2.Close()
            camera3.Close()
            camera4.Close()
            stop_daq = True
            DaqInputThread.join()

    Date_and_Experiment = str(datetime.datetime.now())
    Date_and_Experiment = Date_and_Experiment.replace(":", "-")
    Date_and_Experiment = Date_and_Experiment.replace(" ", "-")
    Date_and_Experiment += "_Fly1"


    for i in range(len(video_frames)):
        filename = Date_and_Experiment + "_Trial_" + str(i + 1)
        cam_imgs = [['Camera1', video_frames[i]], ['Camera2', video_frames2[i]], ['Camera3', video_frames3[i]], ['Camera4', video_frames4[i]]]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(save_video, cam_imgs)
            for result in results:
                print(result)  # displays when cameras are saved

except KeyboardInterrupt as k:
    print(f"Key board interrupt: {k}")
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    while Run_Motor.poll() != 0:
        continue
    Run_Motor.kill()
    Run_Motor.wait()
    Send_signal_process.kill()
    Send_signal_process.wait()
    DaqInputThread.join()

motor_delay_time = time.perf_counter()
while Run_Motor.poll() != 0:
    continue
print(f"Motor delay time: {time.perf_counter() - motor_delay_time}")
Run_Motor.kill()
Run_Motor.wait()

Send_signal_process.kill()
Send_signal_process.wait()
DaqInputThread.join()

cam1_total_frames = 0
cam2_total_frames = 0
cam3_total_frames = 0
cam4_total_frames = 0


for frames in video_frames:
    cam1_total_frames += len(frames)
for frames in video_frames2:
    cam2_total_frames += len(frames)
for frames in video_frames3:
    cam3_total_frames += len(frames)
for frames in video_frames4:
    cam4_total_frames += len(frames)


print("Total Number of images grabbed (Cam 1): " + str(cam1_total_frames))
for i in range(len(video_frames)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames[i])}")

print("Total Number of images grabbed (Cam 2): " + str(cam2_total_frames))
for i in range(len(video_frames2)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames2[i])}")

print("Total Number of images grabbed (Cam 3): " + str(cam3_total_frames))
for i in range(len(video_frames3)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames3[i])}")

print("Total Number of images grabbed (Cam 4): " + str(cam4_total_frames))
for i in range(len(video_frames4)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames4[i])}")

time_tick = list(range(0, len(ai_2_data)))
time_tick = [(x / ai_sample_rate) for x in time_tick]

print("Total Cam 1 peaks num (ai 1 data): " + str(len(Find_Peak(ai_1_data)[0])))
for i in range(len(camera_start_time_stamp)):
    print(f"Segment: {i + 1}'s number of peaks: {len(Find_Peak(ai_1_data[int(camera_start_time_stamp[i]):int(camera_end_time_stamp[i])])[0])}")

print("Total Cam 2 peaks num (ai 2 data): " + str(len(Find_Peak(ai_2_data)[0])))
for i in range(len(camera_start_time_stamp)):
    print(f"Segment: {i + 1}'s number of peaks: {len(Find_Peak(ai_2_data[int(camera_start_time_stamp[i]):int(camera_end_time_stamp[i])])[0])}")

print("Total Cam 3 peaks num (ai 3 data): " + str(len(Find_Peak(ai_3_data)[0])))
for i in range(len(camera_start_time_stamp)):
    print(f"Segment: {i + 1}'s number of peaks: {len(Find_Peak(ai_3_data[int(camera_start_time_stamp[i]):int(camera_end_time_stamp[i])])[0])}")

print("Total Cam 4 peaks num (ai 4 data): " + str(len(Find_Peak(ai_4_data)[0])))
for i in range(len(camera_start_time_stamp)):
    print(f"Segment: {i + 1}'s number of peaks: {len(Find_Peak(ai_4_data[int(camera_start_time_stamp[i]):int(camera_end_time_stamp[i])])[0])}")


peaks, _ = Find_Peak(ai_1_data)
peaks_val = [ai_1_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_1_data, color='blue')
plt.plot(peaks_time_stamp, peaks_val, "x", color='purple', markersize=15)

peaks, _ = Find_Peak(ai_2_data)
peaks_val = [ai_2_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_2_data, color='orange')
plt.plot(peaks_time_stamp, peaks_val, "o", color='brown', markersize=15)

peaks, _ = Find_Peak(ai_3_data)
peaks_val = [ai_3_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_3_data, color='green')
plt.plot(peaks_time_stamp, peaks_val, "*", color='navy', markersize=15)

peaks, _ = Find_Peak(ai_4_data)
peaks_val = [ai_4_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_4_data, color='red')
plt.plot(peaks_time_stamp, peaks_val, "^", color='gray', markersize=15)

for i in event_time_stamp:
    plt.axvline(x=i, color='olive')
for i in camera_start_time_stamp:
    plt.axvline(x=i/ai_sample_rate, color='cyan')
for i in camera_end_time_stamp:
    plt.axvline(x=i/ai_sample_rate, color='black')
plt.show()


