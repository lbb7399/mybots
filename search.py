from parallelHillClimber import PARALLEL_HILL_CLIMBER
from numpy.random import SeedSequence, default_rng

ss = SeedSequence(100)

phc = PARALLEL_HILL_CLIMBER(ss)
phc.Evolve()
phc.Show_Best()
