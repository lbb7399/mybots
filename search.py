from parallelHillClimber import PARALLEL_HILL_CLIMBER
from numpy.random import SeedSequence, default_rng
from os import system
import constants as c

system("rm data/fitnesscurve*.npy")
for i, runNum in enumerate(c.runnumbers):
    seedNumber = runNum*100
    ss = SeedSequence(seedNumber)

    phc = PARALLEL_HILL_CLIMBER(ss,runNum)
    phc.Evolve()
    phc.Show_Best()


# out of loop


system("python3 analyze.py")
