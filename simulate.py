import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

stepsiter = 1000
amplitude = np.pi/4
frequency = 10
phaseOffset = 0
backLegSensorValues = np.zeros(stepsiter)
frontLegSensorValues = np.zeros(stepsiter)

targetAngles = amplitude * np.sin(frequency * np.linspace(0, 2*np.pi, stepsiter) + phaseOffset)
#np.save('data/targetAngles.npy', targetAngles)
#exit()
for i in range(stepsiter):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL, targetPosition = targetAngles[i], maxForce = 50)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_FrontLeg", controlMode = p.POSITION_CONTROL, targetPosition = targetAngles[i], maxForce = 50)
    
    time.sleep(1/240)
backfilename = 'data/backLegSensorValues.npy'
np.save(backfilename, backLegSensorValues)
frontfilename = 'data/frontLegSensorValues.npy'
np.save(frontfilename, frontLegSensorValues)
p.disconnect()

