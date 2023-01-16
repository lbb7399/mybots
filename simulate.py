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
stepsiter = 10
backLegSensorValues = numpy.zeros(stepsiter)
for i in range(stepsiter):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    time.sleep(1/60)
filename = 'data/backlegsensor.npy'
#filename = '/Users/lindsaybogar/gitrep/data/backlegsensor.npy'
numpy.save(filename, backLegSensorValues)
print(backLegSensorValues)
p.disconnect()

