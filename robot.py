from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import math
import os
import constants as c
class ROBOT:
    def __init__(self, solutionID, world):
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        os.system(f"rm brain{solutionID}.nndf")
        self.solutionID = solutionID
        self.world = world

        
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
            
    def Act(self, iter):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
               # print(f"Neuron Name: {neuronName}, Joint Name: {jointName}, Desired Angle: {desiredAngle}")
                
        #for key in self.motors:
            #self.motors[key].Set_Value(self.robotId, iter)
            
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
        
    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        f = open(f"tmp{self.solutionID}.txt", "w")
        f.write(str(xPosition))
        f.close()
        os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        
        ballPosition = self.world.Get_Ball_Position()
        print(ballPosition)
        ballMagnitude = math.sqrt((ballPosition[0]-c.ballInitialX)**2+(ballPosition[1]-c.ballInitialY)**2)
        if ballMagnitude < 0.01:
            ballMagnitude = 0
        
        g = open(f"balltmp{self.solutionID}.txt", "w")
        g.write(str(ballMagnitude))
        g.close()
        os.system(f"mv balltmp{self.solutionID}.txt ballfitness{self.solutionID}.txt")
        
