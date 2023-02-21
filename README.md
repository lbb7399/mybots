# Assignment 7: Random 3D Creature

MAKE SURE SIDEBARS ARE DISABLED

## Creature Body Options

The creature starts as a single cube. It then propogates out, branching, for a specified number of generations and potential branches. Each new branch can hinge from one of the far edges of the parent link or directly on its face. All joints are hinge joints. If a link and its parent are face to face, the joint may exist along the two other axes with a 50/50 chance. Each link dimension can be between 0.1 and 0.6 units. 

The body does have the possibility to overlap on itself but I did this code before the full rubric came out and I have not had the time to change it effectively so I fully accept the point loss.


![alt text](https://i.imgur.com/PemdD3m.jpg)
![alt text](https://i.imgur.com/aLGn5QE.jpg)

## Creature Brain Options

Each link has a 50/50 chance of having a sensor. Every sensor is connected to every motor in this case.

![alt text](https://i.imgur.com/DTxsQwu.jpg)

## Required Installation

This code requires the ```pybullet``` package. Download using ```pip3 install pybullet```.

## Running the Code
 Type ```python3 search.py``` into the terminal. If you desire to change the number of brnaches and/or generations of brnaching, you can do so in ```constants.py```.


## Credit

Basis of this code is from the [r/ludobots](https://www.reddit.com/r/ludobots/) course and this [pyrosim](https://github.com/jbongard/pyrosim) package.
