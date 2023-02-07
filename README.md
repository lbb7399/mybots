# Assignment 5

This code mimics evolution of a animal-esque quadruped, whose basic shape and components can be seen below in 2D. The fitness of the creature is determined by how far by magnitude it is able to kick a ball which is placed two units away from the origin in the -x direction.


![alt text](https://i.imgur.com/0n0RaC0.png)


The creature begins with randomly generated dimensions, within bounds, for its torso, leg segments, and how high its center of gravity would be if it took the position seen in the picture above. All legs have the same dimensions. From there, it uses a slightly modified version of the parallel hill climber developed by r/ludobots to find better sensor weights to kick the ball. Then a dimension of the creature is changed and the process repeats.


## Running the code

Run search.py and the final output will be the evolved creature. The only variables you should/would change are the population and generation sizes in constants.py. 

numberOfGenerations refers to the number of iterations parallel hill climber will do in one pass, populationSize is the number of creatures analyzed and evolved each generation of parallel hill climber. bodyPopulation refers to the number of parallel hill climbers that are run in body hill climber in each generation and bodyGenerations refers to how many times a creature's body evolves.

