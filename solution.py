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
        os.system(f"python3 simulate.py {directOrGUIEv} {str(self.myID)} {str(self.myPopID)} 2&>1 &")
        # 2&>1 &
        
    def Wait_For_Simulation_To_End(self):
        start_time = time.time()
        while not os.path.exists(f"files/fitness{str(self.myID)}.txt"):
            time.sleep(0.01)
            time_now = time.time()
            diff = time_now-start_time
            if diff > 120:
                print("fitness file now loading")
                exit()
        f = open(f"files/fitness{str(self.myID)}.txt", "r")
        self.fitness = float(f.read())
        os.system(f"rm files/fitness{self.myID}.txt")
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
                    #print("THIS IS WORKING")
                    #print(self.counter, self.base2name)
                    #print(self.namelist0[startindex:])
                    count += 1
                if count > 20:
                    self.OneBase = True
                    self.numLinks == 0
            #print(self.namelist)
            
                    
                
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
        self.links[linkname].Reset_Lists()
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
                                    #print(name,conIndex,count)
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
        
#        DNEanymore = []
#        for key in self.links[linkname].connections:
#            if not key in self.namelist:
#                DNEanymore.append(key)
#
#        if DNEanymore:
#            for i, key in enumerate(DNEanymore):
#                del self.links[linkname].connections[key]
#                if key in self.links[linkname].parentJointNames:
#                    self.links[linkname].parentJointNames.remove(key)
#
#                elif key in self.links[linkname].childJointNames:
#                    self.links[linkname].childJointNames.remove(key)
                
        
        
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
        pyrosim.Start_URDF(f"files/body{self.myPopID}.urdf")
        
        for i,linkname in enumerate(self.namelist):
            
            if i == 0:

                self.links[linkname].Send_Object()
                
            else:
                self.links[linkname].Send_Joint()
                self.links[linkname].Send_Object()
        
        pyrosim.End()
        while not os.path.exists(f"files/body{self.myPopID}.urdf"):
            time.sleep(0.01)

    
        
    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"files/brain{self.myID}.nndf")
        
        for i, lName in enumerate(self.sensorNames):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = f"{lName}")
        
        for j, jName in enumerate(self.motorJointNames):
            mName = j+self.numSensors
            
            pyrosim.Send_Motor_Neuron( name = mName , jointName = jName)

                
        for i in range(self.numSensors):
            for j in range(self.numSensors, self.numSensors + self.numMotors):
                pyrosim.Send_Synapse(sourceNeuronName = i , targetNeuronName = j , weight = self.weights[i][j-self.numSensors])
        

        pyrosim.End()
        while not os.path.exists(f"files/brain{self.myID}.nndf"):
            time.sleep(0.01)
            
            
    def Mutate(self):
        self.mutated = False
        self.mutation = "none"
        prob = self.child_rng.random()
        if prob < 0.25:
            self.Mutate_A_Motor_Weight()
            self.mutNum = 1
        elif 0.25 <= prob < 0.5:
            self.Mutate_Sensor()
            self.mutNum = 2
        elif 0.5 <= prob < 4*0.5/3:
            self.Mutate_Add_Block()
            self.mutNum = 3
        elif 4*0.5/3 <= prob < 5*0.5/3:
            self.Change_Link_Dimension()
            self.mutNum = 4
        else:
            self.Mutate_Remove_Block()
            self.mutNum = 5
            
        
    def Mutate_Mind(self):
        self.mutated = False
        self.mutation = "none"
        prob = self.child_rng.random()
        if prob < 0.5:
            self.Mutate_A_Motor_Weight()
            self.mutNum = 1
        else:
            self.Mutate_Sensor()
            self.mutNum = 2

            
    def Mutate_Body(self):
        self.mutated = False
        self.mutation = "none"
        prob = self.child_rng.random()
        if prob < 1/3:
            self.Mutate_Add_Block()
            self.mutNum = 3
        elif 1/3 <= prob < 2/3:
            self.Change_Link_Dimension()
            self.mutNum = 4
        else:
            self.Mutate_Remove_Block()
            self.mutNum = 5

