# Assignment 6: 1D Creature

This code creates a randomly generated 1D snake.

## Snake Body Options

All links in the chain of the snake are rectangular prisms. There can be as many as 12 or as few as 3 links in a snake. The dimensions of each link are randomly assigned, ranging from 0.1 to 0.6. The first link in the chain lies at the origin with a height of 0.3 and the subsequent links grow in the -y direction also centered at 0.3. Each link randomly generates whether it will have a sensor (green) or not (blue). If no sensor is randomly generated, a sensor is randomly assigned to a block in the chain as the motors require a sensor for the code to run smoothly. Each block, except for the first, generates a joint type to connect it to the previous block. This can either be a horizontal joint in the x direction or a veritcal joint in the z direction.

![alt text](https://i.imgur.com/dUjpQRj.jpg)

## Snake Brain Options

Currently, all sensor neurons are connected to all motor neurons directly through synaptic randomly generated synaptic weights.

## Required Installation

This code requires the ```pybullet``` package. Download using ```pip3 install pybullet```.

## Running the Code

Use the command ```python3 search.py``` in your terminal to run the code. Once it has run, it will display a simulation of the randomly generated creature. 


## Credit

Basis of this code is from the [r/ludobots](https://www.reddit.com/r/ludobots/) course and this [pyrosim](https://github.com/jbongard/pyrosim) package.
