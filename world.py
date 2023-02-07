import pybullet as p
import pybullet_data
class WORLD:
    def __init__(self):
       
        
        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF("world.sdf")
    
    def Get_Ball_Position(self):
        posAndOrientation = p.getBasePositionAndOrientation(self.objects[0])
        position = posAndOrientation[0]
#        xPosition = position[0]
#        yPosition = position[1]
#        height = position[2]
        return position
