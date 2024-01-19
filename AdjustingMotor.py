import threading
from subprocess import Popen
from simple_pid import PID
import time
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Net import *
import pypylon.pylon as py
import numpy as np
import cv2

def onVoltageChange(self, voltage):
    # print("\nVoltage: " + str(voltage))
    # PID control with update handler
    PID_Control()
    return

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
def DisplayGrid(Image, x, y, Width, Height, TargetCoord):
    Array = Image
    for i in range(0, Height + 1, 20):
        Array[y + i][x:x + Width] = np.full((1, Width), 70)
    for i in range(0, Width + 1, 20):
        for j in range(Height):
            Array[y + j][x + i] = 70
    Array[y + (TargetCoord[1] - 1) * 20 + 1][(x + ((TargetCoord[0] - 1) * 20) + 1):(x + (TargetCoord[0] * 20) + 1)] = np.full((1, 20), 150)
    Array[y + TargetCoord[1] * 20 + 1][(x + ((TargetCoord[0]-1) * 20) + 1):(x + (TargetCoord[0] * 20) + 1)] = np.full((1, 20), 150)
    for i in range(20):
        Array[y + (TargetCoord[1] - 1) * 20 + i][(x + ((TargetCoord[0] - 1) * 20) + 1)] = 150
    for i in range(20):
        Array[y + (TargetCoord[1] - 1) * 20 + i][(x + ((TargetCoord[0]) * 20) + 1)] = 150
    return Array
def ViewFly():
    global camera2
    global camera4
    global camera5
    wait_time = 5000
    camera2.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera4.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    camera6.StartGrabbing(py.GrabStrategy_LatestImageOnly)
    while not stopCam:
        try:
            grabResult2 = camera2.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult4 = camera4.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)
            grabResult6 = camera6.RetrieveResult(wait_time, py.TimeoutHandling_ThrowException)

            if grabResult2.GrabSucceeded() and grabResult4.GrabSucceeded() and grabResult6.GrabSucceeded():
                Image = grabResult2.Array
                Target_coord = (5, 8)
                Image = DisplayGrid(Image, 280, 140, 260, 260, Target_coord)
                cv2.imshow("Front", Image)
                cv2.waitKey(1)
                Image = grabResult4.Array
                Target_coord = (10, 10)
                Image = DisplayGrid(Image, 210, 100, 400, 400, Target_coord)
                cv2.imshow("Bottom", Image)
                cv2.waitKey(1)
                Image = grabResult6.Array
                Target_coord = (17, 12)
                Image = DisplayGrid(Image, 120, 80, 600, 360, Target_coord)
                cv2.imshow("Left Side", Image)
                cv2.waitKey(1)

            grabResult2.Release()
            grabResult4.Release()
            grabResult6.Release()
        except py.TimeoutException as e:
            camera2.Close()
            camera4.Close()
            camera6.Close()
            print(f"Timeout exception: {e}")
            break
    camera2.StopGrabbing()
    camera4.StopGrabbing()
    camera6.StopGrabbing()
    camera2.Close()
    camera4.Close()
    camera6.Close()

Video_Saving_time = 1.8


Current_target_position = 1
last_voltage = 0
max_duty_cycle = 1
deadband = 0.01

stopCam = False
dcMotor0 = DCMotor()
voltageInput0 = VoltageInput()

dcMotor0.openWaitForAttachment(5000)
dcMotor0.setDataRate(125)

voltageInput0.openWaitForAttachment(5000)
voltageInput0.setOnVoltageChangeHandler(onVoltageChange)
voltageInput0.setChannel(0)
voltageInput0.setDataRate(125)


FPS = 100
ExposureTime = ((1/FPS)*1000000) - 5000
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


camera2 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[1]))
camera2.Open()
camera2.Width.SetValue(camera2.Width.GetMax())
camera2.Height.SetValue(camera2.Height.GetMax())
camera2.ExposureTime = ExposureTime
camera2.AcquisitionFrameRate = FPS
camera2.LineSelector = "Line4"
camera2.LineMode = "Output"
camera2.LineInverter = False
camera2.LineSource = "ExposureActive"
camera2.Gain = camera2.Gain.Max
camera2.MaxNumBuffer = 100


camera4 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[3]))
camera4.Open()
camera4.Width.SetValue(camera4.Width.GetMax())
camera4.Height.SetValue(camera4.Height.GetMax())
camera4.ExposureTime = ExposureTime
camera4.AcquisitionFrameRate = FPS
camera4.LineSelector = "Line4"
camera4.LineMode = "Output"
camera4.LineInverter = False
camera4.LineSource = "ExposureActive"
camera4.Gain = camera4.Gain.Max
camera4.MaxNumBuffer = 100


camera6 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[5]))
camera6.Open()
camera6.Width.SetValue(camera6.Width.GetMax())
camera6.Height.SetValue(camera6.Height.GetMax())
camera6.ExposureTime = ExposureTime
camera6.AcquisitionFrameRate = FPS
camera6.LineSelector = "Line4"
camera6.LineMode = "Output"
camera6.LineInverter = False
camera6.LineSource = "ExposureActive"
camera6.Gain = camera6.Gain.Max
camera6.MaxNumBuffer = 100

# Send_signal_process = Popen(['python', 'subprocess_daq_trigger.py', str(FPS)])

ViewThread = threading.Thread(target=ViewFly)
ViewThread.start()
time.sleep(1)
Target = ""

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
                if (abs(dcMotor0.getVelocity()) < 0.01 and abs(Current_target_position - voltageInput0.getVoltage()) < deadband) or (time.perf_counter() - start_time) > 2:
                    Target = input("Please enter a position (0~5000): ")
                    break

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
    dcMotor0.setTargetVelocity(0)
    dcMotor0.close()
    voltageInput0.close()
    stopCam = True
    ViewThread.join()
cv2.destroyAllWindows()
camera2.Close()
camera4.Close()
camera6.Close()

