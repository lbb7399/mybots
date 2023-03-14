from solution import SOLUTION
import constants as c
import copy
import os
from numpy.random import SeedSequence, default_rng
import numpy as np
import pickle
class PARALLEL_HILL_CLIMBER:
    def __init__(self, ss, runNumber):
        
        os.system("rm files/brain*.nndf")
        os.system("rm files/fitness*.txt")
        os.system("rm files/body*.urdf")
        

        self.ss = ss
        child_seeds = ss.spawn(c.populationSize)
        self.runNumber = runNumber
        self.allFitness = np.zeros(c.numberOfGenerations+1)
        self.parents = {}
        self.mutations = {"generation": []}
        self.info = ["Success","Type","Specifics"]
        
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID,i,child_seeds[i])
            self.nextAvailableID = self.nextAvailableID + 1
            for j, thing in enumerate(self.info):
                key = f"{i}{thing}"
                self.mutations[key] = [0]*c.numberOfGenerations
                
        
            
        

    
    def Evolve(self):
#        for i in range(c.populationSize):
#            self.parents[i].Start_Simulation("DIRECT")
#
#        for i in range(c.populationSize):
#            self.parents[i].Wait_For_Simulation_To_End()

        # instead:
        self.Evaluate(self.parents)
        
        self.currentGen = 0
        pickle.dump(self.parents, open(f"pickles/{self.runNumber}/save_parents{self.runNumber}-{self.currentGen}.p", "wb"))
        self.Pick_Fitness()

        
        counter = 1
        self.mutType = "mind"
        for currentGeneration in range(c.numberOfGenerations):
            self.currentGen = currentGeneration + 1
            self.mutations["generation"].append(self.currentGen)
            self.Evolve_For_One_Generation()
            counter += 1
            if counter == 51:
                self.mutType = "body"
            if counter == 101:
                self.mutType = "mind"
                counter = 1

            
        fitfilename = f"data/fitnesscurve{self.runNumber}.npy"
        np.save(fitfilename, self.allFitness)
        pickle.dump(self.mutations, open(f"pickles/{self.runNumber}/save_mutations{self.runNumber}-{self.currentGen}.p", "wb"))

            
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
        self.attemptedmuts = []
        self.mutnums = []
        for key in self.children:
            mutated = False
            copyofSolution = copy.deepcopy(self.children[key])
            while mutated == False:
                if self.runNumber <= 5:
                    self.children[key].Mutate()
                else:
                    if self.mutType == "mind":
                        self.children[key].Mutate_Mind()
                    elif self.mutType == "body":
                        self.children[key].Mutate_Body()
                
                mutated = self.children[key].mutated
                mutNum = self.children[key].mutNum
                if mutated is False and mutNum in c.problemMutations:
                    new_seed = self.ss.spawn(1)
                    self.children[key] = copy.deepcopy(copyofSolution)
                    self.children[key].New_Seed(new_seed[0])
                    print("copied")
                    #print(self.children[key].namelist)
                elif mutated is True:
                    del copyofSolution
                    key1 = f"{key}{self.info[1]}"
                    key2 = f"{key}{self.info[2]}"
                    self.mutations[key1][self.currentGen-1] = self.children[key].mutNum
                    self.mutations[key2][self.currentGen-1] = self.children[key].mutation
                    
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

            key1 = f"{key}{self.info[0]}"
            if self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]
                self.mutations[key1][self.currentGen-1] = "True"
            else:
                self.parents[key].New_Seed(child2_seeds[count])
                self.mutations[key1][self.currentGen-1] = "False"
            count += 1
        
        os.system(f"rm pickles/{self.runNumber}/save_mutations{self.runNumber}-{self.currentGen-1}.p")
        pickle.dump(self.mutations, open(f"pickles/{self.runNumber}/save_mutations{self.runNumber}-{self.currentGen}.p", "wb"))
        pickle.dump(self.parents, open(f"pickles/{self.runNumber}/save_parents{self.runNumber}-{self.currentGen}.p", "wb"))
                
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
        
        
    def Load_Pickle(self,parents):
        self.parents = parents
        
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
        
        pickle.dump(self.parents, open(f"pickles/{self.runNumber}/save_final{self.runNumber}-{self.currentGen}.p", "wb"))
        pickle.dump(self.parents[bestfitkey], open(f"pickles/{self.runNumber}/save_bestfinal{self.runNumber}-{self.currentGen}.p", "wb"))
        self.parents[bestfitkey].Start_Simulation("GUI")
        print(f"Best fit: {bestfit}")
        

