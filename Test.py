from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.VoltageInput import *
import time

def onPositionChange(self, positionChange, timeChange, indexTriggered):
    print("----------")
    print("PositionChange: " + str(positionChange))
    print("TimeChange: " + str(timeChange))
    print("IndexTriggered: " + str(indexTriggered))
    print("getPosition: " + str(self.getPosition()))
    print()
    print("----------")

def onVoltageChange(self, voltage):
    print("Voltage: " + str(voltage))

def onVelocityUpdate(self, velocity):
    print("Velocity: " + str(velocity))

try:
    dcMotor0 = DCMotor()
    encoder0 = Encoder()
    voltage0 = VoltageInput()
except PhidgetException as e:
    sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t")
    raise


encoder0.setOnPositionChangeHandler(onPositionChange)
dcMotor0.setOnVelocityUpdateHandler(onVelocityUpdate)
voltage0.setOnVoltageChangeHandler(onVoltageChange)


dcMotor0.openWaitForAttachment(1000)
encoder0.openWaitForAttachment(1000)
voltage0.openWaitForAttachment(1000)

encoder0.setPosition(100)
encoder0.setDataInterval(256)
encoder0.setPositionChangeTrigger(1)
dcMotor0.setTargetVelocity(-0.5)


try:
    input("Press Enter to Stop\n")
except (Exception, KeyboardInterrupt):
    pass

dcMotor0.close()
encoder0.close()
