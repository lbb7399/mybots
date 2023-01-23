import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
import pybullet as p

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
    
    def Prepare_To_Act(self):
        self.amplitude = c.amplitudeBack
        self.offset = c.phaseOffsetBack
        if self.jointName == "Torso_BackLeg":
            self.frequency = c.frequencyBack
        else:
            self.frequency = c.frequencyBack/2
        self.motorValues = self.amplitude * np.sin(self.frequency * np.linspace(0, 2*np.pi, c.stepsiter) + self.offset)
        
    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = desiredAngle, maxForce = c.maxForceBack)
        
    def Save_Values(self):
        filename = f"data/{self.jointName}MotorValues.npy"
        np.save(filename, self.MotorValues)
