# Import necessary package
from simple_pid import PID
import time
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import pandas as pd
import numpy as np
import json

def onVoltageChange(self, voltage):
    # print("\nVoltage: " + str(voltage))
    # PID control with update handler
    PID_Control()
    return
def PID_Control():
    global last_voltage
    global Record_trace
    global Voltage_trial_trace
    global Voltage_trace_trial_time_stamp
    global Parent_reference_time_stamp
    pid = PID(0.5, 1, 0.3, Current_target_position)
    output = pid(last_voltage)

    if Record_trace:
        Voltage_trace_trial_time_stamp.append(time.perf_counter())
        Voltage_trial_trace.append(voltageInput0.getVoltage())
    # print(f"Target voltage: {Current_target_position} Current voltage: {voltageInput0.getVoltage()} Current output: {dcMotor0.getVelocity()}")
    if output >= max_duty_cycle:
        output = max_duty_cycle
    elif output <= -max_duty_cycle:
        output = -max_duty_cycle
    dcMotor0.setTargetVelocity(output)
    last_voltage = voltageInput0.getVoltage()
def SaveMotorMetadata(MotorTrace, TimeStamp, meta_data_file):
    data_to_record = dict()
    trace_length = []
    for i in range(len(MotorTrace)):
        trace_length.append(len(MotorTrace[i]))
    max_length = max(trace_length)

    for i in range(len(MotorTrace)):
        data_to_record[f"Trial_{i + 1}_MotorTrace"] = MotorTrace[i] + [np.nan] * (max_length - len(MotorTrace[i]))
        data_to_record[f"Trial_{i + 1}_TraceTimeStamp"] = TimeStamp[i] + [np.nan] * (max_length - len(TimeStamp[i]))

    # Convert the dictionary to pd data frame and save it to the metadata file
    df = pd.DataFrame(data_to_record)
    df.to_csv(meta_data_file, index=False)

# Access arguments using sys.argv
script_name = sys.argv[0]
json_data = sys.argv[1]

# Deserialize the JSON string back into a dictionary
input_data = json.loads(json_data)

# Obtain the metadata file path
Experiment_Meta_data_csv = sys.argv[2]

# The time stamp at main script: RunExperiment.py when motor subprocess was started
Parent_reference_time_stamp = float(sys.argv[3])

# Get parameter to run motor
Target_V = input_data["Target_V"]  # motor stop position
Initial_V = input_data["Initial_V"]  # motor start position
Trial_num = input_data["Trial_Num"]  # Number of trials
Platform_stop_duration = input_data["Platform_stop_time"]  # platform stop duration

# Current position of motor
Current_target_position = 1

# Initialize previous position of motor
last_voltage = 0

# Maximum motor velocity
max_duty_cycle = 0.5

# Room of error as motor approach stop position
deadband = 0.01

# Initialize the motor
dcMotor0 = DCMotor()

# Initialize the potentiometer
voltageInput0 = VoltageInput()

# Open the motor and set the data rate
dcMotor0.openWaitForAttachment(5000)
dcMotor0.setDataRate(125)

# Open the potentiometer
voltageInput0.openWaitForAttachment(5000)

# Set event handler for potentiometer
voltageInput0.setOnVoltageChangeHandler(onVoltageChange)

# Set potentiometer channel and data rate
voltageInput0.setChannel(0)
voltageInput0.setDataRate(125)

# Initialize the voltage trace and time stamp data
Voltage_trace = []
Voltage_trial_trace = []
Voltage_trace_time_stamp = []
Voltage_trace_trial_time_stamp = []

# Boolean to determine when to record motor trace
Record_trace = False

try:
    try:
        print("Motor subprocess ready!")
        t = 0

        # Run the motor for n trials
        while t < Trial_num:

            # Wait for the run motor command from main script
            if sys.stdin.readline().strip() == "RunMotor":

                # Initialize trial motor position and time trace
                Voltage_trial_trace = []
                Voltage_trace_trial_time_stamp = []

                # start recording the motor position trace
                Record_trace = True

                # Get the motor extension start time stamp
                Extend_start_time = time.perf_counter()

                # Start extending the motor
                while True:

                    # Set the target position to designated motor stop position
                    Current_target_position = Target_V

                    # Extend the motor while target distance is not reached and has not reached the 3 seconds limit.
                    if (abs(dcMotor0.getVelocity()) < 0.01 and abs(Current_target_position - voltageInput0.getVoltage()) < deadband) or (time.perf_counter() - Extend_start_time) > 3:

                        # Once the motor reach destination, set velocity to 0
                        dcMotor0.setTargetVelocity(0)

                        # Wait for the designated time
                        time.sleep(Platform_stop_duration[t])

                        # Get the time stamp when the motor start to retract
                        Retract_time_start = time.perf_counter()

                        # Set the retract to true
                        Retract = True

                        # Set the target position back to motor start position
                        Current_target_position = Initial_V

                        # Start retracting
                        while Retract:

                            # Retract the motor while target position is not reached and has not reached the 3 seconds limit.
                            if abs(dcMotor0.getVelocity()) < 0.01 and (abs(voltageInput0.getVoltage() - Current_target_position) < deadband) or (time.perf_counter() - Retract_time_start) > 3:

                                # once reached the target position, set velocity to 0
                                dcMotor0.setTargetVelocity(0)

                                # Set retract to false
                                Retract = False
                        break

                # Record position trace and timestamp
                Voltage_trace.append(Voltage_trial_trace)
                Voltage_trace_time_stamp.append(Voltage_trace_trial_time_stamp)

                # Motor activity has ceased for that trial, stop recording its position
                Record_trace = False
                t += 1

        # One all trials end, set velocity to 0
        dcMotor0.setTargetVelocity(0)

        # Close the potentiometer
        voltageInput0.close()

        # Close the motor
        dcMotor0.close()
    except:
        print("Phidget exception occur")
        print("Channels closed")

        # Set motor velocity to 0
        dcMotor0.setTargetVelocity(0)

        # Close motor
        dcMotor0.close()

        # Close potentiometer
        voltageInput0.close()
# In case of keyboard interrupt
except KeyboardInterrupt as k:
    print("Channels closed")
    # Set motor velocity to 0
    dcMotor0.setTargetVelocity(0)

    # Close motor
    dcMotor0.close()

    # Close potentiometer
    voltageInput0.close()

print("Motor subprocess ends")

# Stop the communication with main script
sys.stdin.close()

# Close motor
dcMotor0.close()

# Close potentiometer
voltageInput0.close()

# Save motor trace to metadata
SaveMotorMetadata(Voltage_trace, Voltage_trace_time_stamp, Experiment_Meta_data_csv)
# add_column_to_csv(Experiment_Meta_data_csv, "MotorTrace", Voltage_trace)
# add_column_to_csv(Experiment_Meta_data_csv, "MotorTimeStamp", Voltage_trace_time_stamp)
