import pypylon.pylon as py
from pypylon import genicam
import numpy as np
import time
from matplotlib import pyplot as plt
from Project3Dto2D import ConfigurationEventPrinter
from cameraeventprinter import CameraEventPrinter
from imageio import get_writer
from subprocess import Popen
import subprocess
import os
import concurrent.futures
import datetime
import scipy
import pandas as pd
import json
import csv
import threading
import nidaqmx.system
from nidaqmx.constants import (AcquisitionType, CountDirection, Edge, READ_ALL_AVAILABLE, TaskMode,
                               TriggerType, WAIT_INFINITELY, TerminalConfiguration)
def save_video(cam_img):
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
def Find_Peak(ai_data):
    return scipy.signal.find_peaks(ai_data, distance=95, prominence=[3, 5])
def CountFrames (Frames_Per_Second, Motor_Extend_time, Motor_Retract_time, Platform_stop_duration):
    return (Motor_Extend_time + Motor_Retract_time + Platform_stop_duration) * Frames_Per_Second

# Example handler for camera events.
class SampleCameraEventHandler(py.CameraEventHandler):
    # Only very short processing tasks should be performed by this method. Otherwise, the event notification will block the
    # processing of images.
    def OnCameraEvent(self, camera, userProvidedId, node):
        print("Exposure End event. FrameID: ", camera.EventExposureEndFrameID.Value, " Timestamp: ",
                  camera.EventExposureEndTimestamp.Value)
            # More events can be added here.


