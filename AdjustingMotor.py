import json
import threading
from subprocess import Popen
from simple_pid import PID
import time
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
import pypylon.pylon as py
import numpy as np
import cv2
import subprocess
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def onVoltageChange(self, voltage):
    # print("\nVoltage: " + str(voltage))
    # PID control with update handler
    PID_Control()
    return
def PID_Control():
    global last_voltage

    pid = PID(0.5, 1, 0.3, Current_target_position)
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
def ViewFly():
    global camera1
    global camera2
    global camera3
    global camera4
    global camera5
    global camera6
    global SideViewX
    global SideViewY
    global FrontViewX
    global FrontViewY
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

                TargetCoord = [FrontViewX, FrontViewY]
                TargetCoord1 = [FrontViewX - 1, FrontViewY]
                TargetCoord2 = [FrontViewX - 2, FrontViewY]
                TargetCoord3 = [FrontViewX - 3, FrontViewY]
                TargetCoord4 = [FrontViewX - 4, FrontViewY]
                Image4 = grabResult4.Array
                Image4 = DisplayGrid(Image4, 300, 120, 200, 380, TargetCoord)
                Image4 = DisplayGrid(Image4, 300, 120, 200, 380, TargetCoord1)
                Image4 = DisplayGrid(Image4, 300, 120, 200, 380, TargetCoord2)
                Image4 = DisplayGrid(Image4, 300, 120, 200, 380, TargetCoord3)
                Image4 = DisplayGrid(Image4, 300, 120, 200, 380, TargetCoord4)

                Draw_boundary(Image4)

                TargetCoord = [SideViewX, SideViewY]
                TargetCoord1 = [SideViewX + 1, SideViewY]
                TargetCoord2 = [SideViewX + 2, SideViewY]
                TargetCoord3 = [SideViewX - 1, SideViewY]
                TargetCoord4 = [SideViewX - 2, SideViewY]
                Image6 = grabResult6.Array
                Image6 = DisplayGrid(Image6, 180, 140, 440, 260, TargetCoord)
                Image6 = DisplayGrid(Image6, 180, 140, 440, 260, TargetCoord1)
                Image6 = DisplayGrid(Image6, 180, 140, 440, 260, TargetCoord2)
                Image6 = DisplayGrid(Image6, 180, 140, 440, 260, TargetCoord3)
                Image6 = DisplayGrid(Image6, 180, 140, 440, 260, TargetCoord4)
                Draw_boundary(Image6)

                Image5 = grabResult5.Array
                Combined_images_1 = cv2.hconcat([Image6, Image4])
                # Combined_images_2 = cv2.hconcat([Image5, Image4])


                #Combined_image = cv2.vconcat([Combined_images_1, Combined_images_2])
                # Combined_images_1 = cv2.resize(Combined_images_1, (1300, 550))
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
"""
Initialize the camera acquisition setting
"""
def InitializeCamera(Device, ExposureTime, sharpness, noise_reduction_value, Buffer):
    print("Camera: " + str(Device.GetSerialNumber()))
    Camera = py.InstantCamera(py.TlFactory.GetInstance().CreateDevice(Device))
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

SideViewX = 11
SideViewY = 9
FrontViewX = 5
FrontViewY = 12


# Set the camera acquisition setting
FPS = 40
ExposureTime = 5000
noise_reduction_value = 1  # Noise reduction
Buffer = 300  # Recording buffer
sharpness = 3  # Sharpness
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

# Camera 7 initialization
# camera7 = InitializeCamera(devices[6], ExposureTime=ExposureTime, sharpness=sharpness, noise_reduction_value=noise_reduction_value, Buffer=Buffer)

Continuous_recording = 1
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
        trigger_command(Send_signal_process, "StartSendingSignal")
        while True:
            if Target.lower() == 'n':
                break
            elif float(Target) > 4500 or float(Target) < 500:
                print("Please enter a valid value")
            else:
                Current_target_position = float(Target) / 1000
            start_time = time.perf_counter()
            while True:
                if (abs(dcMotor0.getVelocity()) < 0.01 and abs(
                        Current_target_position - voltageInput0.getVoltage()) < deadband) or (
                        time.perf_counter() - start_time) > 3:
                    Current_target_position = voltageInput0.getVoltage()
                    dcMotor0.setTargetVelocity(0)
                    Target = input("Please enter a position (0~5000): ")
                    break
        print("Stop adjusting")
        trigger_command(Send_signal_process, "StopSendingSignal")
        stopCam = True
        dcMotor0.setTargetVelocity(0)
        voltageInput0.close()
        dcMotor0.close()
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
