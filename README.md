# Assignment 8: Evolved Random 3D Creatures

This code randomly generates a create that fills 3D space then evolves it to move further in the -x direction. 

## Creature Body Options

The creature has the ability to be 3 links x 4 links x 3 links. Initially, links are selected with a 50/50 chance to exist. Once this process is complete, the links are searched to ensure that they are all connected (see adding block mutation for criteria). If jointed links are face to face, they may either have a joint on their face in either of the two direction perpendicular to their axis or a joint on one of their four touching edges. If the links are connected by an edge, they are connected along that edge. A joint can either be revolute or continuous. Each creature must have at least two links and at least one sensor. Initial dimensions of links are 0.5x0.5x0.5.

### Joint Options
![alt text](https://i.imgur.com/zTpHEXP.jpg)
![alt text](https://i.imgur.com/Mj4LHCl.jpg)

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

[YouTube Video]()

Resulting fitness graph for 5 runs:
![alt text](https://i.imgur.com/sy8NNoa.png)

While these creatures do evolve, they do not evolve well and fall more in the Leaning Tower category than anything else. The only run that did not fall over was trial 5, which had the lowest fitness. Future development would include working more on joint options and connection as well as adding in different link shapes.


## Required Installation

This code requires the ```pybullet``` package. Download using ```pip3 install pybullet```.

## Running the Code
 Type ```python3 search.py``` into the terminal. If you desire to change the number of genrations, population size, dimension limits, etc, you can do so in ```constants.py```.


## Credit

Basis of this code is from the [r/ludobots](https://www.reddit.com/r/ludobots/) course and this [pyrosim](https://github.com/jbongard/pyrosim) package.
