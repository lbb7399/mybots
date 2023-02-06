from solution import SOLUTION
import constants as c
import copy
import os
import time
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm ballfitness*.txt")
        
        
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    
    def Evolve(self):
#        for i in range(c.populationSize):
#            self.parents[i].Start_Simulation("DIRECT")
#
#        for i in range(c.populationSize):
#            self.parents[i].Wait_For_Simulation_To_End()

        # instead:
        self.Evaluate(self.parents)
        
        
        for currentGeneration in range(c.numberOfGenerations):
            self.currentGen = currentGeneration
            self.Evolve_For_One_Generation()

            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
#        self.child.Evaluate("DIRECT") #old
        self.Evaluate(self.children)
    
#        print(f"Parent fit: {self.parent.fitness}, Child fit: {self.child.fitness}")
        self.Print()
        self.Select()
        
    
    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].SET_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
        
    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()
            
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
        for key in self.parents:
#            if self.children[key].fitness < self.parents[key].fitness:
#                self.parents[key] = self.children[key]
            
            if self.children[key].ballFitness > self.parents[key].ballFitness:
                self.parents[key] = self.children[key]
            
    def Show_Best(self):

        for i, key in enumerate(self.parents.keys()):
            if i == 0:
                bestfit = self.parents[key].fitness
                bestfitkey = key
            if self.parents[key].ballFitness > bestfit:
                bestfit = self.parents[key].fitness
                bestfitkey = key
            else:
                pass
        self.parents[bestfitkey].Start_Simulation("GUI")
        print(f"Best fit: {bestfit}")
        
