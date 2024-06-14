import sys
import pygame


class Game:
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption("Demo")
        self.screen = pygame.display.set_mode((640,480))


        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.clock = pygame.time.Clock()
        self.collision_area = pygame.Rect(50,50,300,50)

        self.img_pos = [160,260]
    def run(self):

        self.screen.fill((13,219,248))


        self.screen.blit(self.img, self.img_pos)




        while True:



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            keys = pygame.key.get_pressed()

            
            pygame.display.update()
            self.clock.tick(60)

Game().run()