import numpy as np
import matplotlib.pyplot as plt
import constants as c



for i, runNum in enumerate(c.runnumbers):
    loadedfile  = np.load(f"data/fitnesscurve{runNum}.npy")
    plt.plot(loadedfile, label = f"{runNum}")

plt.legend()
plt.show()

