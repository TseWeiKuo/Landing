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
    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when IMAGES_TO_GRAB images have been retrieved.
    # Create writer
    # print('C:/Users/Brandon Pratt/Desktop/Brandon/Linear Treadmill/Data/Videos/' + filename +'.mp4')
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
    global ai_5_data
    global ai_6_data
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

mk_dir = 1
if mk_dir == 1:
    dir_path = r"C:\Users\agrawal-admin\Desktop\DataFolder"
    dir_path_vid = r"C:\Users\agrawal-admin\Desktop\DataFolder\calibration/"
    # Create target Directory if don't exist
    if not os.path.exists(dir_path_vid):
        os.mkdir(dir_path_vid)
        save_path = dir_path_vid + '/'
        print("Directory ", dir_path_vid, " Created ")
    else:
        save_path = dir_path_vid
        print(save_path)
else:
    print("Directory not created")
    save_path = r"C:\Users\agrawal-admin\Desktop\DataFolder\videos-raw"


event_time_stamp = []
camera_start_time_stamp = []
camera_end_time_stamp = []


video_frames1 = []
video_frames2 = []
video_frames3 = []
video_frames4 = []
video_frames5 = []
video_frames6 = []

camera1_videos_seg = []
camera2_videos_seg = []
camera3_videos_seg = []
camera4_videos_seg = []
camera5_videos_seg = []
camera6_videos_seg = []

stop_daq = False
daq_start_time = 0
ai_6_data = []
ai_5_data = []
ai_4_data = []
ai_3_data = []
ai_2_data = []
ai_1_data = []
ai_sample_rate = 20000


T = 0
FPS = 30
Duration = 200
ExposureTime = ((1/FPS)*1000000) - 28000
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
print("Camera 5: " + str(devices[4].GetSerialNumber()))
print("Camera 6: " + str(devices[5].GetSerialNumber()))

camera1 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[0]))
camera1.Open()
camera1.Width.SetValue(camera1.Width.GetMax())
camera1.Height.SetValue(camera1.Height.GetMax())
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
camera2.Width.SetValue(camera2.Width.GetMax())
camera2.Height.SetValue(camera2.Height.GetMax())
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
camera3.Width.SetValue(camera3.Width.GetMax())
camera3.Height.SetValue(camera3.Height.GetMax())
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
camera4.Width.SetValue(camera4.Width.GetMax())
camera4.Height.SetValue(camera4.Height.GetMax())
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


camera5 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[4]))
camera5.Open()
camera5.Width.SetValue(camera5.Width.GetMax())
camera5.Height.SetValue(camera5.Height.GetMax())
camera5.ExposureTime = ExposureTime
camera5.LineSelector = "Line4"
camera5.LineMode = "Output"
camera5.LineInverter = False
camera5.LineSource = "ExposureActive"
camera5.Gain = camera5.Gain.Max
camera5.MaxNumBuffer = 100
camera5.LineSelector = "Line3"
camera5.LineMode = "Input"
camera5.TriggerSelector = "FrameStart"
camera5.TriggerSource = "Line3"
camera5.TriggerActivation = "RisingEdge"
camera5.TriggerDelay = 0


camera6 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[5]))
camera6.Open()
camera6.Width.SetValue(camera6.Width.GetMax())
camera6.Height.SetValue(camera6.Height.GetMax())
camera6.ExposureTime = ExposureTime
camera6.LineSelector = "Line4"
camera6.LineMode = "Output"
camera6.LineInverter = False
camera6.LineSource = "ExposureActive"
camera6.Gain = camera6.Gain.Max
camera6.MaxNumBuffer = 100
camera6.LineSelector = "Line3"
camera6.LineMode = "Input"
camera6.TriggerSelector = "FrameStart"
camera6.TriggerSource = "Line3"
camera6.TriggerActivation = "RisingEdge"
camera6.TriggerDelay = 0



