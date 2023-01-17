import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.stepsiter)
    
    def Get_Value(self, iter):
        self.values[iter] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #if iter == c.stepsiter - 1:
           # print(self.values)
    def Save_Values(self):
        filename = f"data/{self.linkName}SensorValues.npy"
        np.save(filename, self.values)
