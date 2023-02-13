import constants as c
import random

class LINK:
    def __init__(self,linkID, parentID, numChildren):
        self.linkID = linkID
        self.parentID = parentID
        self.numChildren = numChildren
        
    def Is_Origin(self, linkID):
        if linkID == 0:
            return True
        else:
            return False
        
    def Set_Shape(self, parentShape):
        self.parentShape = parentShape
    
        flip = random.randint(1,2)
        if flip == 1:
            self.shape = "box"
        if flip == 2:
            self.shape = "sphere"

    
    def Set_Dimensions(self, parentDims):
        if self.shape == "box":
            self.length = random.random()*c.multiRandom + c.addRandom
            self.width = random.random()*c.multiRandom + c.addRandom
            self.height = random.random()*c.multiRandom + c.addRandom
            self.dims = [self.length,self.width,self.height]
        
        elif self.shape == "sphere":
            self.radius = random.random()*c.multiRandom/2 + c.addRandom/2
            self.dims = self.radius
        
        if self.parentShape == "sphere":
            self.parentRadius = parentDims
            
        elif self.parentShape == "box":
            self.parentLength = parentDims[0]
            self.parentWidth = parentDims[1]
            self.parentHeight = parentDims[2]
            self.parentDims = parentDims
            

            
            
    def Set_Sensor(self):
        flip = random.randint(1,2)
        if flip == 1:
            self.sensor = True
            self.color = "green"
        if flip == 2:
            self.sensor = False
            self.color = "blue"
            
    def Set_Direction(self,direction,parentDirection):
        self.direction = direction
        self.parentDirection = parentDirection
        self.direction_name, self.axis, self.sign = self.Direction_Name_and_Axis(self.direction)
        self.parent_direction_name, self.parent_axis , self.parent_sign= self.Direction_Name_and_Axis(self.parentDirection)
        print(self.linkID, self.shape, self.direction_name, self.dims)
        

    
    def Direction_Name_and_Axis(self, direction):
        if direction == 1:
            direction_name = "x"
            axis = "x"
            sign = 1
        if direction == 2:
            direction_name = "-x"
            axis = "x"
            sign = -1
        if direction == 3:
            direction_name = "y"
            axis = "y"
            sign = 1
        if direction == 4:
            direction_name = "-y"
            axis = "y"
            sign = -1
        if direction == 5:
            direction_name = "z"
            axis = "z"
            sign = 1
        if direction == 6:
            direction_name = "-z"
            axis = "z"
            sign = -1
        if direction == "none":
            direction_name = "origin"
            axis = "origin"
            sign = "none"
        return direction_name, axis, sign
        
    def Set_Joint_Axis(self):
        axes = ["x", "y","z"]
        if self.Is_Origin(self.linkID):
            self.joint_axis = "none"
        
        elif self.Is_Origin(self.parentID):
            axes.remove(self.axis)
            axis = random.randint(0,1)
            self.joint_axis = self.Return_Axis(axes[axis])
        else:
            if self.parentShape == "box":
                if self.parent_axis == self.axis:
                    axes.remove(self.axis)
                    axis = random.randint(0,1)
                    self.joint_axis = self.Return_Axis(axes[axis])
                else:
                    axes.remove(self.axis)
                    axes.remove(self.parent_axis)
                    self.joint_axis = self.Return_Axis(axes[0])
            elif self.parentShape == "sphere":
                axes.remove(self.axis)
                axis = random.randint(0,1)
                self.joint_axis = self.Return_Axis(axes[axis])

    def Return_Axis(self,axis):
        if axis == "x":
            joint_axis = "1 0 0"
        elif axis == "y":
            joint_axis = "0 1 0"
        elif axis == "z":
            joint_axis = "0 0 1"
        return joint_axis
    
#    def Set_Origin_Position(self):
#        self.position = c.coord
    
    def Set_Joint_Position(self):
        if self.Is_Origin(self.linkID):
            self.joint_position = "none"
        elif self.Is_Origin(self.parentID):
            centerCoords = c.coord.copy()
            print(centerCoords)
            if self.parentShape == "sphere":
                if self.axis == "x":
                    centerCoords[0] += self.sign*self.parentRadius
                elif self.axis == "y":
                    centerCoords[1] += self.sign*self.parentRadius
                elif self.axis == "z":
                    centerCoords[2] += self.sign*self.parentRadius
            elif self.parentShape == "box":
                if self.axis == "x":
                    centerCoords[0] += self.sign*self.parentLength/2
                elif self.axis == "y":
                    centerCoords[1] += self.sign*self.parentWidth/2
                elif self.axis == "z":
                    centerCoords[2] += self.sign*self.parentHeight/2
                
            self.joint_position = centerCoords
            
        else:
            if self.parentShape == "sphere":
                
            
            print(self.joint_position)
            


            
                
            
            
            
