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


numberOfGenerations = 0
populationSize = 1

#numSensorNeurons = 2
#numMotorNeurons = 1

motorJointRange = 0.2

# body dimension random parameters (0.1 to 0.6)
multiRandom = 0.5
addRandom = 0.1

numGenBody = 4
numChildLow = 1
numChildHigh = 2

# Starting coordinates
x = 0
y = 0
z = 2
coord = [x,y,z]