#
            
    def Mutate_A_Motor_Weight(self):
        
        if self.numSensors == 1:
            randRow = 0
        else:
            randRow = self.child_rng.integers(low=0, high=self.numSensors) # plus 1 bc exclusive (used to be -1 same for randCol)
        if self.numMotors == 1:
            randCol = 0
        else:
            randCol = self.child_rng.integers(low=0, high=self.numMotors)
        original = self.weights[randRow,randCol]
        if self.weights[randRow,randCol] == 0:
            self.weights[randRow,randCol] = 2*self.child_rng.random()-1
        else:
            flip = self.child_rng.integers(low=0, high=2)
            if flip == 0:
                self.weights[randRow,randCol] == 0
            else:
                self.weights[randRow,randCol] = 2*self.child_rng.random()-1
        new = self.weights[randRow,randCol]
        self.mutated = True
        print("mutate synapses")
        self.mutation = f"Mutated sensor: {randRow}, Mutated Motor {randCol}, Old: {original}, New: {new}"
        
    def Mutate_Sensor(self):
        #print(self.namelist)
        #print(self.weights)
        #print(len(self.weights),len(self.weights[0]))
        #print(self.sensorNames,self.numSensors,len(self.sensorNames))
        
        #print(self.motorJointNames,self.numMotors,len(self.motorJointNames))
        sensorI = self.child_rng.integers(low=0,high=self.numLinks)
        sensor = self.namelist[sensorI]
        self.links[sensor].Switch_Sensor()
        #print(f"Original weights: {self.weights}")
        if self.links[sensor].sensor == True:
            self.sensorNames.append(sensor)
            self.numSensors += 1
            self.Add_Remove_Weight_Obj("add","none",0)
            self.mutated = True
            print("mutate sensor")
            self.mutation = f"Sensor {sensor} turned on"
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
                print("mutate sensor")
                self.mutation = f"Sensor {sensor} turned off"
    
    def Mutate_Add_Block(self,link="default"):
        #print(f"start {self.weights}")
        
        availableBlocks = len(self.canExistButDoesnt)
        if availableBlocks == 0:
            self.mutated = False
        else:
            if link != "default":
                linkname = link
            else:
                if availableBlocks == 1:
                    index = 0
                else:
                    index = self.child_rng.integers(low=0, high=availableBlocks)
                linkname = self.canExistButDoesnt[index]
            print(linkname)
            #print("added block", linkname)
            #print("original name list",self.namelist)
            self.namelist.append(linkname)
            self.namelist0.append(linkname)
            self.canExistButDoesnt.remove(linkname)
            self.links[linkname].Set_Existance(True)
            #print("name list after existance stuff", self.namelist)
            self.numLinks = len(self.namelist)
            #print(self.numLinks)
            count = self.numLinks
            
            self.New_Link_Connections(linkname,count)
            #print(self.links["000"].connections)
            #for i , linknamex in enumerate(self.namelist):
                #print(self.links[linknamex].connections)
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
            
            print(f"add block {linkname}")
            self.mutated = True
            self.mutation = f"Link {linkname} added. Parent link {parentLink}"
            
    def Mutate_Remove_Block(self,link = "default"):
        
        failed = False
        if self.numLinks <= 2:
            self.mutated = False
            failed = True
        else:
            if link == "default":
                index = self.child_rng.integers(low=0, high=self.numLinks)
                rlinkname = self.namelist[index]
            else:
                rlinkname = link
                index = self.namelist.index(rlinkname)
            #print("original")
            #print(self.namelist)
            print(rlinkname)
            #print(f"\n")
            if index == 0:
                isorigin = True
            else:
                isorigin = False
            oldnamelist = self.namelist.copy()
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
            #print("after attempt")
            #print(self.namelist)
            if failed == False:
                oldsensorNames = self.sensorNames
                sensorNames = []
                #print(rlinkname)
                
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
                        sensorindices0.sort(reverse=True)
                        for i, sensorIndex in enumerate(sensorindices0):
                            self.Add_Remove_Weight_Obj("remove",sensorIndex,0)
                    
                self.numSensors = numSensors


                oldmotorJointNames = self.motorJointNames
                motorJointNames = []
                changes = []
                oldparentsjoints = []
                for i, linkname in enumerate(self.namelist):

                    if i != 0:
                        if self.links[linkname].parentLink not in self.links[linkname].parentJointNames:
                            old = self.links[linkname].parentLink
                            #print("    parent change",linkname)
                            self.links[linkname].Set_Parent()
                            self.links[linkname].Set_Joint_Axis()
                            changes.append(f"Link: {linkname}, Old Parent: {old}, New Parent: {self.links[linkname].parentLink}")
                            oldparentsjoints.append(f"{old}_{linkname}")
                        motorJointNames.append(self.links[linkname].joint_name)
                    else:
                        if self.links[linkname].parentLink != "none":
                            old = self.links[linkname].parentLink
                            #print("    parent change",linkname)
                            self.links[linkname].Set_Parent(parent="none")
                            changes.append(f"Link: {linkname}, Old Parent: {old}, New Parent: none")
                
                        
                    
                
                #print(self.removedBlocks)
                removedjoints = []
                #print("old weights",len(self.weights),len(self.weights[0]))
                #print("old joints",oldmotorJointNames,len(oldmotorJointNames))
                #print("new joints",self.motorJointNames,len(motorJointNames))
                #print("num motors", self.numMotors)
                for i,joint in enumerate(oldmotorJointNames):
                    if joint not in motorJointNames:
                        if joint not in oldparentsjoints:
                            removedjoints.append(joint)
                            
