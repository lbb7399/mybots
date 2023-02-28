import pickle
import constants as c


#parents = pickle.load( open( "save_parentsfinal1.p", "rb" ) )
#for i in range(c.populationSize):
#    parents[i].Start_Simulation("DIRECT")
#
#
#for i in range(c.populationSize):
#    parents[i].Wait_For_Simulation_To_End()
#
#for i, key in enumerate(parents.keys()):
#    if i == 0:
#        bestfit = parents[key].fitness
#        bestfitkey = key
#    if parents[key].fitness < bestfit:
#        bestfit = parents[key].fitness
#        bestfitkey = key
#    else:
#        pass
#
#
#parents[bestfitkey].Start_Simulation("GUI")
#print(f"Best fit: {bestfit}")

parents = pickle.load( open( "save_parentsfinal1-0.p", "rb" ) )

parents.Start_Simulation("GUI")


#parents[bestfitkey].Start_Simulation("GUI")
print(f"Best fit: {parents.fitness}")
