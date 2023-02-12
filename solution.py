import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.Generate_Random_Body_and_Brain()
        self.Create_Weights()

        
        
        
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
        pyrosim.Send_Cube(name= "Box", pos=[x,y,z] , size=[length,width,height], colorString='grey')
        pyrosim.End()
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
            
    def Generate_Random_Body_and_Brain(self):
        
        # how many blocks? 3 - 12
        self.numBlocks = random.randint(3,12)
        
        self.blocks = {}
        self.dims = {}
        self.numSensors = 0
        self.numMotors = 0
        self.sensorLinkNames = []
        for i in range(self.numBlocks):
            
            # sensor?
            type = random.randint(1,2)
            if type == 1:
                color = 'green'
                self.numSensors += 1
                self.sensorLinkNames.append(f"{i}")
                
            else:
                color = 'blue'
            
            # type of joint
            if i == 0:
                joint1 = 0
                joint2 = 0
                numJoints = 0
            else:
            
#                joint = random.randint(1,3)
                joint = random.randint(1,2)
                
                if joint == 1:
                    joint1 = "1 0 0"
                    joint2 = 0
                    numJoints = 1
                    self.numMotors +=1
                if joint == 2:
                    joint1 = "0 1 0"
                    joint2 = 0
                    numJoints = 1
                    self.numMotors +=1
#                if joint == 3:
#                    joint1 = "1 0 0"
#                    joint2 = "0 1 0"
#                    numJoints = 2
#                    self.numMotors +=2
            
            self.blocks[i] = [color,joint1, joint2, numJoints]
            
            # random dimensions
            length = random.random()/2 + 0.1
            width = random.random()/2 + 0.1
            height = random.random()/2 + 0.1
            
            self.dims[i] = [length,width,height]
        
        # there needs to be at least one sensor
        if self.numSensors == 0:
            sensBlock = random.randint(0,self.numBlocks-1)
            self.blocks[sensBlock][0] = 'green'
            self.numSensors += 1

 
    
    def Create_Weights(self):
        self.weights = np.random.rand(self.numSensors,self.numMotors)
        self.weights = 2*self.weights-1
            
            
        
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        self.motorJointNames = []
        
        midZpos = 0.3
        
        for i in range(self.numBlocks):
            
            
            if i == 0:

                pyrosim.Send_Cube(name=f"{i}", pos=[0,0,midZpos] , size=self.dims[i], colorString=self.blocks[i][0])
                
            elif i == 1:
                if self.blocks[i][3] == 1:
                
                    pyrosim.Send_Joint( name = f"{i-1}_{i}" , parent= f"{i-1}" , child = f"{i}" , type = "revolute", position = [0,self.dims[i-1][1]/2,midZpos], jointAxis = self.blocks[i][1])
                    self.motorJointNames.append(f"{i-1}_{i}")
                    
#                elif self.blocks[i][3] == 2:
#
#                    pyrosim.Send_Joint( name = f"{i-1}_{i}1" , parent= f"{i-1}" , child = f"{i}" , type = "revolute", position = [0,width/2,midZpos], jointAxis = self.blocks[i][1])
#                    self.motorJointNames.append(f"{i-1}_{i}1")
#
#                    pyrosim.Send_Joint( name = f"{i-1}_{i}2" , parent= f"{i-1}" , child = f"{i}" , type = "revolute", position = [0,width/2,midZpos], jointAxis = self.blocks[i][2])
#                    self.motorJointNames.append(f"{i-1}_{i}2")
                    
                else:
                    print("too many joints system exit")
                    exit()
                    
                pyrosim.Send_Cube(name=f"{i}", pos=[0,self.dims[i][1]/2,0] , size=self.dims[i], colorString=self.blocks[i][0])
            else:
                if self.blocks[i][3] == 1:
                
                    pyrosim.Send_Joint( name = f"{i-1}_{i}" , parent= f"{i-1}" , child = f"{i}" , type = "revolute", position = [0,self.dims[i-1][1],0], jointAxis = self.blocks[i][1])
                    self.motorJointNames.append(f"{i-1}_{i}")
                    
#                elif self.blocks[i][3] == 2:
#
#                    pyrosim.Send_Joint( name = f"{i-1}_{i}1" , parent= f"{i-1}" , child = f"{i}" , type = "revolute", position = [0,width0,0], jointAxis = self.blocks[i][1])
#                    self.motorJointNames.append(f"{i-1}_{i}1")
#
#                    pyrosim.Send_Joint( name = f"{i-1}_{i}2" , parent= f"{i-1}" , child = f"{i}" , type = "revolute", position = [0,width0,0], jointAxis = self.blocks[i][2])
#                    self.motorJointNames.append(f"{i-1}_{i}2")
                    
                else:
                    print("too many joints system exit")
                    exit()
                    
                pyrosim.Send_Cube(name=f"{i}", pos=[0,self.dims[i][1]/2,0] , size=self.dims[i], colorString=self.blocks[i][0])
        
        

        print(self.blocks)
        print(f"Number of Sensors: {self.numSensors}")
        print(f"Number of Sensors List: {len(self.sensorLinkNames)}")
        print(self.sensorLinkNames)
        print(f"Number of Motors: {self.numMotors}")
        print(f"Number of Motors List: {len(self.motorJointNames)}")
        print(self.motorJointNames)
        
        
        pyrosim.End()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
            
    
        
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        
        for i, lName in enumerate(self.sensorLinkNames):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = lName)
        
        for j, jName in enumerate(self.motorJointNames):
            mName = j+self.numSensors
            
            pyrosim.Send_Motor_Neuron( name = mName , jointName = jName)

                
        for i in range(self.numSensors):
            for j in range(self.numSensors, self.numSensors + self.numMotors):
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = j , weight = self.weights[i][j-self.numSensors])
        

        pyrosim.End()
        while not os.path.exists(f"brain{self.myID}.nndf"):
            time.sleep(0.01)
        
        
        
    def Mutate(self):
        randRow = random.randint(0, self.numSensors - 1)
        randCol = random.randint(0, self.numMotors - 1)
        self.weights[randRow,randCol] = 2*random.random()-1
        
        
    def SET_ID(self, nextAvID):
        self.myID = nextAvID
        
