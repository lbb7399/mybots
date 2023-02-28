import pickle
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from numpy.random import SeedSequence, default_rng
ss = SeedSequence(100)
phc = PARALLEL_HILL_CLIMBER(ss,1)
parents = pickle.load( open( "save_parents34.p", "rb" ) )
phc.Evolve()
phc.Show_Best()

