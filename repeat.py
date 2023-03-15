import pickle
import constants as c




num = 9
best = 9
gen = 500
parents = pickle.load( open( f"pickles/{num}/save_parents{num}-{gen}.p", "rb" ) )

parents[best].Start_Simulation("GUI")


