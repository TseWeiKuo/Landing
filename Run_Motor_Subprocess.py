from simple_pid import PID
import sys
import time
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *


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


# Access arguments using sys.argv
script_name = sys.argv[0]
Target_V = float(sys.argv[1])
Initial_V = int(sys.argv[2])
Trial_num = int(sys.argv[3])
Platform_stop_duration = int(sys.argv[4])
inter_trial_wait_time = int(sys.argv[5])
Video_Saving_time = 1.8


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

time.sleep(2)
try:
    try:
        # time.sleep(1)
        for i in range(Trial_num):
            video_start_time = time.perf_counter()
            start_time = time.perf_counter()
            while True:
                Current_target_position = Target_V
                if (abs(dcMotor0.getVelocity()) < 0.01 and abs(Current_target_position - voltageInput0.getVoltage()) < deadband) or (time.perf_counter() - start_time) > 2:
                    dcMotor0.setTargetVelocity(0)
                    time.sleep(Platform_stop_duration)
                    Retract_time_start = time.perf_counter()
                    Retract = True
                    Current_target_position = Initial_V
                    # Retract back to start position
                    while Retract:
                        if abs(dcMotor0.getVelocity()) < 0.01 and (abs(voltageInput0.getVoltage() - Current_target_position) < deadband) or (time.perf_counter() - Retract_time_start) > 2:
                            dcMotor0.setTargetVelocity(0)
                            print(f"Video duration {time.perf_counter() - video_start_time}")
                            Retract = False
                            start_time = time.perf_counter()
                    break
            if (i + 1) < Trial_num:
                time.sleep(inter_trial_wait_time)
        dcMotor0.setTargetVelocity(0)
        voltageInput0.close()
        dcMotor0.close()
    except PhidgetException:
        print("Channels closed")
        dcMotor0.setTargetVelocity(0)
        dcMotor0.close()
        voltageInput0.close()
except KeyboardInterrupt as k:
    print("Channels closed")
    dcMotor0.setTargetVelocity(0)
    dcMotor0.close()
    voltageInput0.close()
print("Motor subprocess ends")
dcMotor0.close()
voltageInput0.close()


