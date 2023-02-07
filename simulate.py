import sys
from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
print(solutionID)


simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()
