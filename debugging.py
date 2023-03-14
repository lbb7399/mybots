import pickle
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from numpy.random import SeedSequence, default_rng
import constants as c
import numpy as np
from statistics import median,mean
from scipy.stats import ttest_ind
#ss = SeedSequence(100)
#phc = PARALLEL_HILL_CLIMBER(ss,1)
#parents = pickle.load( open( "save_parents34.p", "rb" ) )
#phc.Evolve()
#phc.Show_Best()

#parent1 = pickle.load( open( "pickles/6/save_parents6-81.p", "rb" ) )
#parent2 = pickle.load( open( "pickles/6/save_parents6-82.p", "rb" ) )
#print(parent[1].namelist)
#print(parent[1].motorJointNames,parent[1].numMotors,len(parent[1].motorJointNames))
#print(parent1[3].motorJointNames)
#print(parent2[3].motorJointNames)
#parent2[3].links["002"].Set_Parent(parent="none")
#parent2[3].Mutate_Remove_Block(link="101")
#print(parent2[3].motorJointNames)
#print(len(parent2[3].weights),len(parent2[3].weights[0]))
#print(parent2[8].namelist0)
#print(parent2[8].canExistButDoesnt)
#parent2[8].Mutate_Add_Block(link="000")





for i, runNum in enumerate(c.runnumberstot):
    print(runNum)
    maxFitness = np.zeros(c.numberOfGenerations+1)
    minFitness = np.zeros(c.numberOfGenerations+1)
    medFitness = np.zeros(c.numberOfGenerations+1)
    avgFitness = np.zeros(c.numberOfGenerations+1)
    allFitness = {}
    for i in range(c.populationSize):
        allFitness[i] = []

    for currentGeneration in range(c.numberOfGenerations+1):
        currentGen = currentGeneration
        parents = pickle.load( open( f"pickles/{runNum}/save_parents{runNum}-{currentGen}.p", "rb" ) )
        fitnesses = []
        for i, key in enumerate(parents.keys()):
            if currentGen != 0:
                allFitness[key].append(parents[key].fitness)
            fitnesses.append(parents[key].fitness)
            if i == 0:
                bestfit = parents[key].fitness
                worstfit = parents[key].fitness
                bestfitkey = key
                worstfitkey = key
            if parents[key].fitness < bestfit:
                bestfit = parents[key].fitness
                bestfitkey = key
            if parents[key].fitness > worstfit:
                worstfit = parents[key].fitness
                worstfitkey = key

        medfit = median(fitnesses)
        avgfit = mean(fitnesses)

        maxFitness[currentGen] = -1*bestfit
        minFitness[currentGen] = -1*worstfit
        medFitness[currentGen] = -1*medfit
        avgFitness[currentGen] = -1*avgfit
    maxfilename = f"data/maxfitnesscurve{runNum}.npy"
    minfilename = f"data/minfitnesscurve{runNum}.npy"
    medianfilename = f"data/medianfitnesscurve{runNum}.npy"
    avgfilename = f"data/avgfitnesscurve{runNum}.npy"
    np.save(maxfilename, maxFitness)
    np.save(minfilename, minFitness)
    np.save(medianfilename, medFitness)
    np.save(avgfilename, avgFitness)
    
    muts = pickle.load( open( f"pickles/{runNum}/save_mutations{runNum}-{c.numberOfGenerations}.p", "rb" ) )
    for i in range(c.populationSize):
        muts[f"{i}Fit"] = allFitness[i]
    
    pickle.dump(muts, open(f"pickles/{runNum}/save_mutations{runNum}-{c.numberOfGenerations}-fit.p", "wb"))
    



rand_fitness = []
rand_best_fit = []
seq_fitness = []
seq_best_fit = []
best_fit_keys = {}
for i, runNum in enumerate(c.runnumberstot):
    parents = pickle.load( open( f"pickles/{runNum}/save_parents{runNum}-{c.numberOfGenerations}.p", "rb" ) )
    if runNum <= 5:
        for j,key in enumerate(parents.keys()):
            rand_fitness.append(parents[key].fitness)
            if j == 0:
                bestfit = parents[key].fitness
                bestfitkey = key
            if parents[key].fitness < bestfit:
                bestfit = parents[key].fitness
                bestfitkey = key
        rand_best_fit.append(bestfit)
    else:
        for j,key in enumerate(parents.keys()):
            seq_fitness.append(parents[key].fitness)
            if j == 0:
                bestfit = parents[key].fitness
                bestfitkey = key
            if parents[key].fitness < bestfit:
                bestfit = parents[key].fitness
                bestfitkey = key
        seq_best_fit.append(bestfit)
    best_fit_keys[runNum] = bestfitkey

pickle.dump(best_fit_keys, open(f"pickles/save_bestkeys.p", "wb"))
            
print(ttest_ind(a=rand_fitness,b=seq_fitness,equal_var=False))
print(ttest_ind(a=rand_best_fit,b=seq_best_fit,equal_var=False))
print(best_fit_keys)
