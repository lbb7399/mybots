import numpy as np
stepsiter = 1000

amplitudeBack = 4*np.pi/16
frequencyBack = 10
phaseOffsetBack = 0
maxForceBack = 30

amplitudeFront = 4*np.pi/16
frequencyFront = 10
phaseOffsetFront = 0
maxForceFront = 30


numberOfGenerations = 1
populationSize = 1

#numSensorNeurons = 2
#numMotorNeurons = 1

motorJointRange = 0.2

## body dimension random parameters (0.1 to 0.6)
#multiRandom = 0.5
#addRandom = 0.1

#numGenBody = 4
#numChildLow = 1
#numChildHigh = 2




# new random body constants
numXBlocks = 2 # solution constructor
numYBlocks = 2 # solution constructor
numZBlocks = 2 # solution constructor

# for now we are going to set the dimension size in link constructor and operate on the assumption that they are cubic and all the same. If they change (as in they are all different, equation in joint position and probs link position will need to be altered)
scale = 1/2
xDim = scale
yDim = scale
zDim = scale

# Starting coordinates used in link.py in Joint Position
x = 0
y = 0
z = zDim/2
coord = [x,y,z]
