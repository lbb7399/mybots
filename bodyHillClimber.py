from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import random
import copy
class BODY_HILL_CLIMBER:
    def __init__(self):
        
        
        self.phcparents = {}
#        fitness = {}
        for i in range(c.bodyPopulation):
            self.phcparents[i] = PARALLEL_HILL_CLIMBER(i)
            self.phcparents[i].Evolve()
            self.phcparents[i].Get_Best_Solution()
#            fitness[i] = phcparents[i].Get_Best_Fitness()
            
        
    def Evolve(self):
        for currentGen in range(c.bodyGenerations):
            self.currentGen = currentGen
            self.Evolve_for_One_Generation()
        
    def Evolve_for_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.phcchildren)
        self.Print()
        self.Select()
    
    def Spawn(self):
        self.phcchildren = {}
        for key in self.phcparents:
            self.phcchildren[key] = copy.deepcopy(self.phcparents[key])
   
   
    def Mutate(self):
        for key in self.phcchildren:
            delta = random.randint(0,5)
            self.phcchildren[key].Mutate_Body(delta)
            print(f"\n Body Gen Children{self.currentGen}")
            print(f"Goal Z: {self.phcchildren[key].goalZPos}")
            print(f"LDim: {self.phcchildren[key].lDim}")
            print(f"TDim: {self.phcchildren[key].tDim}")
            
    def Evaluate(self, phcs):
        for i in range(c.bodyPopulation):
            phcs[i].Evolve()
            phcs[i].Get_Best_Solution()
    
    def Print(self):
        print(f"\n")
        print(f"Generation {self.currentGen}")
        for key in self.phcparents:
            print(f"ID: {key} Parent fit: {self.phcparents[key].bestFitSolution.ballFitness} Child fit: {self.phcchildren[key].bestFitSolution.ballFitness}")
            #print(f"ID: {key} Parent ball fit: {self.parents[key].ballFitness} Parent fit: {self.children[key].fitness}")
        print(f"\n")
        
    def Select(self):
        for key in self.phcparents:
            if self.phcchildren[key].bestFitSolution.ballFitness > self.phcparents[key].bestFitSolution.ballFitness:
                self.phcparents[key] = self.phcchildren[key]
                
    def Show_Best(self):
        for i, key in enumerate(self.phcparents.keys()):
            if i == 0:
                bestfit = self.phcparents[key].bestFitSolution.ballFitness
                bestfitkey = key
            if self.phcparents[key].bestFitSolution.ballFitness > bestfit:
                bestfit = self.phcparents[key].bestFitSolution.ballFitness
                bestfitkey = key
            else:
                pass
        self.bestfitkey = bestfitkey
        self.phcparents[bestfitkey].Show_Best()
        
        

    
