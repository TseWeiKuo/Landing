from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.CurrentInput import *
import time
import json
import matplotlib as plt
import math
def onStateChange(self, state):
	print("\nState: " + str(state))
def onAttach(self):
	print("Attach")
def onDetach(self):
	print("Detach")
def onError(self, code, description):
	print("Code: " + str(code))
	print("Description: " + str(description))
def onPositionChange(self, positionChange, timeChange, indexTriggered):
	print("\n-----------")
	print("PositionChange: " + str(positionChange))
	print("TimeChange: " + str(timeChange))
	print("IndexTriggered: " + str(indexTriggered))
	print("getPosition: " + str(self.getPosition()))
	print("----------\n")
def VelocityChange(self, velocity):
	print("Velocity: " + str(self.getVelocity()))


def onVoltageChange(self, voltage):
	# print("\nVoltage: " + str(voltage))
	# PID control with update handler
	pid(voltage, vgoal)
	return

def pid(vcurr, vgoal):

	global error
	global duty_cycle
	global integral
	global derivative
	global max_duty_cycle

	dt = 0.00001
	errorlast = error
	error = vgoal - vcurr

	# print("Error: " + str(round(error, 3)) + " Duty cycle: " + str(round(duty_cycle,3)) + " Integral: " + str(integral) + " Derivative: " + str(derivative))

	# compute the duty cycle
	if (abs(error) <= deadband and abs(duty_cycle) < 0.01) :
		duty_cycle = 0
		error = 0
	else:
		# print("Kp * error: " + str(Kp*error))
		# print("Ki * integral: " + str(Ki * integral))
		# print("Kd * derivative: " + str(Kd * derivative))
		# print("Duty cycle: " + str(duty_cycle))
		# print("Voltage: " + str(vcurr))
		duty_cycle = (Kp*error) + (Ki*integral) + (Kd * derivative)

	# bound the duty cycle
	if duty_cycle >= max_duty_cycle:
		duty_cycle = max_duty_cycle
		# print("Using max velocity")
	elif duty_cycle <= -max_duty_cycle: # lower limit to keep the duty cycle and motor velocity linear
		duty_cycle = -max_duty_cycle
	else:
		# print("Using calculated velocity")
		integral += (error * dt)
		# print(errorlast)
		derivative = ((error - errorlast)/dt)/5000

	# change the motor speed
	dcMotor0.setTargetVelocity(duty_cycle)


Kp=1 # proportional gain coefficient
Ki=12.5# integral gain coefficient
Kd=0.004# derivative gain coefficient

max_duty_cycle = 0.8
integral=0 # initialize integral
error=0
derivative=0
deadband = 0.01
duty_cycle = 0
vgoal = 1

dcMotor0 = DCMotor()
encoder0 = Encoder()
voltageInput0 = VoltageInput()

# left motor
print("\n--------------------------------------")
print("\nSetting OnAttachHandler...")
dcMotor0.setOnAttachHandler(onAttach)
print("Setting OnDetachHandler...")
dcMotor0.setOnDetachHandler(onDetach)
print("Setting OnErrorHandler...")
dcMotor0.setOnErrorHandler(onError)

# Register for event before calling open...event handler when position changes
# encoder0.setOnPositionChangeHandler(onPositionChange)


voltageInput0.setOnVoltageChangeHandler(onVoltageChange)
voltageInput0.setChannel(0)

dcMotor0.openWaitForAttachment(5000)
encoder0.openWaitForAttachment(5000)
voltageInput0.openWaitForAttachment(5000)

