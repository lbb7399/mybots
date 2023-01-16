import numpy as np
import matplotlib.pyplot as plt

#backLegSensorValues = np.load('data/backLegSensorValues.npy')
#frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
#targetAngles = np.load('data/targetAngles.npy')
targetAnglesBack  = np.load('data/targetAnglesBack.npy')
targetAnglesFront = np.load('data/targetAnglesFront.npy')
#plt.plot(backLegSensorValues, label = "Back Leg", linewidth = 4)
#plt.plot(frontLegSensorValues, label = "Front Leg")

#plt.plot(targetAngles)
plt.plot(targetAnglesBack, label = "Back Leg", linewidth = 4)
plt.plot(targetAnglesFront, label = "Front Leg")
plt.legend()
plt.show()
