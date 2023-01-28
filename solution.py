import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(3,2)
        self.weights = 2*self.weights-1

        
#    def Evaluate(self, directOrGUIEv):
#        self.Create_World()
#        self.Generate_Body()
#        self.Generate_Brain()
#
#        os.system(f"python3 simulate.py {directOrGUIEv} {str(self.myID)} &")
#        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
#            time.sleep(0.01)
#        f = open(f"fitness{str(self.myID)}.txt", "r")
#        self.fitness = float(f.read())
        
        
    def Start_Simulation(self, directOrGUIEv):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f"python3 simulate.py {directOrGUIEv} {str(self.myID)} &")
        
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{str(self.myID)}.txt", "r")
        self.fitness = float(f.read())
        os.system(f"rm fitness{self.myID}.txt")
        #print(f"FITNESS: {self.fitness}")
        
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
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        
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
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
        
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
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
        while not os.path.exists(f"brain{self.myID}.nndf"):
            time.sleep(0.01)
        
    def Mutate(self):
        randRow = random.randint(0, len(self.weights) - 1)
        randCol = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randRow,randCol] = 2*random.random()-1
        
    def SET_ID(self, nextAvID):
        self.myID = nextAvID
        
