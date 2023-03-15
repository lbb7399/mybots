# Final Project

This code randomly generates a creature that fills 3D space then evolves it to move further in the -x direction. Two methods of evolution are evaluated.

## Hypothesis
My hypothesis is inspired by the work of Josh Bongard. In his work, the brain of a robot is evolved until it meets a specific goal. Once the robot meets this goal, the brain is placed on a robot with an altered body and this pattern continues throughout the run. It is claimed that this method makes a better and more resilient final robot. 

To be consistent across runs within time constraints, rather than letting the brain evolve to meet a certain goal, it and the body will evolve separately and sequentially for a set number of generations each. 

Hypothesis: Evolution will progess faster if mutations are blocked (referred to as sequential in code) where 50 generations of brain mutations will occur then 50 generations of body mutations.

Null: Random selection of a body or brain mutation each generation. The probability of a given mutation is the same in both evolutionary runs. 

https://www.pnas.org/doi/10.1073/pnas.1015390108 add citation

## Experimental Design

10 runs were performed, 5 for each type of evolution. 

The first five runs were random. In ```parallelHillClimber.Mutate()```, every solution is sent to ```solution.Mutate()``` in which it has a 50% chance to chose one of two brian mutations or a 50% chance to chose one of three body mutations.

![Random Diagram](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Random%20Diagram.jpeg?raw=true)

The last five runs were blocked. In ```parallelHillClimber.Evolve()``` a counter tracks whether a mutation should be a brain mutation (count <= 50) or a body mutation (50 < count <= 100). This is passed into ```parallelHillClimber.Mutate()``` where the solutions are either sent to ```solution.Mutate_Mind()```, where there is a 50/50 chance for the two brain mutations, or ```solution.Mutate_Body()```, where there is a 1/3 chance for each of the body mutations, depending on the count. Additionally, while the run numbers for these were 6, 7, 8, 9, and 10, respectively, for clarity, their seed numbers were the same as their corresponding random runs (ie runs 1 and 6 had the same random seed). This means that when comparing the two evolutions, they had the same starting point.

![Blocked Diagram](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Blocked%20Diagram.jpeg?raw=true)

The robots were all tracked by how far in the -x direction they could travel. All mutations, successful and unsuccessful, were recorded.

## Parallel Hill Climber Algorithm







![PHC Diagram]()



## Creature Body Options

The creature has the ability to be 3 links x 4 links x 3 links. Initially, links are selected with a 50/50 chance to exist. Once this process is complete, the links are searched to ensure that they are all connected (see adding block mutation for criteria). If jointed links are face to face, they may either have a joint on their face in either of the two direction perpendicular to their axis or a joint on one of their four touching edges. If the links are connected by an edge, they are connected along that edge. A joint can either be revolute or continuous. Each creature must have at least two links and at least one sensor. Initial dimensions of links are 0.5x0.5x0.5.
### Joint Options
![alt text](https://i.imgur.com/zTpHEXP.jpg)
![alt text](https://i.imgur.com/Mj4LHCl.jpg)

All visuals used for description from run 9, population 9.

## Initial Body Generation


https://user-images.githubusercontent.com/116473746/225168636-8472a355-1db6-4db4-ac4f-f53f9a4d6af1.mp4



![Genotype](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Genotype.jpeg?raw=true)
![Initial Joint Tree](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Initial%20Link%20Tree.jpeg)

![Final Joint Tree](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Final%20Link%20Tree.jpeg?raw=true)




## Creature Brain Options

Each link has a 50/50 chance of having a sensor. For each sensor-motor connection, there is a 50/50 chance of connection.

## Evolution

There are 5 possible mutations that can occur:
- switch sensor on/off: 20%
- add link: 20%
- remove link: 20%
- change synapse: 20%
- change one dimension: 20%

If a mutation fails for whatever reason, another mutation is selected until a mutation is achieved.

The following is a more in depth explanation of each mutation.

### Sensor switch
Randomly select a link in body. If sensor, turn off and vice versa. If there is only one sensor in the body and the mutation attempts to turn it off, the mutation fails as the motors require at least one sensor to operate.
![alt text](https://i.imgur.com/ZwIvPpx.jpg)

### Add Link
A link can be added where one currently does not exist within the set bounds of 3x4x3 blocks. To be added it also needs to be connected along and edge or a face to another link as seen below. This mutation will fail if all links already exist. The new link adds another motor and possibly a sensor and the brain is adjusted accoringly
![alt text](https://i.imgur.com/h1K6mQa.jpg)

###  Remove Link
A link is randomly selected to be removed from the body. This changes the body plan more drastically than adding a link and has a higher chance of failure. It can cause other links to be lost as well. It can also drastically change the connects in nearby links, altering parentage and therefore joints. This method will also fail if all sensors are lost or if the number of links falls below two.
![alt text](https://i.imgur.com/o6TBCuZ.jpg)

### Change Dimensions
A dimension of the links (x,y,z) can be changed uniformly, [0.1,1] in intervals of 0.1. This change is applied to all links, not just active links. This mutation cannot fail.

### Changing Synapses
A random synapse is chosen from all possible synapses. If the synapse is unconnected, it is connected with a random weight. If the synapse is connected, it has a 50/50 chance of being disconnected or changing to another non-zero weight.
![alt text](https://i.imgur.com/62iBJE0.jpg)

## Results

[YouTube Video](https://youtu.be/4cRhPYPOVTA)

Resulting fitness graph for 5 runs:
![alt text](https://i.imgur.com/sy8NNoa.png)

While these creatures do evolve, they do not evolve well and fall more in the Leaning Tower category than anything else. The only run that did not fall over was trial 5, which had the lowest fitness. Future development would include working more on joint options and connection as well as adding in different link shapes.


## Required Installation

This code requires the ```pybullet``` package. Download using ```pip3 install pybullet```.

## Running the Code
 Type ```python3 search.py``` into the terminal. If you desire to change the number of genrations, population size, dimension limits, etc, you can do so in ```constants.py```.
 
 This code it currently set up to run on a Mac with Linux os commands. These show up as os.system() in ```search.py```, ```parallelHillClimber.py``` in the constructor and Select, ```solution.py``` in Start_Simulation and Wait_For_Simulation_To_End, and ```robot.py``` in the constructor and Get_Fitness. If you are using another os, the commands in these lines (not the file names!) may need to be changed.


## Credit

Basis of this code is from the [r/ludobots](https://www.reddit.com/r/ludobots/) course and this [pyrosim](https://github.com/jbongard/pyrosim) package.

## Additional Notes
1. The windows when running the GUI still appear as on my computer at least it causes the simulation to blip in and out of existence without running it. If you would like to try to turn them off, you can do so in ```simulation.py``` in its constructor by uncommenting ```p.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)```.
