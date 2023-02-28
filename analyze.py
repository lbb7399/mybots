import numpy as np
import matplotlib.pyplot as plt
import constants as c
from time import sleep
import os



for i, runNum in enumerate(c.runnumberstot):
    f = f"data/fitnesscurve{runNum}.npy"
    while not os.path.exists(f):
        sleep(0.01)
    loadedfile  = np.load(f)
    plt.plot(loadedfile, label = f"{runNum}")
plt.title("Fitness Evolution")
plt.xlabel("Generations")
plt.ylabel("Distance from Origin in -x Direction")
plt.legend()
plt.show()
plt.savefig("Evolution Curve.png")
