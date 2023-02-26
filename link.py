import constants as c
import random
import pyrosim.pyrosim as pyrosim
import numpy as np

class LINK:
    def __init__(self,linkID, exist,x,y,z):
        
        self.linkID = linkID
        self.exist = exist
        self.x = x
        self.y = y
        self.z = z
        
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
        flip = random.randint(1,2)
        if flip == 1:
            self.sensor = True
            self.color = "green"
        if flip == 2:
            self.sensor = False
            self.color = "blue"
    
    def Set_Number(self,number):
        self.num = number
        
    def Set_Joint_Axis(self):
        axes = ["x","y","z"]
        if self.num == 0:
            self.parentLink = "none"
            self.joint_axis = "none"
            self.joint_name = "none"
            
        else:
            print(self.numPossibleParents)
            if self.numPossibleParents == 1:
                self.parentLink = self.parentJointNames[0]
            else:
                index = random.randint(1,self.numPossibleParents) - 1
                self.parentLink = self.parentJointNames[index]
            self.joint_name = f"{self.parentLink}_{self.linkID}"
            if self.connections[self.parentLink][1] == "face":
                axisI = self.connections[self.parentLink][3].index(1)
                axes.pop(axisI)
                axis = random.randint(0,1)
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
    
    
    def Set_Joint_Position(self,type,parentAbsJoint):
        if type == "origin":
            self.joint_position = "none"
        elif type == "absolute":
            centerCoords = c.coord.copy()
            #print(f"Center: {centerCoords}")
            
            jointcoord = centerCoords + self.jointDir*-1*c.scale/2


            self.joint_position = jointcoord
            self.abs_joint_position = self.joint_position

        else:
            self.abs_joint_position = self.absLinkPos + self.jointDir*c.scale/2

            self.joint_position = self.abs_joint_position - parentAbsJoint
            self.abs_joint_position = self.joint_position
            
    def Set_Link_Position(self):
        print(self.linkID)
        if self.num == 0:
            self.linkpos = c.coord.copy()
            
        else:
            self.linkpos = self.absLinkPos - self.abs_joint_position
        

    def Send_Object(self):
        #print(f"Link Position {self.linkpos}{self.parentLink}{self.joint_name}")
        pyrosim.Send_Cube(name=self.linkID, pos=self.linkpos, size=self.dims, colorString=self.color)
        
    def Send_Joint(self):
        pyrosim.Send_Joint(name=self.joint_name, parent=f"{self.parentLink}", child=self.linkID, type="revolute",position=self.joint_position, jointAxis=self.joint_axis)


#        print(self.joint_position)



#    def Is_Origin(self, linkID):
#        if linkID == 0:
#            return True
#        else:
#            return False
#
#    def Set_Shape(self, parentShape):
#        self.parentShape = parentShape
#
##        flip = random.randint(1,2)
#        flip = 1
#        if flip == 1:
#            self.shape = "box"
#        if flip == 2:
#            self.shape = "sphere"
#
#
#    def Set_Dimensions(self, parentDims):
#        if self.shape == "box":
#            self.length = random.random()*c.multiRandom + c.addRandom
#            self.width = random.random()*c.multiRandom + c.addRandom
#            self.height = random.random()*c.multiRandom + c.addRandom
#            self.dims = [self.length,self.width,self.height]
#            self.axes["x"].append(self.dims[0])
#            self.axes["y"].append(self.dims[1])
#            self.axes["z"].append(self.dims[2])
#
#
#        elif self.shape == "sphere":
#            self.radius = random.random()*c.multiRandom/2 + c.addRandom/2
#            self.dims = self.radius
#            self.axes["x"].append(self.radius)
#            self.axes["y"].append(self.radius)
#            self.axes["z"].append(self.radius)
#
#        if self.parentShape == "sphere":
#            self.parentRadius = parentDims
#            self.axes["x"].append(self.parentRadius)
#            self.axes["y"].append(self.parentRadius)
#            self.axes["z"].append(self.parentRadius)
#
#        elif self.parentShape == "box":
#            self.axes["x"].append(parentDims[0])
#            self.axes["y"].append(parentDims[1])
#            self.axes["z"].append(parentDims[2])
#            self.parentDims = parentDims
#
#
#
#

