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

num = 10
best = 9
gen = 500
parents = pickle.load( open( f"pickles/{num}/save_parents{num}-{gen}.p", "rb" ) )

parents[best].Start_Simulation("GUI")
#print(parents[9].namelist,parents[9].numLinks)
#
#print(parents[9].sensorNames,parents[9].numSensors)
#print(parents[9].motorJointNames,parents[9].numMotors)
#print(parents[9].links[parents[9].namelist[0]].dims)
#
#for i,linkname in enumerate(parents[9].namelist):
#    print(linkname, parents[9].links[linkname].absLinkPos, parents[9].links[linkname].color )

#parents[bestfitkey].Start_Simulation("GUI")
#print(f"Best fit: {parents.fitness}")

