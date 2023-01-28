from solution import SOLUTION
import constants as c
import copy
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION()

    
    def Evolve(self):
        for i in range(c.populationSize):
            self.parents[i].Evaluate("GUI")
        
        #for currentGeneration in range(c.numberOfGenerations):
            #self.Evolve_For_One_Generation()

            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        print(f"Parent fit: {self.parent.fitness}, Child fit: {self.child.fitness}")
        self.Select()
    
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        
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
        
