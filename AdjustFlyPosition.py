import threading
from subprocess import Popen
from simple_pid import PID
import time
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
import pypylon.pylon as py
import numpy as np
import cv2
import json

import subprocess

def onVoltageChange(self, voltage):
    # print("\nVoltage: " + str(voltage))
    # PID control with update handler
    PID_Control()
    return
def trigger_command(subprocess_instance, command):
    try:
        if subprocess_instance.poll() is None:
            subprocess_instance.stdin.write(command + '\n')
            subprocess_instance.stdin.flush()
            # print("Sent command:", command)
        else:
            print("Subprocess has terminated with return code:", subprocess_instance.returncode)
            out, err = subprocess_instance.communicate()
            if out:
                print("Subprocess output:", out)
            if err:
                print("Subprocess error:", err)
    except IOError as e:
        print(f"Error writing to subprocess: {e}")
def PID_Control():
    global last_voltage

    pid = PID(0.55, 1, 0.2, Current_target_position)
    output = pid(last_voltage)
    # print(f"Target voltage: {Current_target_position} Current voltage: {voltageInput0.getVoltage()} Current output: {dcMotor0.getVelocity()}")
    if output >= max_duty_cycle:
        output = max_duty_cycle
    elif output <= -max_duty_cycle:
        output = -max_duty_cycle
    dcMotor0.setTargetVelocity(output)
    last_voltage = voltageInput0.getVoltage()

def Draw_boundary(Image):
    for i in range(np.shape(Image)[0]):
        Image[i][0] = 70
        Image[i][np.shape(Image)[1] - 1] = 70
    Image[0][0:np.shape(Image)[1]] = np.full((1, np.shape(Image)[1]), 70)
    Image[np.shape(Image)[0] - 1][0:np.shape(Image)[1]] = np.full((1, np.shape(Image)[1]), 70)
def DisplayGrid(Image, x, y, Width, Height, TargetCoord):
    Array = Image
    for i in range(0, Height + 1, 20):
        Array[y + i][x:x + Width] = np.full((1, Width), 70)
    for i in range(0, Width + 1, 20):
        for j in range(Height):
            Array[y + j][x + i] = 70
    Array[y + (TargetCoord[1] - 1) * 20 + 1][(x + ((TargetCoord[0] - 1) * 20) + 1):(x + (TargetCoord[0] * 20) + 1)] = np.full((1, 20), 200)
    Array[y + TargetCoord[1] * 20 + 1][(x + ((TargetCoord[0]-1) * 20) + 1):(x + (TargetCoord[0] * 20) + 1)] = np.full((1, 20), 200)
    for i in range(20):
        Array[y + (TargetCoord[1] - 1) * 20 + i][(x + ((TargetCoord[0] - 1) * 20) + 1)] = 200
    for i in range(20):
        Array[y + (TargetCoord[1] - 1) * 20 + i][(x + ((TargetCoord[0]) * 20) + 1)] = 200
    return Array

def ViewFly():
    global camera1
    global camera2
    global camera3
    global camera4
    global camera5
    global camera6
    wait_time = 5000
    camera1.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera2.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera3.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera4.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera5.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera6.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    while not stopCam:
        try:
            grabResult1 = camera1.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult2 = camera2.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult3 = camera3.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult4 = camera4.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult5 = camera5.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult6 = camera6.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)

            if grabResult1.GrabSucceeded() and grabResult2.GrabSucceeded() and grabResult3.GrabSucceeded() and \
                    grabResult4.GrabSucceeded() and grabResult5.GrabSucceeded() and grabResult6.GrabSucceeded():

                Image1 = grabResult1.Array
                Image2 = grabResult2.Array
                Image3 = grabResult3.Array
                Image4 = grabResult4.Array
                Image5 = grabResult5.Array
                Image6 = grabResult6.Array
                Combined_images_1 = cv2.hconcat([Image6, Image1, Image2])
                Combined_images_2 = cv2.hconcat([Image5, Image3, Image4])


                Combined_image = cv2.vconcat([Combined_images_1, Combined_images_2])
                Combined_image = cv2.resize(Combined_image, (1800, 900))
                cv2.imshow("All views", Combined_image)
                cv2.waitKey(1)

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
    camera1.StopGrabbing()
    camera2.StopGrabbing()
    camera3.StopGrabbing()
    camera4.StopGrabbing()
    camera5.StopGrabbing()
    camera6.StopGrabbing()
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()

