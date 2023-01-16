import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
stepsiter = 100
backLegSensorValues = numpy.zeros(stepsiter)
frontLegSensorValues = numpy.zeros(stepsiter)
for i in range(stepsiter):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL, targetPosition = 0.0, maxForce = 500)
    
    time.sleep(1/60)
backfilename = 'data/backLegSensorValues.npy'
numpy.save(backfilename, backLegSensorValues)
frontfilename = 'data/frontLegSensorValues.npy'
numpy.save(frontfilename, frontLegSensorValues)
p.disconnect()

