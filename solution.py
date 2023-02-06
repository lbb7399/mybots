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
        
        #os.system(f"rm fitness{self.myID}.txt")
        #print(f"FITNESS: {self.fitness}")
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 1
        width = 1
        height = 1
        x = -2
        y = 2
        z = 0.5
        #pyrosim.Send_Cube(name= "Box", pos=[x,y,z] , size=[length,width,height])
        pyrosim.Send_Sphere(name="BowlingBall" , pos=[-3,+3,0.5] , size=[0.1])
        pyrosim.End()
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        
    def Generate_Body(self):
        goalZPos = 0.8
        tlength = 1
        twidth = 0.5
        theight = 0.3
        
        llength = 0.15
        lwidth = 0.15
        lheight = ((goalZPos-theight/2)/np.sqrt(2)) - llength
        
        tzPos = 2*lheight + theight/2
        
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name= "Torso", pos=[0,0,tzPos] , size=[tlength,twidth,theight])
        
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [tlength/2,-(twidth/2 - lwidth/2),tzPos-theight/2], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "BackLeg", pos=[llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])

        pyrosim.Send_Joint( name = "BackLeg_BackLegLower" , parent= "BackLeg" , child = "BackLegLower" , type = "revolute", position = [0,0,-lheight], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "BackLegLower", pos=[llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])


        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [-tlength/2,-(twidth/2 - lwidth/2),tzPos-theight/2], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "FrontLeg", pos=[-llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])

        pyrosim.Send_Joint( name = "FrontLeg_FrontLegLower" , parent= "FrontLeg" , child = "FrontLegLower" , type = "revolute", position = [-llength,0,-lheight], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "FrontLegLower", pos=[llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])


        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-tlength/2,(twidth/2 - lwidth/2),tzPos-theight/2], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "LeftLeg", pos=[-llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])
        
        pyrosim.Send_Joint( name = "LeftLeg_LeftLegLower" , parent= "LeftLeg" , child = "LeftLegLower" , type = "revolute", position = [-llength,0,-lheight], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "LeftLegLower", pos=[llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])
        
        
        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [tlength/2,(twidth/2 - lwidth/2),tzPos-theight/2], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "RightLeg", pos=[llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])
        
        pyrosim.Send_Joint( name = "RightLeg_RightLegLower" , parent= "RightLeg" , child = "RightLegLower" , type = "revolute", position = [0,0,-lheight], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name= "RightLegLower", pos=[llength/2,0,-lheight/2] , size=[llength,lwidth,lheight])
        
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
        