# Example of an image event handler.
class SampleImageEventHandler(py.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        print("CSampleImageEventHandler.OnImageGrabbed called.")
        print()
        print()


Data_Folder_Path = r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\DataFolder"
Experiment = "Test Acquisition"
Group_name = "EventStartTrigger"
MetaData_csv_file = ""
Fly_num = ""
save_date = ""
Date = datetime.datetime.now().date()



save_folder = os.path.join(Data_Folder_Path, Experiment)
if Experiment not in os.listdir(Data_Folder_Path):
    os.mkdir(save_folder)
os.chdir(save_folder)

Group_Folder = os.path.join(save_folder, Group_name)
if Group_name not in os.listdir(save_folder):
    os.mkdir(Group_Folder)
os.chdir(Group_Folder)

Date_Folder = os.path.join(Group_Folder, str(Date))
if str(Date) not in os.listdir(Group_Folder):
    os.mkdir(Date_Folder)
os.chdir(Date_Folder)

Fly_num = "Fly_" + str(len([dirs for dirs in os.listdir(Date_Folder) if os.path.isdir(dirs)]) + 1)
Fly_Folder = os.path.join(Date_Folder, Fly_num)
os.mkdir(Fly_Folder)
os.chdir(Fly_Folder)

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

FPS = 200
eMyExposureEndEvent = 100
stop_daq = False
daq_start_time = 0
ai_6_data = []
ai_5_data = []
ai_4_data = []
ai_3_data = []
ai_2_data = []
ai_1_data = []
ai_sample_rate = FPS * 100


T = 0
ExposureTime = 500
noise_reduction_value = 1
sharpness = 2
Cropped = False
print(f"ExposureTime: {ExposureTime} us")



tlFactory = py.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()
print("Camera 1: " + str(devices[0].GetSerialNumber()))
print("Camera 2: " + str(devices[1].GetSerialNumber()))
print("Camera 3: " + str(devices[2].GetSerialNumber()))
print("Camera 4: " + str(devices[3].GetSerialNumber()))
print("Camera 5: " + str(devices[4].GetSerialNumber()))
print("Camera 6: " + str(devices[5].GetSerialNumber()))
if Cropped:
    camera1 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[0]))
    camera1.Open()
    camera1.Width.SetValue(640)
    camera1.Height.SetValue(550)
    camera1.OffsetX = 128
    camera1.OffsetY = 43
    camera1.PgiMode.Value = "On"
    camera1.NoiseReduction.Value = noise_reduction_value
    camera1.SensorReadoutMode.Value = "Fast"
    camera1.SharpnessEnhancement.Value = sharpness
    camera1.ExposureTime = ExposureTime
    camera1.LineSelector = "Line4"
    camera1.LineMode = "Output"
    camera1.LineInverter = False
    camera1.LineSource = "FrameTriggerWait"
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
    camera2.Width.SetValue(640)
    camera2.Height.SetValue(550)
    camera2.OffsetX = 112
    camera2.OffsetY = 43
    camera2.PgiMode.Value = "On"
    camera2.NoiseReduction.Value = noise_reduction_value
    camera2.SharpnessEnhancement.Value = sharpness
    camera2.SensorReadoutMode.Value = "Fast"
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
    camera3.Width.SetValue(640)
    camera3.Height.SetValue(550)
    camera3.OffsetX = 128
    camera3.OffsetY = 43
    camera3.PgiMode.Value = "On"
    camera3.NoiseReduction.Value = noise_reduction_value
    camera3.SharpnessEnhancement.Value = sharpness
    camera3.SensorReadoutMode.Value = "Fast"
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
    camera4.Width.SetValue(640)
    camera4.Height.SetValue(550)
    camera4.OffsetX = 96
    camera4.OffsetY = 43
    camera4.PgiMode.Value = "On"
    camera4.NoiseReduction.Value = noise_reduction_value
    camera4.SharpnessEnhancement.Value = sharpness
    camera4.SensorReadoutMode.Value = "Fast"
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
    camera5.Width.SetValue(640)
    camera5.Height.SetValue(550)
    camera5.OffsetX = 96
    camera5.OffsetY = 43
    camera5.PgiMode.Value = "On"
    camera5.NoiseReduction.Value = noise_reduction_value
    camera5.SharpnessEnhancement.Value = sharpness
    camera5.SensorReadoutMode.Value = "Fast"
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
    camera6.Width.SetValue(640)
    camera6.Height.SetValue(550)
    camera6.OffsetX = 128
    camera6.OffsetY = 43
    camera6.PgiMode.Value = "On"
    camera6.NoiseReduction.Value = noise_reduction_value
    camera6.SharpnessEnhancement.Value = sharpness
    camera6.SensorReadoutMode.Value = "Fast"
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
else:
    camera1 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[0]))
    camera1.Open()
    camera1.Width.SetValue(camera1.Width.GetMax())
    camera1.Height.SetValue(camera1.Height.GetMax())
    camera1.PgiMode.Value = "On"
    camera1.NoiseReduction.Value = noise_reduction_value
    camera1.SharpnessEnhancement.Value = sharpness
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
    camera2.PgiMode.Value = "On"
    camera2.NoiseReduction.Value = noise_reduction_value
    camera2.SharpnessEnhancement.Value = sharpness
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
    camera3.PgiMode.Value = "On"
    camera3.NoiseReduction.Value = noise_reduction_value
    camera3.SharpnessEnhancement.Value = sharpness
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
    camera4.PgiMode.Value = "On"
    camera4.NoiseReduction.Value = noise_reduction_value
    camera4.SharpnessEnhancement.Value = sharpness
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
    camera5.PgiMode.Value = "On"
    camera5.NoiseReduction.Value = noise_reduction_value
    camera5.SharpnessEnhancement.Value = sharpness
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
    camera6.PgiMode.Value = "On"
    camera6.NoiseReduction.Value = noise_reduction_value
    camera6.SharpnessEnhancement.Value = sharpness
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
    camera6.EventSelector.Value = "ExposureEnd"
    camera6.EventNotification.Value = "On"
    camera6.TriggerActivation = "RisingEdge"
    camera6.TriggerDelay = 0

    # Create an example event handler. In the present case, we use one single camera handler for handling multiple camera events.
    # The handler prints a message for each received event.
    handler1 = SampleCameraEventHandler()

    # Create another more generic event handler printing out information about the node for which an event callback
    # is fired.
    handler2 = CameraEventPrinter()
    # Register the standard configuration event handler for enabling software triggering.
    # The software trigger configuration handler replaces the default configuration
    # as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
    camera6.RegisterConfiguration(py.SoftwareTriggerConfiguration(), py.RegistrationMode_ReplaceAll,
                                 py.Cleanup_Delete)

    # For demonstration purposes only, add sample configuration event handlers to print out information
    # about camera use and image grabbing.
    camera6.RegisterConfiguration(ConfigurationEventPrinter(), py.RegistrationMode_Append,
                                 py.Cleanup_Delete)  # Camera use.

    # For demonstration purposes only, register another image event handler.
    camera6.RegisterImageEventHandler(SampleImageEventHandler(), py.RegistrationMode_Append, py.Cleanup_Delete)

    # Camera event processing must be activated first, the default is off.
    # camera6.GrabCameraEvents.SetValue(True)

    # Register an event handler for the Exposure End event. For each event type, there is a "data" node
    # representing the event. The actual data that is carried by the event is held by child nodes of the
    # data node. In the case of the Exposure End event, the child nodes are EventExposureEndFrameID and EventExposureEndTimestamp.
    # The CSampleCameraEventHandler demonstrates how to access the child nodes within
    # a callback that is fired for the parent data node.
    # The user-provided ID eMyExposureEndEvent can be used to distinguish between multiple events (not shown).
    camera6.RegisterCameraEventHandler(handler1, "EventExposureEndData", eMyExposureEndEvent,
                                      py.RegistrationMode_ReplaceAll, py.Cleanup_None)

    # The handler is registered for both, the EventExposureEndFrameID and the EventExposureEndTimestamp
    # node. These nodes represent the data carried by the Exposure End event.
    # For each Exposure End event received, the handler will be called twice, once for the frame ID, and
    # once for the time stamp.
    camera6.RegisterCameraEventHandler(handler2, "EventExposureEndFrameID", eMyExposureEndEvent,
                                      py.RegistrationMode_Append, py.Cleanup_None)
    camera6.RegisterCameraEventHandler(handler2, "EventExposureEndTimestamp", eMyExposureEndEvent,
                                      py.RegistrationMode_Append, py.Cleanup_None)

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


