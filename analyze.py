import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load('data/backLegSensorValues.npy')
frontLegSensorValues = numpy.load('data/frontLegSensorValues.npy')

plt.plot(backLegSensorValues, label = "Back Leg", linewidth = 4)
plt.plot(frontLegSensorValues, label = "Front Leg")
plt.legend()
plt.show()
