import pyrosim.pyrosim as pyrosim
pyrosim.Start_SDF("boxes.sdf")
length0 = 1
width0 = 1
height0 = 1
x0 = -2
y0 = -2
z0 = 0.5
for k in range(5):
    x = x0 + k
    for j in range(5):
        y = y0 + j
        for i in range(10):
            z = z0 + i
            length = length0*(0.9**i)
            width = width0*(0.9**i)
            height = height0*(0.9**i)
            
            pyrosim.Send_Cube(name= f"Box{k}{j}{i}", pos=[x,y,z] , size=[length,width,height])

pyrosim.End()
