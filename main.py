import pygame
# not working rn lol
class Cat:
    def __init__(self, screen):
        self.screen = screen
        self.moved = False
        self.facing_left = False
        self.original_image = pygame.image.load("adam.png")
        self.skill_image = pygame.image.load("Apple_Cat.jpg")
        
        self.image = self.original_image
        self.display = pygame.transform.scale(self.image, (140, 100))
        
        self.x = 0
        self.y = 320
        self.screen_width = 1080
        self.screen_height = 720
        
        # cooldowns
        self.skill_ready = True
        self.skill_cooldown = 2000 
        self.last_skill_time = 0

    def draw(self):
        # camera
        offset_x = self.x - self.screen_width // 2
        offset_y = self.y - self.screen_height // 2
        self.screen.blit(self.display, (self.x - offset_x, self.y - offset_y))

    def skill_one(self):
        self.image = self.skill_image
        self.display = pygame.transform.scale(self.image, (140, 100))
        print("used")

    def reset_image(self):
        self.image = self.original_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.display = pygame.transform.scale(self.image, (140, 100))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 5 
        
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.y += dist
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.y -= dist
            
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.x -= dist
            if not self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.display = pygame.transform.scale(self.image, (140, 100))
                self.facing_left = True
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.x += dist
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.display = pygame.transform.scale(self.image, (140, 100))
                self.facing_left = False

        current_time = pygame.time.get_ticks()
        if not self.skill_ready:
            if current_time - self.last_skill_time >= self.skill_cooldown:
                self.skill_ready = True
                self.reset_image()

        if key[pygame.K_e] and self.skill_ready:
            self.skill_one()
            self.skill_ready = False
            self.last_skill_time = current_time

def main():
    pygame.init()
    width, height = 1080, 720
    background = pygame.image.load("bg.png")
    screen = pygame.display.set_those_screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("nasty cretin")
    
    cat = Cat(screen) # Pass screen to Cat
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cat.handle_keys()
        
        screen.fill((255, 255, 255))
        cat.draw()
        pygame.display.update()
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()