FPS = 40
ExposureTime = 2000
noise_reduction_value = 1.2
sharpness = 3
Continuous_recording = 1
Cropped = False
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

if Cropped:
    camera1 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[0]))
    camera1.Open()
    camera1.Width.SetValue(640)
    camera1.Height.SetValue(550)
    camera1.OffsetX = 160
    camera1.OffsetY = 6
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
    camera2.Width.SetValue(640)
    camera2.Height.SetValue(550)
    camera2.OffsetX = 96
    camera2.OffsetY = 60
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
    camera3.Width.SetValue(640)
    camera3.Height.SetValue(550)
    camera3.OffsetX = 64
    camera3.OffsetY = 45
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
    camera4.Width.SetValue(640)
    camera4.Height.SetValue(550)
    camera4.OffsetX = 128
    camera4.OffsetY = 43
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
    camera5.Width.SetValue(640)
    camera5.Height.SetValue(550)
    camera5.OffsetX = 80
    camera5.OffsetY = 60
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
    camera6.Width.SetValue(640)
    camera6.Height.SetValue(550)
    camera6.OffsetX = 128
    camera6.OffsetY = 43
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

placeholder_list = []
Send_signal_process = Popen(['python', 'subprocess_daq_trigger.py', str(FPS), str(20), str(Continuous_recording), json.dumps(placeholder_list)], stdin=subprocess.PIPE, text=True)
stopCam = False
ViewThread = threading.Thread(target=ViewFly)
ViewThread.start()

Current_target_position = 1
last_voltage = 0
max_duty_cycle = 1
deadband = 0.01

dcMotor0 = DCMotor()
voltageInput0 = VoltageInput()

dcMotor0.openWaitForAttachment(5000)
dcMotor0.setDataRate(125)

voltageInput0.openWaitForAttachment(5000)
voltageInput0.setOnVoltageChangeHandler(onVoltageChange)
voltageInput0.setChannel(0)
voltageInput0.setDataRate(125)


try:
    try:
        Target = input("Please enter a position (0~5000): ")
        while True:
            if Target.lower() == 'n':
                break
            elif float(Target) > 5000 or float(Target) < 0:
                print("Please enter a valid value")
            else:
                Current_target_position = float(Target) / 1000
            start_time = time.perf_counter()
            while True:
                if (abs(dcMotor0.getVelocity()) < 0.01 and abs(
                        Current_target_position - voltageInput0.getVoltage()) < deadband) or (
                        time.perf_counter() - start_time) > 2:
                    Target = input("Please enter a position (0~5000): ")
                    break
        print("Stop adjusting")
        trigger_command(Send_signal_process, "StopSendingSignal")
        dcMotor0.setTargetVelocity(0)
        voltageInput0.close()
        dcMotor0.close()
        stopCam = True
        ViewThread.join()
    except PhidgetException:
        print("Channels closed")
        dcMotor0.setTargetVelocity(0)
        dcMotor0.close()
        voltageInput0.close()
        stopCam = True
        ViewThread.join()
except KeyboardInterrupt as k:
    print("Channels closed")
    stopCam = True
    ViewThread.join()
    cv2.destroyAllWindows()
    camera1.Close()
    camera2.Close()
    camera3.Close()
    camera4.Close()
    camera5.Close()
    camera6.Close()

cv2.destroyAllWindows()
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