frames_to_grab = 200
os.chdir(r"C:\Users\agrawal-admin\OneDrive - Virginia Tech\Desktop\Agrawal_Lab")
# Launch the subprocess
Send_signal_process = Popen(['python', 'SendAO.py', str(FPS)], stdin=subprocess.PIPE, text=True)
time.sleep(5)
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

    while images_grabbed < frames_to_grab:
        try:
            print(images_grabbed)
            grabResult1 = camera1.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult2 = camera2.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult3 = camera3.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult4 = camera4.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult5 = camera5.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult6 = camera6.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)

            if grabResult1.GrabSucceeded() and grabResult2.GrabSucceeded() and grabResult3.GrabSucceeded()\
                    and grabResult4.GrabSucceeded() and grabResult5.GrabSucceeded() and grabResult6.GrabSucceeded():
                images_grabbed += 1
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
    # Stop the camera
    camera1.StopGrabbing()
    camera2.StopGrabbing()
    camera3.StopGrabbing()
    camera4.StopGrabbing()
    camera5.StopGrabbing()
    camera6.StopGrabbing()

    T += 1
    print(f"Trial {T}")
    tm = str(datetime.datetime.now().time())
    tm = tm.replace(":", "-")[:-4]
    Date_and_time_of_exp = str(datetime.datetime.now().date()) + "-" + tm
    filename = Date_and_time_of_exp + "_" + Group_name + "_" + Fly_num + "_Trial_" + str(T)
    cam_imgs = [['_Cam1', camera1_videos_seg], ['_Cam2', camera2_videos_seg], ['_Cam3', camera3_videos_seg],
                ['_Cam4', camera4_videos_seg], ['_Cam5', camera5_videos_seg], ['_Cam6', camera6_videos_seg]]
    video_saving_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(save_video, cam_imgs)
    print("Air puff time!")

    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()
    Send_signal_process.stdin.close()
except KeyboardInterrupt as k:
    print(f"Key board interrupt: {k}")
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()

    while Send_signal_process.poll() != 0:
        continue
    Send_signal_process.kill()
    Send_signal_process.wait()


while Send_signal_process.poll() != 0:
    continue
Send_signal_process.kill()
Send_signal_process.wait()


