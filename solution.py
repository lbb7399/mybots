import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from link import LINK
#from numpy.random import SeedSequence, default_rng

class SOLUTION:
    def __init__(self, myID,myPopID,child_seed):
        self.myID = myID
        self.myPopID = myPopID
        self.child_seed = child_seed
        self.child_rng = np.random.default_rng(child_seed)
        self.numXBlocks = c.numXBlocks
        self.numYBlocks = c.numYBlocks
        self.numZBlocks = c.numZBlocks
        self.numLinks = 0
        self.Generate_Random_Body_and_Brain_3D()
        self.Create_Weights()
        #print(self.weights)
        #print(self.namelist)

        
    def Start_Simulation(self, directOrGUIEv):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f"python3 simulate.py {directOrGUIEv} {str(self.myID)} {str(self.myPopID)}")
        # 2&>1 &
        
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
        
        while self.numLinks < 2:
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
        self.Define_Parent()
        self.Define_Joint_Axis_and_Type()
        self.Define_Absolute_Link_Position()
        self.Define_Joint_Position()
        self.Define_Link_Position()
        #print(self.numSensors)
        
        
#        for i, linkname in enumerate(self.namelist):
#            print(f"\n")
#            print(f"Link: {linkname} Parent: {self.links[linkname].parentLink} Joint: {self.links[linkname].jointOrient} JointDir = {self.links[linkname].jointDir} ")
#            print(self.links[linkname].absLinkPos, self.links[linkname].abs_joint_position)
#            print(self.links[linkname].linkpos, self.links[linkname].joint_position)
            


        
        
        
        
    def Create_Links(self):
        self.links = {}
        self.namelist0 = []
        self.namelistDNE = []
        numPossibleLinks = self.numXBlocks*self.numYBlocks*self.numZBlocks
        exist0 = self.child_rng.integers(low=0,high=2,size=(self.numXBlocks,self.numYBlocks,self.numZBlocks))
        gchild_seeds = self.child_seed.spawn(numPossibleLinks)
        count = 0
        for i in range(self.numXBlocks):
            for j in range(self.numYBlocks):
                for k in range(self.numZBlocks):
                    name = f"{i}{j}{k}"
                    #exist0 = random.randint(0,1)
                    if exist0[i][j][k] == 0:
                        exist = False
                        self.namelistDNE.append(name)
                    elif exist0[i][j][k] == 1:
                        exist = True
                        self.namelist0.append(name)
                    self.links[name] = LINK(name,exist,i,j,k,gchild_seeds[count])
                    count += 1
        #print("Original Name List 0")
        #print(self.namelist0)
        
        
    def Check_Link_Existence(self,startindex):
        self.canExistButDoesnt = []
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
                                            pass
                                            #print("hopefully that error is showing up")
                                            #print(self.namelist0)
                                            #print(self.namelist)
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
                                    else:
                                        if name not in self.canExistButDoesnt:
                                            self.canExistButDoesnt.append(name)
            

            
            if existance == 0:
                self.links[linkname].Set_Existance(False)
                self.namelistDNE.append(linkname)
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
        
    def New_Link_Connections(self, linkname, count):

        xlist = [self.links[linkname].x-1, self.links[linkname].x,self.links[linkname].x+1]
        ylist = [self.links[linkname].y-1, self.links[linkname].y,self.links[linkname].y+1]
        zlist = [self.links[linkname].z-1, self.links[linkname].z,self.links[linkname].z+1]

        for i, x in enumerate(xlist):
            for j, y in enumerate(ylist):
                for k, z in enumerate(zlist):
                    name = f"{x}{y}{z}"
                    relativePos = [i,j,k]
                    conrelativePos0 = -1*np.array(relativePos)
                    conrelativePos = conrelativePos0.tolist()
                    if name in self.links.keys():
                        if name != linkname:
                            #print(name, linkname)
                            if 1 in relativePos:
                                if self.links[name].exist:
                                    conIndex = self.namelist0.index(name)
                                    if conIndex < count:
                                        jointRelative = "parent"
                                        conjointRelative = "child"
                                    else:
                                        jointRelative = "child"
                                        conjointRelative = "parent"
                                    
                                    # diagonal or face to face joint
                                    if relativePos.count(1) == 2:
                                        jointOrient = "face"
                                    else:
                                        jointOrient = "hinge"
                                    
                                    self.links[linkname].Add_Joint(name, relativePos,jointRelative,jointOrient)
                                    self.links[name].Add_Joint(linkname, conrelativePos,conjointRelative,jointOrient)
                                else:
                                    if name not in self.canExistButDoesnt:
                                        self.canExistButDoesnt.append(name)

            self.links[linkname].Set_Number(self.counter)
            self.counter += 1
    
    def Removed_Link_Existence_Check(self,startindex):
        removedBlock = self.removedBlocks[0]
        self.canExistButDoesnt = []
        for count,linkname in enumerate(self.namelist0[startindex:]):
            self.links[linkname].Reset_Lists()
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
                                    else:
                                        if name not in self.canExistButDoesnt:
                                            self.canExistButDoesnt.append(name)
            
            if existance == 0:
                self.links[linkname].Set_Existance(False)
                self.namelistDNE.append(linkname)
                self.removedBlocks.append(linkname)
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
        
        if self.numSensors == 0:
            sensor = self.child_rng.integers(low=0,high=self.numLinks)
            self.links[self.namelist[sensor]].Switch_Sensor()
            self.sensorNames.append(self.namelist[sensor])
            self.numSensors = 1
        
        
    def Define_Parent(self):
        for i,linkname in enumerate(self.namelist):
            self.links[linkname].Set_Parent()
            
    def Define_Joint_Axis_and_Type(self):
        self.motorJointNames = []
        for i,linkname in enumerate(self.namelist):
            self.links[linkname].Set_Joint_Axis()
            self.links[linkname].Set_Joint_Type()
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

            elif parentLink == self.originName:
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
        #self.weights = np.random.rand(self.numSensors,self.numMotors)
        weights0 = self.child_rng.random((self.numSensors,self.numMotors))
        weights0 = 2*weights0-1
        exist = self.child_rng.integers(low=0,high=2,size=(self.numSensors,self.numMotors))
        for i in range(self.numSensors):
            for j in range(self.numMotors):
                if exist[i][j] == 0:
                    weights0[i][j] = 0
        self.weights = weights0
        #print(self.myID,self.weights)
            
            
        
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
        self.mutated = False
        prob = self.child_rng.random()
        if prob < c.section:
            self.Change_Link_Dimension()
            self.mutNum = 1
        elif c.section <= prob < 2*c.section:
            self.Mutate_Sensor()
            self.mutNum = 2
        elif 2*c.section <= prob < 3*c.section:
            self.Mutate_Add_Block()
            self.mutNum = 3
        elif 3*c.section <= prob < 4*c.section:
            self.Mutate_A_Motor_Weight()
            self.mutNum = 4
        else:
            self.Mutate_Remove_Block()
            self.mutNum = 5

