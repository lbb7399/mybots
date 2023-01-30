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
#        for i in range(c.populationSize):
#            self.parents[i].Start_Simulation("DIRECT")
#
#        for i in range(c.populationSize):
#            self.parents[i].Wait_For_Simulation_To_End()

        # instead:
        self.Evaluate(self.parents)
        
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
#        self.child.Evaluate("DIRECT") #old
        self.Evaluate(self.children)
    
#        print(f"Parent fit: {self.parent.fitness}, Child fit: {self.child.fitness}")
#        self.Select()
        
    
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
    
    def Select(self):
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child
            
    def Show_Best(self):
#        self.parent.Evaluate("GUI")
        pass
        
