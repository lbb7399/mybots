import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os

class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2)
        self.weights = 2*self.weights-1

        
    def Evaluate(self):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python3 simulate.py")
        f = open("fitness.txt", "r")
        self.fitness = float(f.read())
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 1
        width = 1
        height = 1
        x = -2
        y = 2
        z = 0.5
        pyrosim.Send_Cube(name= "Box", pos=[x,y,z] , size=[length,width,height])
        pyrosim.End()
        
    def Generate_Body(self):
        length = 1
        width = 1
        height = 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name= "Torso", pos=[1.5,0,1.5] , size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
        pyrosim.Send_Cube(name= "BackLeg", pos=[-0.5,0,-0.5] , size=[length,width,height])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
        pyrosim.Send_Cube(name= "FrontLeg", pos=[0.5,0,-0.5] , size=[length,width,height])
        pyrosim.End()
        
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")
        
        self.sensorNeuronNames = [0, 1, 2]
        self.motorNeuronNames = [3,4]
        for currentRow, sensor in enumerate(self.sensorNeuronNames):
            for currentColumn, motor in enumerate(self.motorNeuronNames):
                pyrosim.Send_Synapse(sourceNeuronName = sensor , targetNeuronName = motor , weight = self.weights[currentRow][currentColumn])

        pyrosim.End()
        
    def Mutate(self):
        randRow = random.randint(0, len(self.weights) - 1)
        randCol = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randRow,randCol] = 2*random.random()-1