#
            
    def Mutate_A_Motor_Weight(self):
        print("mutate synapses")
        if self.numSensors == 1:
            randRow = 0
        else:
            randRow = self.child_rng.integers(low=0, high=self.numSensors) # plus 1 bc exclusive (used to be -1 same for randCol)
        if self.numMotors == 1:
            randCol = 0
        else:
            randCol = self.child_rng.integers(low=0, high=self.numMotors)
        if self.weights[randRow,randCol] == 0:
            self.weights[randRow,randCol] = 2*self.child_rng.random()-1
        else:
            flip = self.child_rng.integers(low=0, high=2)
            if flip == 0:
                self.weights[randRow,randCol] == 0
            else:
                self.weights[randRow,randCol] = 2*self.child_rng.random()-1
        self.mutated = True
        
    def Mutate_Sensor(self):
        print("mutate sensor")
        sensorI = self.child_rng.integers(low=0,high=self.numLinks)
        sensor = self.namelist[sensorI]
        self.links[sensor].Switch_Sensor()
        #print(f"Original weights: {self.weights}")
        if self.links[sensor].sensor == True:
            self.sensorNames.append(sensor)
            self.numSensors += 1
            self.Add_Remove_Weight_Obj("add","none",0)
            self.mutated = True
        else:
            if self.numSensors == 1:
                self.mutated = False
                self.links[sensor].Switch_Sensor()
            else:
                index = self.sensorNames.index(sensor)
                self.Add_Remove_Weight_Obj("remove",index,0)
                self.sensorNames.remove(sensor)
                self.numSensors = self.numSensors - 1
                #print(f"New weights: {self.weights}")
                self.mutated = True
    
    def Mutate_Add_Block(self):
        #print(f"start {self.weights}")
        print("add block")
        availableBlocks = len(self.canExistButDoesnt)
        if availableBlocks == 0:
            self.mutated = False
        else:
            if availableBlocks == 1:
                index = 0
            else:
                index = self.child_rng.integers(low=0, high=availableBlocks)
            linkname = self.canExistButDoesnt[index]
            self.namelist.append(linkname)
            self.namelist0.append(linkname)
            self.canExistButDoesnt.remove(linkname)
            self.links[linkname].Set_Existance(True)
            self.numLinks += 1
            count = self.numLinks-1
            
            self.New_Link_Connections(linkname,count)
            self.links[linkname].Set_Sensor()
            #print(self.links[linkname].sensor)
            if self.links[linkname].sensor is True:
                self.sensorNames.append(linkname)
                self.numSensors += 1
                self.Add_Remove_Weight_Obj("add","none",0)
            self.links[linkname].Set_Parent()
            self.links[linkname].Set_Joint_Axis()
            self.links[linkname].Set_Joint_Type()
            self.motorJointNames.append(self.links[linkname].joint_name)
            self.numMotors += 1
            self.Add_Remove_Weight_Obj("add","none",1)
            self.links[linkname].Set_Absolute_Link_Position()
            parentLink = self.links[linkname].parentLink
            if  parentLink== self.originName:
                type = "absolute"
                parentabsJoint = self.originLinkPos
            else:
                type = "relative"
                parentabsJoint = self.links[parentLink].abs_joint_position
            
            self.links[linkname].Set_Joint_Position(type,parentabsJoint)
            self.links[linkname].Set_Link_Position()
            #print(self.numLinks)
            #print(self.weights)
            
            
            self.mutated = True
            
    def Mutate_Remove_Block(self):
        print("remove block")
        failed = False
        if self.numLinks <= 2:
            self.mutated = False
            failed = True
        else:
            index = self.child_rng.integers(low=0, high=self.numLinks)
            rlinkname = self.namelist[index]

            self.namelist.remove(rlinkname)
            self.namelist0 = self.namelist.copy()
            self.namelist = []
            self.namelistDNE.append(rlinkname)
            self.links[rlinkname].Set_Existance(False)
            self.removedBlocks = [rlinkname]
            self.counter = 0
            count = 0
            self.OneBase = False
            startindex = 0
            while self.OneBase is False:
                self.Removed_Link_Existence_Check(startindex)
                if self.OneBase is False:
                    self.namelist0.remove(self.base2name)
                    self.namelist0.append(self.base2name)
                    startindex = self.base2index
                    count += 1
                if count > 20:
                    self.mutated = False
                    failed = True
                    break
            if self.numLinks <= 2:
                self.mutated = False
                failed = True
            if failed is False:
                oldsensorNames = self.sensorNames
                sensorNames = []
                print(rlinkname)
                
                for i, linkname in enumerate(self.namelist):
                    if self.links[linkname].sensor is True:
                        sensorNames.append(linkname)
                numSensors = len(sensorNames)
                if self.numSensors == 0:
                    self.mutated = False # cannot have only 1 sensor
                    failed = True
                else:
                    self.sensorNames = sensorNames
                
                if self.numSensors > numSensors:
                    sensorindices0 = []
                    #find indices of sensors
                    for i, sensor in enumerate(oldsensorNames):
                        if sensor not in sensorNames:
                            index = oldsensorNames.index(sensor)
                            sensorindices0.append(index)
                    if len(sensorindices0) == 1:
                        self.Add_Remove_Weight_Obj("remove",sensorindices0[0],0)
                    else:
                        sensorindices = sensorindices0.sort(reverse=True)
                        for i, sensorIndex in enumerate(sensorindices):
                            self.Add_Remove_Weight_Obj("remove",sensorIndex,0)
                    
                self.numSensors = numSensors


                oldmotorJointNames = self.motorJointNames
                motorJointNames = []
                for i, linkname in enumerate(self.namelist):
                    if self.links[linkname].parentLink not in self.links[linkname].parentJointNames:
                        print("parent change",linkname)
                        self.links[linkname].Set_Parent()
                        self.links[linkname].Set_Joint_Axis()
                    if i != 0:
                        motorJointNames.append(self.links[linkname].joint_name)

                removedjoints = []
                for i, linkname in enumerate(self.removedBlocks):
                    removedjoints.append(f"{self.links[linkname].parentLink}_{linkname}")

                motorindices0 = []
                for i, motor in enumerate(removedjoints):
                    index = oldmotorJointNames.index(motor)
                    motorindices0.append(index)


                if len(motorindices0) == 1:
                    self.Add_Remove_Weight_Obj("remove",motorindices0[0],1)
                else:
                    motorindices = motorindices0.sort(reverse=True)
                    for i, motorIndex in enumerate(motorindices):
                        self.Add_Remove_Weight_Obj("remove",motorIndex,1)




                
                self.motorJointNames = motorJointNames
                self.numMotors = len(self.motorJointNames)
                self.Define_Joint_Position()
                self.Define_Link_Position()
                print(self.namelist)
                if failed is not True:
                    self.mutated = True
