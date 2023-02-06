from solution import SOLUTION
import constants as c
import copy
import os
import time
import random
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm ballfitness*.txt")
        
        
        # define body dimensions
        self.dimensions = [0.8,0.15,0.15,1,0.5,0.3]
        self.goalZPos = self.dimensions[0]
        self.lDim = self.dimensions[1:3]
        self.tDim = self.dimensions[3:6]
        
#        self.goalZPos = random.random()*1.5 + 0.5
#
#        llength = random.random()/10 + 0.1
#        lwidth = random.random()/10 + 0.1
#
#        self.lDim = [llength,lwidth]
#
#        tlength = random.random()*1.5 + 0.5
#        twidth = random.random()/2 + 0.3
#        theight = random.random()*3/4 + 0.25
#
#        self.tDim = [tlength,twidth,theight]
        

        
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID, self.goalZPos, self.lDim, self.tDim)
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
            start_time = time.time()
            self.currentGen = currentGeneration
            self.Evolve_For_One_Generation()
            print(time.time()-start_time)

            
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
            print(f"ID: {key} Parent fit: {self.parents[key].ballFitness} Child fit: {self.children[key].ballFitness}")
            #print(f"ID: {key} Parent ball fit: {self.parents[key].ballFitness} Parent fit: {self.children[key].fitness}")
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
                bestfit = self.parents[key].ballFitness
                bestfitkey = key
            if self.parents[key].ballFitness > bestfit:
                bestfit = self.parents[key].ballFitness
                bestfitkey = key
            else:
                pass
        self.parents[bestfitkey].Start_Simulation("GUI")
        self.bestFitSolution = self.parents[bestfitkey]
        print(f"Best fit: {bestfit}")
        print(f"\nDimensions:")
        print(f"Goal Torso Height: {self.goalZPos}")
        print(f"Leg Dim: {self.lDim}")
        print(f"Torso Dim: {self.tDim}")
        
