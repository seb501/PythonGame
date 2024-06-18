import sys
import random
import math
import pygame
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
class Game:
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption("Demo")
        self.screen = pygame.display.set_mode((640,480))

        self.display = pygame.Surface((320,240))
        
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=6),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=6),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=6),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur = 15, loop=False ),
            'particle/particle': Animation(load_images('particles/particle'), img_dur = 6, loop=False ),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png')
        }
        
        self.player = Player(self , (50,50), (8,15))
        self.tilemap = Tilemap(self, tile_size=16)
        self.load_level(0)

       
        self.Clouds =  Clouds(self.assets['clouds'], count =  15)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.leaf_spawner = []

        #tree leafs
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawner.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1],23,13 ))

        #spawner 
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0),('spawners', 1)]):
            if spawner['variant'] == 00:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8,15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0,0]
        self.dead = 0


    def run(self):

     
        while True:
            
            self.display.fill((120,120,244))
            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.load_level(0)
            #Camera
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 26
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 26
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #Particles
            for rect in self.leaf_spawner:
                if random.random() * 45655 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.2, 0.3], frame=random.randint(0, 20)))

            #Clouds
            self.Clouds.update()
            self.Clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)
            

            #Enemy
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0,0))
                enemy.render(self.display, offset= render_scroll)
                if kill: 
                    self.enemies.remove(enemy)
            #Player
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self. assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

            #Sparks
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset = render_scroll)
                if kill:
                    self.sparks.remove(spark)
            #remove Particle
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_v:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
               

            keys = pygame.key.get_pressed()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()