#                print(self.sensorNames)
#                print(len(self.sensorNames))
#                print(self.numSensors)
#                print(self.weights)
                print(self.myID)
                
                
                    
    def Change_Link_Dimension(self):
        print("change dim")
        newDim = self.child_rng.integers(low=1, high=11)*0.1
        whichDim = self.child_rng.integers(low=0, high=3)
        for i, linkname in enumerate(self.namelist):
            self.links[linkname].Change_A_Dimension(newDim,whichDim)
        self.Define_Absolute_Link_Position()
        self.Define_Joint_Position()
        self.Define_Link_Position()
        print("HELLO")
        print(self.links[linkname].dims)
        self.mutated = True
        
    def SET_ID(self, nextAvID):
        self.myID = nextAvID
    
    def Add_Remove_Weight_Obj(self,operation,index,axis):
        if operation == "add":
            if axis == 0:
                weights_add0 = self.child_rng.random((1,self.numMotors))
                weights_add = 2*weights_add0-1
                exist = self.child_rng.integers(low=0, high=2, size=(1,self.numMotors))
                for i in range(self.numMotors):
                    weights_add0[0][i] = weights_add[0][i]*exist[0][i]
            else:
                weights_add0 = self.child_rng.random((self.numSensors,1))
                weights_add = 2*weights_add0-1
                exist = self.child_rng.integers(low=0, high=2, size=(self.numSensors,1))
                for i in range(self.numSensors):
                    weights_add0[i] = weights_add[i]*exist[i]
            self.weights = np.append(self.weights, weights_add, axis)
        else:
            self.weights = np.delete(self.weights, index, axis)
            
    def New_Seed(self,seed):
        self.child_seed = seed
        self.child_rng = np.random.default_rng(seed)
        
        
