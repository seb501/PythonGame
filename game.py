import sys
import pygame
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

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
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=5),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=6),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=6),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=6),
        
        }
        
        self.player = Player(self , (50,50), (8,15))
        self.tilemap = Tilemap(self, tile_size=16)
        self.scroll = [0,0]
        self.Clouds =  Clouds(self.assets['clouds'], count =  15)


    def run(self):

     
        while True:
            
            self.display.fill((120,120,244))
            
            #Camera
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 26
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1]) / 26
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.Clouds.update()
            self.Clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
               

            keys = pygame.key.get_pressed()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()