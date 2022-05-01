from urllib.request import HTTPDefaultErrorHandler
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from perlin_noise import PerlinNoise

from nMap import nMap  

app = Ursina() 

window.fullscreen = True
window.show_ursina_splash = True

prevTime = time.time()

scene.fog_color = color.rgb(0, 0, 0)
scene.fog_density = .01

stone_texture = load_texture('stone.png')
creeper_model = load_model('creeper.obj')
creeper_texture = load_texture('creeper_texture.png')
axilotl_model = load_model('axilotl.obj')
axilotl_texture = load_texture('axilotl.png')


# terrain_length = 50

# for i in range(terrain_length * terrain_length):
#     bud = Entity(model="cube", origin_y=.5, texture="stone.png")      
#     bud.x = math.floor(i/terrain_length)
#     bud.z = math.floor(i%terrain_length)
#     bud.y = math.floor(noise([bud.x/freq, bud.z/freq]) * amp)
#     bud.parent = terrain

# terrain.combine()
# terrain.texture = stone_texture
# terrain.collider = 'mesh'

shells = []
shellWidth = 3


# Player stuff
player = FirstPersonController()
prevZ = player.z
prevX = player.x
isRunning = False
walkSpeed = 5


# Terrain and terrain generation
terrain = Entity(model=None, collider=None)
terrainWidth = 100
terrainFinished = False
noise = PerlinNoise(octaves=3, seed=100)
amp = 50
freq = 100
subWidth = int(terrainWidth)
chunks = []
fragments = [] # child of chunk
fragment_index = 0
currentChunk = 0

# Instantiate our 'ghost' chunks
for i in range(subWidth):
    bud = Entity(model="cube")
    fragments.append(bud)


# Instantiate our empty chunks
for i in range(int((terrainWidth * terrainWidth)/subWidth)):
    bud = Entity(model=None)
    bud.parent = terrain
    chunks.append(bud)
    


    
    


for i in range(shellWidth * shellWidth):
    bud = Entity(model='cube', collider='box')
    bud.visible = False
    shells.append(bud)
    
    
        
    
    
def update():
    global prevZ, prevX, prevTime, walkSpeed
    
    if abs(player.z - prevZ) > 1 or abs(player.x - prevX) > 1:
        generate_shell()
        
    if time.time() - prevTime > .04:
        generateChunk()
        prevTime = time.time()
        
    if player.y < -amp + 1:
        player.y = floor(noise([player.x/freq, player.z/freq]) * amp) + player.height + 1
        
        player.land()
        
    nasty_mob.look_at(player, 'back')
        

def input(key):
    global isRunning
    if key == 'escape':
        quit()
    if key == 'left shift': 
        isRunning = not isRunning
    
    
    
def finishTerrain():
    global terrainFinished
    if not terrainFinished:
        terrain.combine()
        terrainFinished = True    
        terrain.texture = stone_texture

def generateChunk():
    global fragment_index, currentChunk, freq
    
    if currentChunk >= len(chunks): 
        finishTerrain()
        return
    
    for i, frag in enumerate(fragments):
        frag.x = floor((i + fragment_index) / terrainWidth)
        
        
        frag.z = floor((i + fragment_index) % terrainWidth)
        frag.y = floor(noise([frag.x/freq, frag.z/freq]) * amp)
        frag.visible = False
        
        # Set color of fragment_index :)
        r = b = 0
        g = nMap(frag.y, -amp, amp, 80, 255)
        frag.color = color.rgb(r, g + amp + 80 , b)
        frag.parent = chunks[currentChunk]
    
    chunks[currentChunk].combine(auto_destroy=False)
    chunks[currentChunk].texture = stone_texture
    fragment_index += subWidth
    currentChunk += 1
     
     
def generate_shell():
    global shellWidth, amp, freq, fragments, currentChunk
        
    for i, shell in enumerate(shells):
        shell.x = floor(i/shellWidth + player.x - .5*shellWidth)
        
        shell.z = floor(i%shellWidth + player.z - .5*shellWidth)
        
        shell.y = floor(noise([shell.x/freq, shell.z/freq]) * amp)
        


nasty_mob = Entity(model=axilotl_model, scale=1, x=22, z=16, y=7.1, double_sided=True, texture=axilotl_texture)
generate_shell()

app.run()