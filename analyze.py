import numpy as np
import matplotlib.pyplot as plt
import constants as c
from time import sleep
import os


colors = ['b','g','r','m','k']
linetype = ['-','--']
count = 0
plt.figure(num=count)
count += 1
for i, runNum in enumerate(c.runnumberstot):
    f = f"data/maxfitnesscurve{runNum}.npy"
    while not os.path.exists(f):
        sleep(0.01)
    loadedfile  = np.load(f)
    if runNum <= 5:
        style = colors[i] + linetype[0]
    else:
        style = colors[i-5] + linetype[1]
    plt.plot(loadedfile, style,label = f"{runNum}")

plt.title("Best Fitness Evolution")
plt.xlabel("Generations")
plt.ylabel("Distance from Origin in -x Direction")
plt.legend()
#plt.show()
plt.savefig("figures/Evolution Curve.png")

x = np.arange(c.numberOfGenerations+1)
stats = ["max","min","median"]
for i,color in enumerate(colors):
    plt.figure(num=count)
    count += 1
    
    loadfile1 = []
    loadfile2 = []
    for j, stat in enumerate(stats):
        f1 = f"data/{stat}fitnesscurve{i+1}.npy"
        f2 = f"data/{stat}fitnesscurve{i+6}.npy"
        loadfile1.append(np.load(f1))
        loadfile2.append(np.load(f2))
    style1 = 'b' + linetype[0]
    plt.plot(loadfile1[2], style1,label = "Random")
    plt.fill_between(x,loadfile1[1],loadfile1[0], alpha=0.5, color='tab:blue')


    #f2 = f"data/maxfitnesscurve{i+6}.npy"
    #loadfile2 = np.load(f2)
    style2 = 'k' + linetype[1]
    plt.plot(loadfile2[2], style2,label = "Sequential")
    plt.fill_between(x,loadfile2[1],loadfile2[0], alpha = 0.5, color='tab:gray')
    #loadfile2.close()
    plt.title(f"Seed {i+1} (Runs {i+1} and {i+6})")
    plt.xlabel("Generations")
    plt.ylabel("Distance from Origin in -x Direction")
    plt.legend()
    #plt.show()
    plt.savefig(f"figures/Seed {i+1} Evolution Curve.png")
    
    plt.figure(num=count)
    count += 1
    plt.plot(loadfile1[0], style1,label = "Random")
    plt.plot(loadfile2[0], style2,label = "Sequential")
    plt.title(f"Largest Fitness: Seed {i+1} (Runs {i+1} and {i+6})")
    plt.xlabel("Generations")
    plt.ylabel("Distance from Origin in -x Direction")
    plt.legend()
    #plt.show()
    plt.savefig(f"figures/Seed {i+1} Max Evolution Curve.png")
