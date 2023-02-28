from solution import SOLUTION
import constants as c
import copy
import os
from numpy.random import SeedSequence, default_rng
import numpy as np
class PARALLEL_HILL_CLIMBER:
    def __init__(self, ss, runNumber):
        
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")

        self.ss = ss
        child_seeds = ss.spawn(c.populationSize)
        self.runNumber = runNumber
        self.allFitness = np.zeros(c.numberOfGenerations+1)
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID,i,child_seeds[i])
            self.nextAvailableID = self.nextAvailableID + 1

    
    def Evolve(self):
#        for i in range(c.populationSize):
#            self.parents[i].Start_Simulation("DIRECT")
#
#        for i in range(c.populationSize):
#            self.parents[i].Wait_For_Simulation_To_End()

        # instead:
        self.Evaluate(self.parents)
        self.currentGen = 0
        self.Pick_Fitness()

        
        
        for currentGeneration in range(c.numberOfGenerations):
            self.currentGen = currentGeneration + 1
            self.Evolve_For_One_Generation()
            
        fitfilename = f"data/fitnesscurve{self.runNumber}.npy"
        np.save(fitfilename, self.allFitness)

            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
#        self.child.Evaluate("DIRECT") #old
        self.Evaluate(self.children)
    
#        print(f"Parent fit: {self.parent.fitness}, Child fit: {self.child.fitness}")
        self.Print()
        self.Select()
        self.Pick_Fitness()
        
    
    def Spawn(self):
        self.children = {}


        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].SET_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

        
    def Mutate(self):

        for key in self.children:
            mutated = False
            copyofSolution = copy.deepcopy(self.children[key])
            while mutated == False:
                self.children[key].Mutate()
                mutated = self.children[key].mutated
                mutNum = self.children[key].mutNum
                if mutated is False and mutNum in c.problemMutations:
                    self.children[key] = copyofSolution
                elif mutated is True:
                    del copyofSolution
                else:
                    print("cycle")
            
    def Evaluate(self, solutions):
        
        
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        
            
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End()
        
            
    def Print(self):
        print(f"\n")
        print(f"Generation {self.currentGen}")
        for key in self.parents:
            print(f"ID: {key} Parent fit: {self.parents[key].fitness} Child fit: {self.children[key].fitness}")
        print(f"\n")
    
    def Select(self):
        child2_seeds = self.ss.spawn(c.populationSize)
        count = 0
        for key in self.parents:
            if self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]
            else:
                self.parents[key].New_Seed(child2_seeds[count])
            count += 1
                
    def Pick_Fitness(self):
        for i, key in enumerate(self.parents.keys()):
            if i == 0:
                bestfit = self.parents[key].fitness
                bestfitkey = key
            if self.parents[key].fitness < bestfit:
                bestfit = self.parents[key].fitness
                bestfitkey = key
        bestfitness = self.parents[bestfitkey].fitness
        self.allFitness[self.currentGen] = abs(bestfitness)
        
            
    def Show_Best(self):
#        self.parent.Evaluate("GUI")

        for i, key in enumerate(self.parents.keys()):
            if i == 0:
                bestfit = self.parents[key].fitness
                bestfitkey = key
            if self.parents[key].fitness < bestfit:
                bestfit = self.parents[key].fitness
                bestfitkey = key
            else:
                pass
        self.parents[bestfitkey].Start_Simulation("GUI")
        print(f"Best fit: {bestfit}")
        

