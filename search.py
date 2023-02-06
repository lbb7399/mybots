from parallelHillClimber import PARALLEL_HILL_CLIMBER
import time

start_time = time.time()
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()
end_time = time.time()

print(end_time- start_time)