#                for i, linkname in enumerate(self.removedBlocks):
#
#
#                    if True in origins:
#                        if linkname == rlinkname and origins[i] == True:
#                            removedjoints.append(oldmotorJointNames[0])
#
#                    else:
#                        if self.links[linkname].parentLink != "none":
#                            removedjoints.append(f"{self.links[linkname].parentLink}_{linkname}")


#                print(self.namelist)
#                for i, linkname in enumerate(self.namelist):
#                    print(f"\n")
#                    print(linkname, self.links[linkname].connections)
                #print(self.removedBlocks)
                #print(oldparentsjoints)
                #print(removedjoints)
                motorindices0 = []

                for i, motor in enumerate(removedjoints):
                    
                    index = oldmotorJointNames.index(motor)
                    
                    motorindices0.append(index)
                
                #print(motorindices0)
                if len(motorindices0) == 1:
                    self.Add_Remove_Weight_Obj("remove",motorindices0[0],1)
                else:
                    motorindices0.sort(reverse=True)
                
                    for motorIndex in motorindices0:
                        self.Add_Remove_Weight_Obj("remove",motorIndex,1)




                
                self.motorJointNames = motorJointNames
                self.numMotors = len(self.motorJointNames)
                self.Define_Joint_Position()
                self.Define_Link_Position()
                #print(self.namelist)
                if failed is not True:
                    self.mutated = True
                    print(f"remove block {rlinkname}")
                    self.mutation = f"Removed link {rlinkname}. Changes: {changes}"
#                print(self.sensorNames)
#                print(len(self.sensorNames))
#                print(self.numSensors)
#                print(self.weights)
                #print("new num motors",self.numMotors)
                #print("new weights",len(self.weights),len(self.weights[0]))
                
                
                
                    
    def Change_Link_Dimension(self):
        whichDim = self.child_rng.integers(low=0, high=3)
        old = self.links[self.namelist[0]].dims[whichDim]
        newDim = 0
        while newDim != old:
            newDim = self.child_rng.integers(low=1, high=11)*0.1

        for linkname in self.links:
            self.links[linkname].Change_A_Dimension(newDim,whichDim)
        self.Define_Absolute_Link_Position()
        self.Define_Joint_Position()
        self.Define_Link_Position()
        #print("HELLO")
        #print(self.links[linkname].dims)
        self.mutated = True
        print("change dim")
        self.mutation = f"Changed dim: {whichDim}, Old: {old}, New = {newDim}"
        
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
        
        