TriggerM = True
if not TriggerM:
    camera1.TriggerMode = "Off"
    camera2.TriggerMode = "Off"
    camera3.TriggerMode = "Off"
    camera4.TriggerMode = "Off"
    camera5.TriggerMode = "Off"
    camera6.TriggerMode = "Off"
else:
    camera1.TriggerMode = "On"
    camera2.TriggerMode = "On"
    camera3.TriggerMode = "On"
    camera4.TriggerMode = "On"
    camera5.TriggerMode = "On"
    camera6.TriggerMode = "On"




# DaqInputThread = threading.Thread(target=ListeningCam)
# DaqInputThread.start()
# Launch the subprocess
Send_signal_process = Popen(['python', 'subprocess_daq_trigger.py', str(FPS)])
frames_to_grab = FPS * Duration
filename = ""

Exit = False
try:
    wait_time = 5000
    images_grabbed = 0
    # Clear previous video segment
    camera1_videos_seg.clear()
    camera2_videos_seg.clear()
    camera3_videos_seg.clear()
    camera4_videos_seg.clear()
    camera5_videos_seg.clear()
    camera6_videos_seg.clear()

    # Start the camera
    camera1.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera2.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera3.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera4.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera5.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera6.StartGrabbing(py.GrabStrategy_LatestImageOnly)

    # Start of video time stamp
    print("Start grabbing videos")
    camera_start_time_stamp.append((time.perf_counter() - daq_start_time) * ai_sample_rate)
    cam_start = time.perf_counter()
    second = 0
    # Start grabbing video
    while images_grabbed < frames_to_grab:
        try:
            if images_grabbed % FPS == 0:
                second += 1
                print(second)
            grabResult1 = camera1.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult2 = camera2.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult3 = camera3.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult4 = camera4.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult5 = camera5.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult6 = camera6.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)

            if grabResult1.GrabSucceeded() and grabResult2.GrabSucceeded() and grabResult3.GrabSucceeded()\
                    and grabResult4.GrabSucceeded() and grabResult5.GrabSucceeded() and grabResult6.GrabSucceeded():
                images_grabbed += 1
                event_time_stamp.append(time.perf_counter() - daq_start_time)
                camera1_videos_seg.append(grabResult1.Array)
                camera2_videos_seg.append(grabResult2.Array)
                camera3_videos_seg.append(grabResult3.Array)
                camera4_videos_seg.append(grabResult4.Array)
                camera5_videos_seg.append(grabResult5.Array)
                camera6_videos_seg.append(grabResult6.Array)

            grabResult1.Release()
            grabResult2.Release()
            grabResult3.Release()
            grabResult4.Release()
            grabResult5.Release()
            grabResult6.Release()
        except py.TimeoutException as e:
            camera1.Close()
            camera2.Close()
            camera3.Close()
            camera4.Close()
            camera5.Close()
            camera6.Close()
            print(f"Timeout exception: {e}")
            break
        # End of video time stamp
    camera_end_time_stamp.append((time.perf_counter() - daq_start_time) * ai_sample_rate)

    # Stop the camera
    camera1.StopGrabbing()
    camera2.StopGrabbing()
    camera3.StopGrabbing()
    camera4.StopGrabbing()
    camera5.StopGrabbing()
    camera6.StopGrabbing()

    T += 1
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()
    stop_daq = True
    # DaqInputThread.join()
    Cam = "2_"
    cam_imgs = [[Cam + 'Cam1', camera1_videos_seg], [Cam + 'Cam2', camera2_videos_seg], [Cam + 'Cam3', camera3_videos_seg],
                [Cam + 'Cam4', camera4_videos_seg], [Cam + 'Cam5', camera5_videos_seg], [Cam + 'Cam6', camera6_videos_seg]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(save_video, cam_imgs)

except KeyboardInterrupt as k:
    print(f"Key board interrupt: {k}")
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()
    Send_signal_process.kill()
    Send_signal_process.wait()
    stop_daq = True
    # DaqInputThread.join()

Send_signal_process.kill()
Send_signal_process.wait()
# DaqInputThread.join()

cam1_total_frames = 0
cam2_total_frames = 0
cam3_total_frames = 0
cam4_total_frames = 0
cam5_total_frames = 0
cam6_total_frames = 0


for frames in video_frames1:
    cam1_total_frames += len(frames)
for frames in video_frames2:
    cam2_total_frames += len(frames)
for frames in video_frames3:
    cam3_total_frames += len(frames)
for frames in video_frames4:
    cam4_total_frames += len(frames)
for frames in video_frames5:
    cam5_total_frames += len(frames)
for frames in video_frames6:
    cam6_total_frames += len(frames)


print("Total Number of images grabbed (Cam 1): " + str(cam1_total_frames))
for i in range(len(video_frames1)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames1[i])}")

