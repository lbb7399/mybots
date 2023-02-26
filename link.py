import constants as c
import random
import pyrosim.pyrosim as pyrosim
import numpy as np

class LINK:
    def __init__(self,linkID, exist,x,y,z,gchild_seed):
        
        self.linkID = linkID
        self.exist = exist
        self.x = x
        self.y = y
        self.z = z
        self.gchild_rng = np.random.default_rng(gchild_seed)
        
        self.connections = {}
        self.parentJointNames = []
        self.childJointNames = []
        
        self.xDim = c.xDim
        self.yDim = c.yDim
        self.zDim = c.zDim
        self.dims = [self.xDim,self.yDim,self.zDim]
#        self.parentID = parentID
#        self.numChildren = numChildren
#        self.joint_name = f"{parentID}_{linkID}"
#        self.axes = {
#            "x": [0],
#            "y": [1],
#            "z": [2]
#        }
#

    def Set_Existance(self,existance):
        self.exist = existance
        
    def Add_Joint(self,conName,relativePos,jointRelative,jointOrient):
        jointDirRelativeToLink = [0,0,0]
        axisRelativeToLink = [0,0,0]
        for i,x in enumerate(relativePos):
            if x == 0:
                jointDirRelativeToLink[i] = -1
                axisRelativeToLink[i] = 1
            elif x == 2:
                jointDirRelativeToLink[i] = 1
                axisRelativeToLink[i] = 1
            
        if jointRelative == "parent":
            self.parentJointNames.append(conName)
        else:
            self.childJointNames.append(conName)
        
        self.numPossibleParents = len(self.parentJointNames)
        self.jointDir = np.array(jointDirRelativeToLink)
        self.connections[conName] = [jointRelative,jointOrient,jointDirRelativeToLink,axisRelativeToLink]

    def Set_Sensor(self):
        #flip = random.randint(1,2)
        flip = self.gchild_rng.integers(low=1, high=3)
        if flip == 1:
            self.sensor = True
            self.color = "green"
        if flip == 2:
            self.sensor = False
            self.color = "blue"
            
    def Switch_Sensor(self):
        if self.sensor == True:
            self.sensor = False
            self.color = "blue"
        else:
            self.sensor = True
            self.color = "green"
    
    def Set_Number(self,number):
        self.num = number
        
    def Set_Joint_Axis(self):
        axes = ["x","y","z"]
        if self.num == 0:
            self.parentLink = "none"
            self.joint_axis = "none"
            self.joint_name = "none"
            self.jointOrient = "none"
            self.jointDir = "none"
            
        else:
            print(self.numPossibleParents)
            if self.numPossibleParents == 1:
                self.parentLink = self.parentJointNames[0]
            else:
                #index = random.randint(1,self.numPossibleParents) - 1
                index = self.gchild_rng.integers(low=1,high=self.numPossibleParents+1) - 1
                self.parentLink = self.parentJointNames[index]
            self.jointOrient = self.connections[self.parentLink][1]
            self.jointDir = np.array(self.connections[self.parentLink][2])
            self.joint_name = f"{self.parentLink}_{self.linkID}"
            if self.connections[self.parentLink][1] == "face":
                axisI = self.connections[self.parentLink][3].index(1)
                axes.pop(axisI)
                #axis = random.randint(0,1)
                axis = self.gchild_rng.integers(low=0,high=2)
                self.joint_axis = self.Return_Axis(axes[axis])
            elif self.connections[self.parentLink][1] == "hinge":
                axis = self.connections[self.parentLink][3].index(0)
                self.joint_axis = self.Return_Axis(axes[axis])
                
    def Return_Axis(self,axis):
        if axis == "x":
            joint_axis = "1 0 0"
        elif axis == "y":
            joint_axis = "0 1 0"
        elif axis == "z":
            joint_axis = "0 0 1"
        return joint_axis
                
    def Reset_Lists(self):
        self.connections = {}
        self.parentJointNames = []
        self.childJointNames = []
    
    
    def Set_Absolute_Link_Position(self):
        self.absx = self.x*c.scale
        self.absy = self.y*c.scale
        self.absz = self.z*c.scale + self.zDim/2
        
        self.absLinkPos = [self.absx,self.absy,self.absz]
    
    
    def Set_Joint_Position(self,type,parentAbs):
        if type == "origin":
            self.joint_position = "none"
            self.abs_joint_position = "none"
        elif type == "absolute":
            centerCoords = np.array(parentAbs)
            #print(f"Center: {centerCoords}")
            
            jointcoord = centerCoords + self.jointDir*-1*c.scale/2


            self.joint_position = jointcoord
            self.abs_joint_position = self.joint_position

        else:
            self.abs_joint_position = self.absLinkPos + self.jointDir*c.scale/2

            self.joint_position = self.abs_joint_position - parentAbs
            
    def Set_Link_Position(self):
        print(self.linkID)
        if self.num == 0:
            self.linkpos = self.absLinkPos
            
        else:
            self.linkpos = self.absLinkPos - self.abs_joint_position
        

    def Send_Object(self):
        #print(f"Link Position {self.linkpos}{self.parentLink}{self.joint_name}")
        pyrosim.Send_Cube(name=self.linkID, pos=self.linkpos, size=self.dims, colorString=self.color)
        
    def Send_Joint(self):
        pyrosim.Send_Joint(name=self.joint_name, parent=f"{self.parentLink}", child=self.linkID, type="revolute",position=self.joint_position, jointAxis=self.joint_axis)



