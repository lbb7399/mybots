import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
targetAngles = np.load('data/targetAngles.npy')

#plt.plot(backLegSensorValues, label = "Back Leg", linewidth = 4)
#plt.plot(frontLegSensorValues, label = "Front Leg")
#plt.legend()
plt.plot(targetAngles)
plt.show()
