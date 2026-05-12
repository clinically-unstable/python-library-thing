import pygame

class Cat():
    def __init__(self):
        self.image = pygame.image.load("Babem.png")
        # image size
        self.display = pygame.transform.scale(self.image, (140, 160))
        self.x = 0
        self.y = 0

    def draw(self, surface):
        surface.blit(self.display, (self.x, self.y))

    def skill_one(self):
        self.image = pygame.image.load("Apple_Cat.jpg")
        self.display = pygame.transform.scale(self.image, (140, 160))
        print("used")
        
    def handle_keys(self):
        # movement
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.y += dist
        elif key[pygame.K_UP] or key[pygame.K_w]: 
            self.y -= dist 
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.x += dist 
        elif key[pygame.K_LEFT] or key[pygame.K_a]:
            self.x -= dist 

        if key[pygame.K_e]:
            Cat.skill_one(self)

def main():

    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    cat = Cat()
    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                running = False

        cat.handle_keys()
        screen.fill((255,255,255)) 
        cat.draw(screen) 
        pygame.display.update() 
    # framerate
        clock.tick(120)
main()