#
#    def Set_Direction(self,direction,parentDirection,gparentDirection,parentInline):
#        self.direction = direction
#        self.parentDirection = parentDirection
#        self.parentInline = parentInline
#        self.gparentDirection = gparentDirection
#        self.direction_name, self.axis, self.sign = self.Direction_Name_and_Axis(self.direction)
#        self.parent_direction_name, self.parent_axis , self.parent_sign= self.Direction_Name_and_Axis(self.parentDirection)
#        self.gparent_direction_name, self.gparent_axis , self.gparent_sign= self.Direction_Name_and_Axis(self.gparentDirection)
#
#        print(self.linkID, self.shape, self.direction_name, self.dims)
#
#        if self.Is_Origin(self.linkID):
#            self.inline = "none"
#        elif self.Is_Origin(self.parentID):
#            self.inline = True
#        else:
#            if self.parentShape == "sphere":
#                self.inline = True
#            elif self.axis == self.parent_axis:
#                self.inline = True
#            else:
#                self.inline = False
#
#
#
#
#    def Direction_Name_and_Axis(self, direction):
#        if direction == 1:
#            direction_name = "x"
#            axis = "x"
#            sign = 1
#        if direction == 2:
#            direction_name = "-x"
#            axis = "x"
#            sign = -1
#        if direction == 3:
#            direction_name = "y"
#            axis = "y"
#            sign = 1
#        if direction == 4:
#            direction_name = "-y"
#            axis = "y"
#            sign = -1
#        if direction == 5:
#            direction_name = "z"
#            axis = "z"
#            sign = 1
#        if direction == 6:
#            direction_name = "-z"
#            axis = "z"
#            sign = -1
#        if direction == "none":
#            direction_name = "origin"
#            axis = "origin"
#            sign = "none"
#        return direction_name, axis, sign
#
#    def Set_Joint_Axis(self):
#        axes = ["x", "y","z"]
#        if self.Is_Origin(self.linkID):
#            self.joint_axis = "none"
#
#        elif self.Is_Origin(self.parentID):
#            axes.remove(self.axis)
#            axis = random.randint(0,1)
#            self.joint_axis = self.Return_Axis(axes[axis])
#        else:
#            if self.parentShape == "box":
#                if self.parent_axis == self.axis:
#                    axes.remove(self.axis)
#                    axis = random.randint(0,1)
#                    self.joint_axis = self.Return_Axis(axes[axis])
#                else:
#                    axes.remove(self.axis)
#                    axes.remove(self.parent_axis)
#                    self.joint_axis = self.Return_Axis(axes[0])
#            elif self.parentShape == "sphere":
#                axes.remove(self.axis)
#                axis = random.randint(0,1)
#                self.joint_axis = self.Return_Axis(axes[axis])
#

#
##    def Set_Origin_Position(self):
##        self.position = c.coord
#
#    def Set_Joint_Position(self):
#        if self.Is_Origin(self.linkID):
#            self.joint_position = "none"
#        elif self.Is_Origin(self.parentID):
#            centerCoords = c.coord.copy()
#            print(f"Center: {centerCoords}")
#
#            if self.parentShape == "sphere":
#                centerCoords[self.axes[self.axis][0]] += self.sign*self.parentRadius
#            elif self.parentShape == "box":
#                centerCoords[self.axes[self.axis][0]] += self.sign*self.axes[self.axis][2]/2
#
#
#            self.joint_position = centerCoords
#
#        else:
#            joint_position = [0,0,0]
#            if self.parentShape == "sphere":
#                joint_position[self.axes[self.parent_axis][0]] += self.parent_sign*self.parentRadius
#                joint_position[self.axes[self.axis][0]] += self.sign*self.parentRadius
#            elif self.parentShape == "box":
#                joint_position[self.axes[self.parent_axis][0]] += self.parent_sign*self.axes[self.parent_axis][2]
#
## nothing                if self.parentInline and self.inline:
#                if self.parentInline is True and self.inline is False:
#                    joint_position[self.axes[self.axis][0]] += self.sign*self.axes[self.axis][2]/2
#                if self.parentInline is False and self.inline is True:
#                    joint_position[self.axes[self.gparent_axis][0]] += self.gparent_sign*self.axes[self.gparent_axis][2]/2
#
#            self.joint_position = joint_position
#
#
#
#
##        print(self.joint_position)
#
#    def Set_Link_Position(self):
#        if self.Is_Origin(self.linkID):
#            self.link_position = c.coord.copy()
#
#
#        else:
#            link_position = [0,0,0]
#            if self.shape is "sphere":
#                link_position[self.axes[self.axis][0]] += self.sign*self.radius
#            elif self.shape is "box":
#                link_position[self.axes[self.axis][0]] += self.sign*self.axes[self.axis][1]/2
#                if self.inline is False:
#                    link_position[self.axes[self.parent_axis][0]] += self.parent_sign*self.axes[self.parent_axis][1]/2
#            self.link_position = link_position
#

            


            
                
            
            
            
