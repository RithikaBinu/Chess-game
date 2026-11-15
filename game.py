from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Initialize the 3D engine
app = Ursina()

# 1. Create the environment (Sky and Ground)
Sky()
ground = Entity(
    model='plane', 
    scale=(100, 1, 100), 
    texture='white_cube', 
    texture_scale=(100,100), 
    collider='box',
    color=color.dark_gray
)

# 2. Drop the player in as a First Person Controller
player = FirstPersonController()

# 3. Spawn random 3D targets (like a firing range)
for i in range(15):
    target = Entity(
        model='cube',
        color=color.red,
        position=(random.randint(-20, 20), 1, random.randint(-20, 20)),
        collider='box'
    )

app.run()