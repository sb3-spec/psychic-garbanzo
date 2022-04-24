from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

def make_floor(side_length):
    for z in range(side_length):
        for x in range(side_length):
            Entity(
                model="cube", color=color.dark_gray, 
                collider="box", ignore=True, position=(x, 0, z), 
                parent=scene, origin_y=.5, texture="white_cube"
            )
 

class TextureBox(Button):
    def __init__(self, position=(5, 2, 5)):
        super().__init__(
            texture="white_cube",
            position=position,
            model="cube", colororigin_y=.5,
        )
        
        self.texture_choice = 0
        self.textures = ["white_cube"]
        
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.texture_choice += 1
                self.texture_choice %= len(self.textures)
                self.texture = self.textures[self.texture_choice]
                
TextureBox()
make_floor(10)

player = FirstPersonController()

app.run()