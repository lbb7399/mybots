from solution import SOLUTION
import constants as c
import copy
import os
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        
        
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    
    def Evolve(self):
        for i in range(c.populationSize):
            self.parents[i].Start_Simulation("DIRECT")
            
        for i in range(c.populationSize):
            self.parents[i].Wait_For_Simulation_To_End()
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

            
    def Evolve_For_One_Generation(self):
#        self.Spawn()
#        self.Mutate()
#        self.child.Evaluate("DIRECT")
#        print(f"Parent fit: {self.parent.fitness}, Child fit: {self.child.fitness}")
#        self.Select()
        pass
    
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.SET_ID(self.nextAvailableID)
        self.nextAvailableID = self.nextAvailableID + 1
        
        
    def Mutate(self):
        self.child.Mutate()
#        print("Parent:")
#        print(self.parent.weights)
#        print("Child:")
#        print(self.child.weights)
    
    def Select(self):
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child
            
    def Show_Best(self):
#        self.parent.Evaluate("GUI")
        pass
        
