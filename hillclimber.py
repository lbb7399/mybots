from solution import SOLUTION
import constants as c
import copy
class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()
    
    def Evolve(self):
        #self.parent.Evaluate("DIRECT")
        for currentGeneration in range(c.numberOfGenerations):
            if currentGeneration == 0:
                self.parent.Evaluate("GUI")
            self.Evolve_For_One_Generation()
            
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
        self.parent.Evaluate("GUI")
        
