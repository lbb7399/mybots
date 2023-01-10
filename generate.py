import pyrosim.pyrosim as pyrosim
pyrosim.Start_SDF("world.sdf")
length0 = 1
width0 = 1
height0 = 1
x = 0
y = 0
z = 0.5
pyrosim.Send_Cube(name= "Box", pos=[x,y,z] , size=[length,width,height])
pyrosim.End()
