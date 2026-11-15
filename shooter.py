from ursina import *

app = Ursina()

# 1. Generate the board
for z in range(8):
    for x in range(8):
        square_color = color.white if (x + z) % 2 == 0 else color.dark_gray
        Entity(parent=scene, position=(x, 0, z), model='cube', scale=(1, 0.1, 1), color=square_color, collider='box')

# 2. Spawn the Pieces (Pawns)
for x in range(8):
    # Spawn White pawns on row 1 (z=1)
    Entity(parent=scene, position=(x, 0.5, 1), model='cylinder', scale=(0.4, 0.8, 0.4), color=color.cyan, collider='box')
    
    # Spawn Black pawns on row 6 (z=6)
    Entity(parent=scene, position=(x, 0.5, 6), model='cylinder', scale=(0.4, 0.8, 0.4), color=color.red, collider='box')

# 3. Camera setup
camera.position = (3.5, 10, -5)
camera.look_at((3.5, 0, 3.5))

app.run()