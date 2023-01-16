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
amplitudeBack = 4*np.pi/16
frequencyBack = 10
phaseOffsetBack = np.pi/8
backLegSensorValues = np.zeros(stepsiter)
amplitudeFront = 4*np.pi/16
frequencyFront = 10
phaseOffsetFront = 0
frontLegSensorValues = np.zeros(stepsiter)

targetAnglesBack = amplitudeBack * np.sin(frequencyBack * np.linspace(0, 2*np.pi, stepsiter) + phaseOffsetBack)
targetAnglesFront = amplitudeFront * np.sin(frequencyFront * np.linspace(0, 2*np.pi, stepsiter) + phaseOffsetFront)
#np.save('data/targetAnglesBack.npy', targetAnglesBack)
#np.save('data/targetAnglesFront.npy', targetAnglesFront)
#exit()
for i in range(stepsiter):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesBack[i], maxForce = 40)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_FrontLeg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesFront[i], maxForce = 40)
    
    time.sleep(1/240)
backfilename = 'data/backLegSensorValues.npy'
np.save(backfilename, backLegSensorValues)
frontfilename = 'data/frontLegSensorValues.npy'
np.save(frontfilename, frontLegSensorValues)
p.disconnect()

