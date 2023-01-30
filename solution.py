import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
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
        os.system(f"python3 simulate.py {directOrGUIEv} {str(self.myID)} 2&>1 &")
        
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
        pyrosim.Send_Cube(name= "Torso", pos=[0,0,1] , size=[length,width,height])
        
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name= "BackLeg", pos=[0,-0.5,0] , size=[0.2,1,0.2])
        
        pyrosim.Send_Joint( name = "BackLeg_BackLegLower" , parent= "BackLeg" , child = "BackLegLower" , type = "revolute", position = [0,-1,-0.1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name= "BackLegLower", pos=[0,-0.1,-0.45] , size=[0.2,0.2,0.9])
        
        
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name= "FrontLeg", pos=[0,0.5,0] , size=[0.2,1,0.2])
        
        pyrosim.Send_Joint( name = "FrontLeg_FrontLegLower" , parent= "FrontLeg" , child = "FrontLegLower" , type = "revolute", position = [0,1,-0.1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name= "FrontLegLower", pos=[0,0.1,-0.45] , size=[0.2,0.2,0.9])
        
        
        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5,0,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "LeftLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2])
        
        pyrosim.Send_Joint( name = "LeftLeg_LeftLegLower" , parent= "LeftLeg" , child = "LeftLegLower" , type = "revolute", position = [-1,0,-0.1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "LeftLegLower", pos=[-0.1,0,-0.45] , size=[0.2,0.2,0.9])
        
        
        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "RightLeg", pos=[0.5,0,0] , size=[1,0.2,0.2])
        
        pyrosim.Send_Joint( name = "RightLeg_RightLegLower" , parent= "RightLeg" , child = "RightLegLower" , type = "revolute", position = [1,0,-0.1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "RightLegLower", pos=[0.1,0,-0.45] , size=[0.2,0.2,0.9])
        
        pyrosim.End()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
            
    
        
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "FrontLegLower")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "BackLegLower")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLegLower")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLegLower")
#
        
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "FrontLeg_FrontLegLower")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "BackLeg_BackLegLower")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "LeftLeg_LeftLegLower")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_RightLegLower")
                
        for i in range(c.numSensorNeurons):
            for j in range(c.numSensorNeurons, c.numSensorNeurons + c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = j , weight = self.weights[i][j-c.numSensorNeurons])
        

        pyrosim.End()
        while not os.path.exists(f"brain{self.myID}.nndf"):
            time.sleep(0.01)
        
        
    def Mutate(self):
        randRow = random.randint(0, c.numSensorNeurons - 1)
        randCol = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randRow,randCol] = 2*random.random()-1
        
    def SET_ID(self, nextAvID):
        self.myID = nextAvID
        
