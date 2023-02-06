from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time
import constants as c

start_time = time.time()
phcs = {}
for i in range(c.bodyGen):
    phcs[i] = PARALLEL_HILL_CLIMBER()
    phcs[i].Evolve()
    phcs[i].Show_Best()


end_time = time.time()

print(end_time- start_time)
