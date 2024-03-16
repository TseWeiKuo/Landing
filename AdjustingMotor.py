import threading
from subprocess import Popen
from simple_pid import PID
import time
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
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

                TargetCoord = [12, 10]
                Image1 = grabResult1.Array
                Image1 = DisplayGrid(Image1, 220, 120, 400, 400, TargetCoord)
                Draw_boundary(Image1)

                TargetCoord = [6, 9]
                Image2 = grabResult2.Array
                Image2 = DisplayGrid(Image2, 275, 130, 280, 280, TargetCoord)
                Draw_boundary(Image2)

                TargetCoord = [2, 2]
                Image3 = grabResult3.Array
                Image3 = DisplayGrid(Image3, 220, 120, 400, 400, TargetCoord)
                Draw_boundary(Image3)

                TargetCoord = [4, 8]
                Image4 = grabResult4.Array
                Image4 = DisplayGrid(Image4, 320, 130, 200, 380, TargetCoord)
                Draw_boundary(Image4)

                TargetCoord = [12, 9]
                Image5 = grabResult5.Array
                Image5 = DisplayGrid(Image5, 140, 180, 520, 280, TargetCoord)
                Draw_boundary(Image5)

                TargetCoord = [17, 9]
                Image6 = grabResult6.Array
                Image6 = DisplayGrid(Image6, 150, 180, 520, 280, TargetCoord)
                Draw_boundary(Image6)


                Combined_images_1 = cv2.hconcat([Image6, Image4])
                Combined_images_2 = cv2.hconcat([Image5, Image4])


                #Combined_image = cv2.vconcat([Combined_images_1, Combined_images_2])
                Combined_images_1 = cv2.resize(Combined_images_1, (1600, 600))
                cv2.imshow("All views", Combined_images_1)
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

FPS = 100
ExposureTime = ((1/FPS)*1000000) - 7000
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
camera1.AcquisitionFrameRate = FPS
camera1.LineSelector = "Line4"
camera1.LineMode = "Output"
camera1.LineInverter = False
camera1.LineSource = "ExposureActive"
camera1.Gain = camera1.Gain.Max
camera1.MaxNumBuffer = 100


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


camera3 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[2]))
camera3.Open()
camera3.Width.SetValue(camera3.Width.GetMax())
camera3.Height.SetValue(camera3.Height.GetMax())
camera3.ExposureTime = ExposureTime
camera3.AcquisitionFrameRate = FPS
camera3.LineSelector = "Line4"
camera3.LineMode = "Output"
camera3.LineInverter = False
camera3.LineSource = "ExposureActive"
camera3.Gain = camera3.Gain.Max
camera3.MaxNumBuffer = 100


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


camera5 = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(devices[4]))
camera5.Open()
camera5.Width.SetValue(camera5.Width.GetMax())
camera5.Height.SetValue(camera5.Height.GetMax())
camera5.ExposureTime = ExposureTime
camera5.AcquisitionFrameRate = FPS
camera5.LineSelector = "Line4"
camera5.LineMode = "Output"
camera5.LineInverter = False
camera5.LineSource = "ExposureActive"
camera5.Gain = camera5.Gain.Max
camera5.MaxNumBuffer = 100


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
