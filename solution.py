import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from link import LINK

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.Generate_Random_Body_and_Brain_3D()
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
            
            
    def Generate_Random_Body_and_Brain_3D(self):
        self.Create_Branching()
        self.Define_Shapes()
        self.Define_Dimensions()
        self.Define_Sensors()
        self.Define_Direction()
        self.Define_Joint_Axis()
        self.Define_Joint_Position()
        self.Define_Link_Position()
        
    
    
    def Create_Branching(self):
        
        self.links = {}

        branching = [0]*(c.numGenBody)
        numChildren = random.randint(c.numChildLow,c.numChildHigh)
        branching[0] = numChildren

        branchNames = [0]*(c.numGenBody)
        self.branchNames1 =[0]
        linkcount = 0
        self.links[0] = LINK(branchNames[0], "none", numChildren)
        linkcount +=1

        # determines branching through generations
        for i in range(c.numGenBody-1):
            if isinstance(branching[i], int):
                childrenthisgen = branching[i]
            else:
                childrenthisgen = sum(branching[i])
            
            
            childrenPerGen = [0]*childrenthisgen
            for j in range(childrenthisgen):
                if i == c.numGenBody -2:
                    childrenPerGen[j] = 0
                else:
                    numChildren = random.randint(c.numChildLow,c.numChildHigh)
                    childrenPerGen[j]=numChildren
            #print(j)


            branching[i+1] = childrenPerGen



        # assigns names to each link
        for i, parents in enumerate(branching[:(c.numGenBody-1)]):

            
            if isinstance(parents, int):
                namesChildrenthisgen = [0]*parents
                #childrenPerGen = [0]*parents
                for j in range(parents):
                    
                    if i == 0:
                        namelink = str(j+1)
                        namesChildrenthisgen[j] = namelink
                        self.branchNames1.append(namelink)
                        if isinstance(branching[i+1], int):
                            self.links[namelink] = LINK(namelink, 0, branching[i+1])
                        else:
                            self.links[namelink] = LINK(namelink, 0, branching[i+1][j])
                        linkcount +=1
                    else:
                        namelink = f"{branchNames[i][0]}{j+1}"
                        namesChildrenthisgen[j] = namelink
                        self.branchNames1.append(namelink)
                        if isinstance(branching[i+1], int):
                            self.links[namelink] = LINK(namelink,f"{branchNames[i][0]}", branching[i+1])
                        else:
                            self.links[namelink] = LINK(namelink,f"{branchNames[i][0]}", branching[i+1][j])
                        linkcount += 1

            else:
                namesChildrenthisgen = [0]*sum(parents)
                
                count = 0
                for j, children in enumerate(parents):
                    
                    for k in range(children):
                        namelink = branchNames[i][j] + str(k+1)
                        namesChildrenthisgen[count] = namelink
                        self.branchNames1.append(namelink)
                        self.links[namelink] = LINK(namelink, branchNames[i][j], branching[i+1][count])
                        count += 1
                        linkcount += 1
                    


            branchNames[i+1] = namesChildrenthisgen
                        
        print(branchNames)
#        print(branching)
#        for i in self.links:
#            print(self.links[i].linkID, self.links[i].parentID, self.links[i].numChildren)
#            print(f"\n")
#        print(self.branchNames1)
        
        
                
    def Define_Shapes(self):
            
        for i, linkname in enumerate(self.branchNames1):
            if self.links[linkname].Is_Origin(linkname):
                self.links[linkname].Set_Shape("none")
            else:
                parentID = self.links[linkname].parentID
                parentLink = self.links[parentID]
                parentShape = parentLink.shape
                self.links[linkname].Set_Shape(parentShape)
                        
    
    def Define_Dimensions(self):
            
        for i, linkname in enumerate(self.branchNames1):
            if self.links[linkname].Is_Origin(linkname):
                self.links[linkname].Set_Dimensions("none")
            else:
                parentID = self.links[linkname].parentID
                parentLink = self.links[parentID]
                parentDims = parentLink.dims
                self.links[linkname].Set_Dimensions(parentDims)
            
    def Define_Sensors(self):
        self.sensorNames = []
        for i,linkname in enumerate(self.links):
            self.links[linkname].Set_Sensor()
            if self.links[linkname].sensor is True:
                self.sensorNames.append(linkname)
        
        self.numSensors = len(self.sensorNames)
            
    def Define_Direction(self):

        for i, linkname in enumerate(self.branchNames1):
            if self.links[linkname].Is_Origin(linkname):
                direction = "none"
                parentInline = "none"
                self.links[linkname].Set_Direction(direction,"none","none",parentInline)
            else:
                parentID = self.links[linkname].parentID
                parentLink = self.links[parentID]
                parentDirection = parentLink.direction
                gparentDirection = parentLink.parentDirection
                parentInline = parentLink.inline
                count = 0
                while count < 1:
                    direction = random.randint(1,6)
                    if self.Check_Direction(parentDirection,direction):
                        self.links[linkname].Set_Direction(direction,parentDirection,gparentDirection,parentInline)
                        count = 1
    
    def Define_Joint_Axis(self):
        self.motorJointNames = []
        for i,linkname in enumerate(self.links):
            self.links[linkname].Set_Joint_Axis()
            if i != 0:
                self.motorJointNames.append(self.links[linkname].joint_name)
        
        self.numMotors = len(self.motorJointNames)
                
    def Define_Joint_Position(self):
        
        for i, linkname in enumerate(self.branchNames1):
            if self.links[linkname].Is_Origin(linkname):
                self.links[linkname].Set_Joint_Position()
            else:
                self.links[linkname].Set_Joint_Position()
            

    def Define_Link_Position(self):
        for i,linkname in enumerate(self.links):
            self.links[linkname].Set_Link_Position()
            

 
    
    def Create_Weights(self):
        self.weights = np.random.rand(self.numSensors,self.numMotors)
        self.weights = 2*self.weights-1
            
            
        
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        for i,linkname in enumerate(self.links):
            
            if i == 0:

                self.links[linkname].Send_Object()
                
            else:
                self.links[linkname].Send_Joint()
                self.links[linkname].Send_Object()
        
        pyrosim.End()
        while not os.path.exists("body.urdf"):
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
        
