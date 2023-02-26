import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from link import LINK

class SOLUTION:
    def __init__(self, myID,myPopID):
        self.myID = myID
        self.myPopID = myPopID
        self.numXBlocks = c.numXBlocks
        self.numYBlocks = c.numYBlocks
        self.numZBlocks = c.numZBlocks
        self.numLinks = 0
        self.Generate_Random_Body_and_Brain_3D()
        self.Create_Weights()

        
        
        
    def Start_Simulation(self, directOrGUIEv):
        self.Create_World()

        self.Generate_Body()
        self.Generate_Brain()
        os.system(f"python3 simulate.py {directOrGUIEv} {str(self.myID)} {str(self.myPopID)}")
        
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{str(self.myID)}.txt", "r")
        self.fitness = float(f.read())
        os.system(f"rm fitness{self.myID}.txt")
        #print(f"FITNESS: {self.fitness}")
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 0.1
        width = 0.1
        height = 0.1
        x = -2
        y = 2
        z = 0.5
        pyrosim.Send_Cube(name= "Box", pos=[x,y,z] , size=[length,width,height], colorString='grey')
        pyrosim.End()
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
            
    def Generate_Random_Body_and_Brain_3D(self):
        
        while self.numLinks == 0:
            count = 0
            self.namelist = []
            self.OneBase = False
            self.counter = 0
            startindex = 0
            self.Create_Links()
            while self.OneBase is False:
                self.Check_Link_Existence(startindex)
                if self.OneBase is False:
#                    print(self.namelist0)
                    self.namelist0.remove(self.base2name)
                    self.namelist0.append(self.base2name)
                    startindex = self.base2index
                    self.links[self.base2name].Reset_Lists()
                    print("THIS IS WORKING")
                    print(self.counter, self.base2name)
                    print(self.namelist0[startindex:])
                    count += 1
                if count > 20:
                    self.OneBase = True
                    self.numLinks == 0
                    
                
        self.Define_Sensors()
        self.Define_Joint_Axis()
        self.Define_Absolute_Link_Position()
        self.Define_Joint_Position()
        self.Define_Link_Position()
        
        
        for i, linkname in enumerate(self.namelist):
            print(f"\n")
            print(f"Link: {linkname} Parent: {self.links[linkname].parentLink} Joint: {self.links[linkname].jointOrient} JointDir = {self.links[linkname].jointDir} ")
            print(self.links[linkname].absLinkPos, self.links[linkname].abs_joint_position)
            print(self.links[linkname].linkpos, self.links[linkname].joint_position)
            


        
        
        
        
    def Create_Links(self):
        self.links = {}
        self.namelist0 = []
        for i in range(self.numXBlocks):
            for j in range(self.numYBlocks):
                for k in range(self.numZBlocks):
                    name = f"{i}{j}{k}"
                    exist0 = random.randint(0,1)
                    if exist0 == 0:
                        exist = False
                    elif exist0 == 1:
                        exist = True
                        self.namelist0.append(name)
                    self.links[name] = LINK(name,exist,i,j,k)
        print("Original Name List 0")
        print(self.namelist0)
        
        
    def Check_Link_Existence(self,startindex):
        for count,linkname in enumerate(self.namelist0[startindex:]):
            existance = 0
    
            xlist = [self.links[linkname].x-1, self.links[linkname].x,self.links[linkname].x+1]
            ylist = [self.links[linkname].y-1, self.links[linkname].y,self.links[linkname].y+1]
            zlist = [self.links[linkname].z-1, self.links[linkname].z,self.links[linkname].z+1]

            for i, x in enumerate(xlist):
                for j, y in enumerate(ylist):
                    for k, z in enumerate(zlist):
                        name = f"{x}{y}{z}"
                        relativePos = [i,j,k]
                        if name in self.links.keys():
                            if name != linkname:
                                #print(name, linkname)
                                if 1 in relativePos:
                                    if self.links[name].exist:
                                        existance += 1 # this link has connections and therefore will exist
                                        
                                        # defining if this connector link is the parent or child to current link
                                        if not name in self.namelist0:
                                            print("hopefully that error is showing up")
                                            print(self.namelist0)
                                            print(self.namelist)
                                        conIndex = self.namelist0.index(name)
                                        if conIndex < count+startindex:
                                            jointRelative = "parent"
                                        else:
                                            jointRelative = "child"
                                        
                                        # diagonal or face to face joint
                                        if relativePos.count(1) == 2:
                                            jointOrient = "face"
                                        else:
                                            jointOrient = "hinge"
                                        
                                        self.links[linkname].Add_Joint(name, relativePos,jointRelative,jointOrient)
            

            
            if existance == 0:
                self.links[linkname].Set_Existance(False)
            else:
                if self.links[linkname].numPossibleParents == 0 and self.counter != 0:
                    self.base2name = linkname
                    self.base2index = count+startindex
                    return
                self.namelist.append(linkname)
                self.links[linkname].Set_Number(self.counter)
                self.counter += 1
        
        self.numLinks = self.counter
        self.OneBase = True
        
                
                
    
                                
    def Define_Sensors(self):
        self.sensorNames = []
        for i,linkname in enumerate(self.namelist):
            self.links[linkname].Set_Sensor()
            if self.links[linkname].sensor is True:
                self.sensorNames.append(linkname)
        
        self.numSensors = len(self.sensorNames)
        
                            
                
    def Define_Joint_Axis(self):
        self.motorJointNames = []
        for i,linkname in enumerate(self.namelist):
            self.links[linkname].Set_Joint_Axis()
            if i != 0:
                self.motorJointNames.append(self.links[linkname].joint_name)

        self.numMotors = len(self.motorJointNames)
#        print(self.motorJointNames)
        
    def Define_Absolute_Link_Position(self):
        for i, linkname in enumerate(self.namelist):
            self.links[linkname].Set_Absolute_Link_Position()
        
            
    def Define_Joint_Position(self):
        self.originName = self.namelist[0]
        self.originLinkPos = self.links[self.originName].absLinkPos
        for i, linkname in enumerate(self.namelist):
            parentLink = self.links[linkname].parentLink
            if linkname == self.originName:
                type = "origin"
                parentabsJoint = "none"

            elif  parentLink== self.originName:
                type = "absolute"
                parentabsJoint = self.originLinkPos
            else:
                type = "relative"
                parentabsJoint = self.links[parentLink].abs_joint_position
            
            self.links[linkname].Set_Joint_Position(type,parentabsJoint)
        

    def Define_Link_Position(self):
        for i,linkname in enumerate(self.namelist):
            self.links[linkname].Set_Link_Position()
                    




 
    
    def Create_Weights(self):
        self.weights = np.random.rand(self.numSensors,self.numMotors)
        self.weights = 2*self.weights-1
            
            
        
    def Generate_Body(self):
        pyrosim.Start_URDF(f"body{self.myPopID}.urdf")
        
        for i,linkname in enumerate(self.namelist):
            
            if i == 0:

                self.links[linkname].Send_Object()
                
            else:
                self.links[linkname].Send_Joint()
                self.links[linkname].Send_Object()
        
        pyrosim.End()
        while not os.path.exists(f"body{self.myPopID}.urdf"):
            time.sleep(0.01)

    
        
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        
        for i, lName in enumerate(self.sensorNames):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = f"{lName}")
        
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
        
    def Check_Direction(self, parentDirection, direction):
        if parentDirection == "none":
            return True
        else:
            if (parentDirection % 2) == 0:
                badDirection = parentDirection - 1
            else:
                badDirection = parentDirection + 1
            
            if badDirection == direction:
                return False
            else:
                return True
        
