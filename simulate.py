import pybullet as p
import time
physicsClient = p.connect(p.GUI)
p.loadSDF("box.sdf")
for i in range(1000):
    p.stepSimulation()
    print(i)
    time.sleep(1/60)
p.disconnect()

