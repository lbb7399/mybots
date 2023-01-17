from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, iter):
        for key in self.sensors:
            self.sensors[key].Get_Value(iter)
            
    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            self.motors[jointName].Prepare_To_Act()
            
    def Act(self, iter):
        for key in self.motors:
            self.motors[key].Set_Value(self.robotId, iter)
            