print("Total Number of images grabbed (Cam 2): " + str(cam2_total_frames))
for i in range(len(video_frames2)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames2[i])}")

print("Total Number of images grabbed (Cam 3): " + str(cam3_total_frames))
for i in range(len(video_frames3)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames3[i])}")

print("Total Number of images grabbed (Cam 4): " + str(cam4_total_frames))
for i in range(len(video_frames4)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames4[i])}")

print("Total Number of images grabbed (Cam 5): " + str(cam5_total_frames))
for i in range(len(video_frames5)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames5[i])}")

print(f"Total Number of images grabbed (Cam 6): " + str(cam6_total_frames))
for i in range(len(video_frames6)):
    print(f"Segment {i + 1}'s number of frames: {len(video_frames6[i])}")

time_tick = list(range(0, len(ai_1_data)))
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

print("Total Cam 5 peaks num (ai 5 data): " + str(len(Find_Peak(ai_5_data)[0])))
for i in range(len(camera_start_time_stamp)):
    print(f"Segment: {i + 1}'s number of peaks: {len(Find_Peak(ai_5_data[int(camera_start_time_stamp[i]):int(camera_end_time_stamp[i])])[0])}")

print("Total Cam 6 peaks num (ai 6 data): " + str(len(Find_Peak(ai_6_data)[0])))
for i in range(len(camera_start_time_stamp)):
    print(f"Segment: {i + 1}'s number of peaks: {len(Find_Peak(ai_6_data[int(camera_start_time_stamp[i]):int(camera_end_time_stamp[i])])[0])}")


peaks, _ = Find_Peak(ai_1_data)
peaks_val = [ai_1_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_1_data, color='blue')
plt.plot(peaks_time_stamp, peaks_val, "x", color='cyan', linewidth=2, markersize=10)

peaks, _ = Find_Peak(ai_2_data)
peaks_val = [ai_2_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_2_data, color='gold')
plt.plot(peaks_time_stamp, peaks_val, "o", color='yellow', linewidth=2, markersize=10)

peaks, _ = Find_Peak(ai_3_data)
peaks_val = [ai_3_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_3_data, color='green')
plt.plot(peaks_time_stamp, peaks_val, "*", color='lime', linewidth=2, markersize=10)

peaks, _ = Find_Peak(ai_4_data)
peaks_val = [ai_4_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_4_data, color='red')
plt.plot(peaks_time_stamp, peaks_val, "^", color='orange', linewidth=2, markersize=10)

peaks, _ = Find_Peak(ai_5_data)
peaks_val = [ai_5_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_5_data, color='maroon')
plt.plot(peaks_time_stamp, peaks_val, ">", color='coral', linewidth=2, markersize=10)

peaks, _ = Find_Peak(ai_6_data)
peaks_val = [ai_6_data[i] for i in peaks]
peaks_time_stamp = [time_tick[i] for i in peaks]
plt.plot(time_tick, ai_6_data, color='indigo')
plt.plot(peaks_time_stamp, peaks_val, ">", color='purple', linewidth=2, markersize=10)

for i in event_time_stamp:
    plt.axvline(x=i, color='olive')
for i in camera_start_time_stamp:
    plt.axvline(x=i/ai_sample_rate, color='teal')
for i in camera_end_time_stamp:
    plt.axvline(x=i/ai_sample_rate, color='black')
plt.show()