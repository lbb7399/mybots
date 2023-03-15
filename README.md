# Final Project

This code randomly generates a creature that fills 3D space then evolves it to move further in the -x direction. Two methods of evolution are evaluated over 500 generations with a population size of 10 each.

### Gif preview
Both robots start with the same random seed and therefore same body and brain but the robot in run 4 is randomly evolved and the robot in run 9 is sequentially evolved. Run 9 had the best fitness over all runs.

![final](https://user-images.githubusercontent.com/116473746/225198178-68ecf23a-a157-43d5-a1e1-61029dbd39b6.gif)

### Video Summary

The file is too large to place in the read me or the repository so here is the [YouTube link](https://youtu.be/6ksTQy0KhNM).



## Hypothesis
My hypothesis is inspired by the work of Josh Bongard. In his [work](https://www.pnas.org/doi/10.1073/pnas.1015390108), the brain of a robot is evolved until it meets a specific goal. Once the robot meets this goal, the brain is placed on a robot with an altered body and this pattern continues throughout the run. It is claimed that this method makes a better and more resilient final robot. 

To be consistent across runs within time constraints, rather than letting the brain evolve to meet a certain goal, it and the body will evolve separately and sequentially for a set number of generations each. 

Hypothesis: Evolution will progess faster if mutations are blocked (referred to as sequential in code) where 50 generations of brain mutations will occur then 50 generations of body mutations.

Null: Random selection of a body or brain mutation each generation. The probability of a given mutation is the same in both evolutionary runs. 


## Experimental Design

10 runs were performed, 5 for each type of evolution. 

The first five runs were random. In ```parallelHillClimber.Mutate()```, every solution is sent to ```solution.Mutate()``` in which it has a 50% chance to chose one of two brian mutations or a 50% chance to chose one of three body mutations.

![Random Diagram](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Random%20Diagram.jpeg?raw=true)

The last five runs were blocked. In ```parallelHillClimber.Evolve()``` a counter tracks whether a mutation should be a brain mutation (count <= 50) or a body mutation (50 < count <= 100). This is passed into ```parallelHillClimber.Mutate()``` where the solutions are either sent to ```solution.Mutate_Mind()```, where there is a 50/50 chance for the two brain mutations, or ```solution.Mutate_Body()```, where there is a 1/3 chance for each of the body mutations, depending on the count. Additionally, while the run numbers for these were 6, 7, 8, 9, and 10, respectively, for clarity, their seed numbers were the same as their corresponding random runs (ie runs 1 and 6 had the same random seed). This means that when comparing the two evolutions, they had the same starting point.

![Blocked Diagram](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Blocked%20Diagram.jpeg?raw=true)

The robots were all tracked by how far in the -x direction they could travel. All mutations, successful and unsuccessful, were recorded.


## Creature Body Options

The creature has the ability to be 3 links x 4 links x 3 links. Initially, links are selected with a 50/50 chance to exist. Once this process is complete, the links are searched to ensure that they are all connected (see adding block mutation for criteria). If jointed links are face to face, they may either have a joint on their face in either of the two direction perpendicular to their axis or a joint on one of their four touching edges. If the links are connected by an edge, they are connected along that edge. A joint can either be revolute or continuous. Each creature must have at least two links and at least one sensor. Initial dimensions of links are 0.5x0.5x0.5.
### Joint Options
![alt text](https://i.imgur.com/zTpHEXP.jpg)
![alt text](https://i.imgur.com/Mj4LHCl.jpg)

All visuals used for description from run 9, population 9 (9-9).

## Initial Body Generation
### Genotype
![Genotype](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Genotype.jpeg?raw=true)

### Phenotype

Process for creating 9-9, initial body:

https://user-images.githubusercontent.com/116473746/225168636-8472a355-1db6-4db4-ac4f-f53f9a4d6af1.mp4


### Initial Joint Tree

As stated before, links can only be children to links that are higher on the list of links than them, therefore preserving one base. Below is the initial joint configuration of run 9-9.

Link list: '021', '022', '030', '032', '112', '121', '211', '212', '231', '232', '200', '100'

![Initial Joint Tree](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Initial%20Link%20Tree.jpeg)


### Final Joint Tree

Added links: 110, 130, 111

Removed links: 212, 112, 032, 232, 022

Link list: '021', '030', '121', '211', '231', '200', '100', '110', '130', '111'

![Final Joint Tree](https://github.com/lbb7399/mybots/blob/final-project/diagrams/Final%20Link%20Tree.jpeg?raw=true)



## Creature Brain Options

Each link has a 50/50 chance of having a sensor. For each sensor-motor connection, there is a 50/50 chance of connection.

## Evolution

There are 5 possible mutations that can occur:
- switch sensor on/off: 25%
- add link: 16.7%
- remove link: 16.7%
- change synapse: 25%
- change one dimension: 16.7%

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


## Parallel Hill Climber Algorithm

At each generation, the original solutions (parents) create duplicates of themselves and mutate. If the child out performs the parent, meaning it travels further in the negative x direction, it replaces the current parent and becomes the parent in the next generation. If the child does not beat the parent, the parent continues on to the next generation, spawns another child, and tries again.


## Results

### Max Fitness of each run
![Total max](https://github.com/lbb7399/mybots/blob/final-project/figures/Evolution%20Curve.png?raw=true)

### Max Fitness Curves for Each Seed
![Seed 1 max](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%201%20Max%20Evolution%20Curve.png?raw=true)
![Seed 2 max](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%202%20Max%20Evolution%20Curve.png?raw=true)
![Seed 3 max](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%203%20Max%20Evolution%20Curve.png?raw=true)
![Seed 4 max](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%204%20Max%20Evolution%20Curve.png?raw=true)
![Seed 5 max](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%205%20Max%20Evolution%20Curve.png?raw=true)

While the hypothesis does beat the null 3/5 times, this is not statistically significant and a t-test on just these ten values found a p-value of 0.75.

### Median Fitness Curves with Total Range
![Seed 1 med](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%201%20Evolution%20Curve.png?raw=true)
![Seed 2 med](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%202%20Evolution%20Curve.png?raw=true)
![Seed 3 med](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%203%20Evolution%20Curve.png?raw=true)
![Seed 4 med](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%204%20Evolution%20Curve.png?raw=true)
![Seed 5 med](https://github.com/lbb7399/mybots/blob/final-project/figures/Seed%205%20Evolution%20Curve.png?raw=true)

As seen in the plots above, when considering the range of fitnesses in each run the populations are extremely similar. Running a t-test across all populations, they are 97% similar. Therefore the hypothesis is false, at least for this set of mutations.

## Example Run

This is run 9-9 highlighting the mutations that had a >0.1 increase to fitness.

![Screenshot 2023-03-14 at 11 29 28 PM](https://user-images.githubusercontent.com/116473746/225206750-30123285-9437-4663-831b-761d79795e7c.png)

### Generation 0

![Screenshot 2023-03-14 at 11 28 52 PM](https://user-images.githubusercontent.com/116473746/225206675-237f8d53-f592-483c-9245-ffbb30bab340.png)
![Screenshot 2023-03-14 at 11 32 47 PM](https://user-images.githubusercontent.com/116473746/225207239-36f1a92e-b194-45e1-9d50-35200e3d8716.png)

### Generation 58

Link 212 removed

![Screenshot 2023-03-14 at 11 30 20 PM](https://user-images.githubusercontent.com/116473746/225206857-388eb470-db6d-4801-a95e-f1bd0252bfce.png)
![Screenshot 2023-03-14 at 11 34 09 PM](https://user-images.githubusercontent.com/116473746/225207422-ae57b122-339e-4adc-9a83-52b5b4582be7.png)

### Generation 93

Link 210 added

![Screenshot 2023-03-14 at 11 31 02 PM](https://user-images.githubusercontent.com/116473746/225206978-4eca2cda-74b0-4a28-9e70-0088c11957e4.png)

![Screenshot 2023-03-14 at 11 34 59 PM](https://user-images.githubusercontent.com/116473746/225207538-6ada8adf-4826-480e-ae9f-6a31ccaa2c8a.png)

### Generation 100

Link 232 removed

![Screenshot 2023-03-14 at 11 31 13 PM](https://user-images.githubusercontent.com/116473746/225207013-2a19c9c5-f27c-460e-a4c7-87f2efe96eac.png)
![Screenshot 2023-03-14 at 11 35 43 PM](https://user-images.githubusercontent.com/116473746/225207646-79d90cee-3610-4c6f-b813-b6089d892fd9.png)

### Generation 122

Synapse 100 - 200_100 mutated from 0.47 to 0.92

![Screenshot 2023-03-14 at 11 31 21 PM](https://user-images.githubusercontent.com/116473746/225207030-3f6ceebc-5f51-4e12-988b-933478ee6208.png)
![Screenshot 2023-03-14 at 11 36 10 PM](https://user-images.githubusercontent.com/116473746/225207707-2e33d740-71e0-4ac9-874d-8f98097dda4c.png)

### Generation 455

Link 210 removed

![Screenshot 2023-03-14 at 11 31 34 PM](https://user-images.githubusercontent.com/116473746/225207054-0297c864-8e09-4030-9f9f-8059156b45e2.png)
![Screenshot 2023-03-14 at 11 37 25 PM](https://user-images.githubusercontent.com/116473746/225207858-941df0c6-f5f5-4e08-b3c1-51056cb7ca4a.png)


### Generation 458

Link 022 removed

![Screenshot 2023-03-14 at 11 31 41 PM](https://user-images.githubusercontent.com/116473746/225207064-60e41413-2268-40c6-8fac-84ddc81a80e0.png)
![Screenshot 2023-03-14 at 11 38 16 PM](https://user-images.githubusercontent.com/116473746/225207961-6badc4cb-2927-46e6-8795-8e623b242c1b.png)


### Generation 500

![Screenshot 2023-03-14 at 11 32 05 PM](https://user-images.githubusercontent.com/116473746/225207113-bba8ff61-b324-4622-bfd6-8a706e707057.png)

![Screenshot 2023-03-14 at 11 38 34 PM](https://user-images.githubusercontent.com/116473746/225207994-98a5b916-47a0-4d80-bfba-5ccd1bf5411a.png)

## Discussion

While the hypothesis failed, there is still something to be learned from this experiment.

### Number of links and fitness

From observing the simulations, robots with a larger number of links seemed to struggle more with beneficial mutations. 

![scatter](https://github.com/lbb7399/mybots/blob/final-project/figures/Links-fitness-scatter.png?raw=true)

The scatter plot has an R2 value of 0.15. While this is a weak correlation, as you can see in the scatterplot a lower number of links does not necessarily mean a higher (lower) fitness but a large number of links does seem to limit mobility.

### Dimension Changing
In all successful mutations across the best runs, there was not a single beneficial dimension change. I believe this is because since it does not change how any of the links connected or their spacing relative to eachother, it did not have an impact. In the future, if the code were altered such that each block could have a different dimension, this mutation could be beneficial but the way it is now it was unsuccessful.

### Mutation success

Overall, mutation success was much lower than expected. Of the most successful in each run, the highest number of mutations was 33 and typically the bulk of the mutations were in the brain and not the body. Adding and removing a block is a big change but, especially in larger robots, this likely had less effect than anticapated. When selecting the remove block mutation, I expected it to succeed more frequently with more changes to its surroundings, like needing to reconfigure joints. It was assumed that that would be a sufficient hidden joint mutation as well. As the success rate was low and often with less influential links in the joint list, it did not succeed in doing so. Therefore, if I were to alter this code in the the future, I would add a joint mutation on its own. I would also likely reduce the probablity of adding or removing a block.


(see pickles/mutationsTrue.xlsx for the successful mutations of the most successful line in each run)

## Conclusion

I believe with more variety of smaller body mutations and more runs/generations, this hypothesis could be retested and generate different results. For this instance though, there was no difference in mutating the brain and body together or separately.

## Required Installation

This code requires the ```pybullet``` package. Download using ```pip3 install pybullet```.

## Running the Code
 Type ```python3 search.py``` into the terminal. If you desire to change the number of genrations, population size, dimension limits, etc, you can do so in ```constants.py```.
 
 To run only the simulation of a previous generation, use ```repeat.py```. For example if you wanted to repeat 9-9, you would need to write num = 9, best = 9, and gen = 500. If you do not know the best run of the final generation, load "pickles/save_bestfinal9-500.p" and run parents.Start_Simulation("GUI") instead of parents[best].Start_Simulation("GUI").
 
 
 This code it currently set up to run on a Mac with Linux os commands. These show up as os.system() in ```search.py```, ```parallelHillClimber.py``` in the constructor and Select, ```solution.py``` in Start_Simulation and Wait_For_Simulation_To_End, and ```robot.py``` in the constructor and Get_Fitness. If you are using another os, the commands in these lines (not the file names!) may need to be changed.


## Credit

Basis of this code is from the [r/ludobots](https://www.reddit.com/r/ludobots/) course and this [pyrosim](https://github.com/jbongard/pyrosim) package.

## Additional Notes
1. The windows when running the GUI still appear as on my computer at least it causes the simulation to blip in and out of existence without running it. If you would like to try to turn them off, you can do so in ```simulation.py``` in its constructor by uncommenting ```p.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)```.