f = open(r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\ImmediatelyAfterStopV.txt", "a")
f1 = open(r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\OneSecDelayV.txt", "a")
f2 = open(r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\OneSecDelayVTrace.txt", "a")
f3 = open(r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\VoltageTrace.txt", "a")
f4 = open(r"C:\Users\agrawal-admin\Desktop\Agrawal_Lab\Duty cycle trace.txt", "a")

Velocity = 0.3
Accuracy = 0.05
target_voltage = [2]
Oscillate = False
ManipulatePos = True
UpperBound = 4.7
LowerBound = 0.3


Accuracy_Table = dict()
OneSecDelay_Table = dict()
OneSecDelayTrace_Table = dict()
VoltageTrace_Table = dict()
Duty_cycle_table = dict()
RecordDriftTraceStart = 0
Trial_num = 15
Minimum_pos = 1
voltageInput0.setDataRate(125)
dcMotor0.setDataRate(125)



if voltageInput0.getVoltage() > UpperBound or voltageInput0.getVoltage() < LowerBound:
	print("At limit")
	start = time.perf_counter()
	while time.perf_counter() - start < 2:
		vgoal = Minimum_pos

try:
	for voltage in target_voltage:
		trial = 0
		Accuracy_Table[str(voltage)] = []
		OneSecDelay_Table[str(voltage)] = []
		OneSecDelayTrace_Table[str(voltage)] = []
		VoltageTrace_Table[str(voltage)] = []
		Duty_cycle_table[str(voltage)] = []
		independent_trace = []
		duty_cycle_trace = []
		start_time = time.perf_counter()
		while True:
			print(voltageInput0.getVoltage())
			vgoal = voltage
			time.sleep(0.001)
			temp = time.perf_counter() - start_time
			independent_trace.append((temp, voltageInput0.getVoltage()))
			duty_cycle_trace.append((temp, dcMotor0.getVelocity()))
			# Target reached
			if (abs(dcMotor0.getVelocity()) < 0.01 and abs(voltage - voltageInput0.getVoltage()) < deadband) or (time.perf_counter() - start_time) > 3:
				trial += 1

				# Accuracy_Table[str(voltage)].append(round(voltageInput0.getVoltage() - voltage, 3))
				dcMotor0.setTargetVelocity(0)
				# print("Target Reached: " + str(voltageInput0.getVoltage()))

				RecordDriftTraceStart = time.perf_counter()
				# DistinctV = []
				# TraceData = []
				while time.perf_counter() - RecordDriftTraceStart < 1:
					independent_trace.append((time.perf_counter() - start_time, voltageInput0.getVoltage()))
					duty_cycle_trace.append((time.perf_counter() - start_time, dcMotor0.getVelocity()))
					time.sleep(0.001)

				VoltageTrace_Table[str(voltage)].append(independent_trace)
				Duty_cycle_table[str(voltage)].append(duty_cycle_trace)
				independent_trace = []
				duty_cycle_trace = []
				# if voltageInput0.getVoltage() not in DistinctV:
				# DistinctV.append(voltageInput0.getVoltage())
				# TraceData.append((time.perf_counter() - RecordDriftTraceStart, voltageInput0.getVoltage()))

				# OneSecDelay_Table[str(voltage)].append(round(voltageInput0.getVoltage() - voltage, 3))
				# OneSecDelayTrace_Table[str(voltage)].append(TraceData)

				Retract_time_start = time.perf_counter()
				Retract = True
				vgoal = Minimum_pos
				# Retract back to start position
				while Retract:
					if abs(dcMotor0.getVelocity()) < 0.01 and abs(voltageInput0.getVoltage() - vgoal) < (deadband * 2) or (time.perf_counter() - Retract_time_start) > 3:
						dcMotor0.setTargetVelocity(0)
						time.sleep(0.5)
						Retract = False
						start_time = time.perf_counter()
			# Limit switch
			if voltageInput0.getVoltage() > UpperBound or voltageInput0.getVoltage() < LowerBound:
				print("Limit switch triggered")
				dcMotor0.setTargetVelocity(0)
				break
			# Trials end
			if trial >= Trial_num:
				break
	# f.write("\n")
	# f1.write("\n")
	# f2.write("\n")
	f3.write("\n")
	f4.write("\n")
	# f1.write(json.dumps(OneSecDelay_Table))
	# f.write(json.dumps(Accuracy_Table))
	# f2.write(json.dumps(OneSecDelayTrace_Table))
	f3.write(json.dumps(VoltageTrace_Table))
	f4.write(json.dumps(Duty_cycle_table))
except KeyboardInterrupt as k:
	print("Channels closed")
	dcMotor0.close()
	encoder0.close()
	voltageInput0.close()
"""
for i in range(len(target_voltage)):
	Accuracy_Table[str(target_voltage[i])] = []
	OneSecDelay_Table[str(target_voltage[i])] = []
	OneSecDelayTrace_Table[str(target_voltage[i])] = []
	t = 0
	AutoRetractTimer = 0
	while True:
		time.sleep(0.0001)
		# Limit switch
		if voltageInput0.getVoltage() > UpperBound or voltageInput0.getVoltage() < LowerBound:
			if voltageInput0.getVoltage() > UpperBound:
				dcMotor0.setTargetVelocity(-Velocity)
			else:
				dcMotor0.setTargetVelocity(Velocity)

		# Target reached
		if target_voltage[i] < voltageInput0.getVoltage():
			dcMotor0.setTargetVelocity(0)
			Accuracy_Table[str(target_voltage[i])].append(round(voltageInput0.getVoltage() - target_voltage[i], 3))

			print("Immediately after stop V: " + str(voltageInput0.getVoltage()))
			RecordDriftTraceStart = time.perf_counter()
			TraceData = []
			DistinctV = []
			while time.perf_counter() - RecordDriftTraceStart < 1:
				if voltageInput0.getVoltage() not in DistinctV:
					DistinctV.append(voltageInput0.getVoltage())
					TraceData.append((time.perf_counter() - RecordDriftTraceStart, voltageInput0.getVoltage()))

			OneSecDelay_Table[str(target_voltage[i])].append(round(voltageInput0.getVoltage() - target_voltage[i], 3))
			OneSecDelayTrace_Table[str(target_voltage[i])].append(TraceData)
			t += 1
			print("1 Sec delay V: " + str(voltageInput0.getVoltage()))

			# Retract to lower bound
			dcMotor0.setTargetVelocity(-Velocity)
			Retract = True
			while Retract:
				if (voltageInput0.getVoltage() - LowerBound) < 0.3:
					dcMotor0.setTargetVelocity(Velocity)
					previous_velocity = Velocity
					Retract = False
			AutoRetractTimer = time.perf_counter()
		else:
			# Extend
			if target_voltage[i] > voltageInput0.getVoltage():
				dcMotor0.setTargetVelocity(Velocity)
			# Retract
			if target_voltage[i] < voltageInput0.getVoltage():
				dcMotor0.setTargetVelocity(-Velocity)
			# Auto retract trigger
			if time.perf_counter() - AutoRetractTimer > 10:
				dcMotor0.setTargetVelocity(-Velocity)
				Retract = True
				while Retract:
					if (voltageInput0.getVoltage() - LowerBound) < 0.3:
						dcMotor0.setTargetVelocity(Velocity)
						previous_velocity = Velocity
						Retract = False
				AutoRetractTimer = time.perf_counter()

		if t >= Trials:
			dcMotor0.setTargetVelocity(0)
			break
	print(Accuracy_Table[str(target_voltage[i])])

print(OneSecDelayTrace_Table)
print(Accuracy_Table)
f.write("\n")
f1.write("\n")
f2.write("\n")
f1.write(json.dumps(OneSecDelay_Table))
f.write(json.dumps(Accuracy_Table))
f2.write(json.dumps(OneSecDelayTrace_Table))
"""
"""
while True:
	if Oscillate:
		if voltageInput0.getVoltage() < LowerBound:
			dcMotor0.setTargetVelocity(0)
			dcMotor0.setTargetVelocity(Velocity)
			Direction = "Extend"
		elif voltageInput0.getVoltage() > UpperBound:
			dcMotor0.setTargetVelocity(0)
			dcMotor0.setTargetVelocity(-Velocity)
			Direction = "Retract"
		else:
			if Direction == "Extend":
				dcMotor0.setTargetVelocity(Velocity)
			else:
				dcMotor0.setTargetVelocity(-Velocity)
	elif ManipulatePos:
		# Limit switch
		if voltageInput0.getVoltage() > UpperBound or voltageInput0.getVoltage() < LowerBound:
			if voltageInput0.getVoltage() > 4.8:
				dcMotor0.setTargetVelocity(-Velocity)
			else:
				dcMotor0.setTargetVelocity(Velocity)
			time.sleep(0.8)
			break
		# Reach Target
		if target_voltage < voltageInput0.getVoltage():
			dcMotor0.setTargetVelocity(0)
			target_pos = float(input("Select a position from 0 ~ 500:"))
			target_voltage = (target_pos / 500) * 4.8
	else:
		break
"""


dcMotor0.close()
encoder0.close()
voltageInput0.close()


