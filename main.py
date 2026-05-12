import pygame

import pygame

class Cat:
    def __init__(self):
        # store both images
        self.original_image = pygame.image.load("adam.png")
        self.skill_image = pygame.image.load("Apple_Cat.jpg")

        self.image = self.original_image
        self.display = pygame.transform.scale(self.image, (140, 100))

        self.x = 0
        self.y = 0

        # cooldowns
        self.skill_ready = True
        self.skill_cooldown = 2000  # ms
        self.last_skill_time = 0

    def draw(self, surface):
        surface.blit(self.display, (self.x, self.y))

    def skill_one(self):
        self.image = self.skill_image
        self.display = pygame.transform.scale(self.image, (140, 100))
        print("used")

    def reset_image(self):
        self.image = self.original_image
        self.display = pygame.transform.scale(self.image, (140, 100))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 2

        # movement
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.y += dist
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.y -= dist
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.x += dist
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.x -= dist

        # cooldown logic
        current_time = pygame.time.get_ticks()

        if not self.skill_ready:
            if current_time - self.last_skill_time >= self.skill_cooldown:
                self.skill_ready = True
                self.reset_image()  

        # skill activation
        if key[pygame.K_e] and self.skill_ready:
            self.skill_one()
            self.skill_ready = False
            self.last_skill_time = current_time



def main():
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("nasty cretin")

    cat = Cat()
    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cat.handle_keys()

        screen.fill((255, 255, 255))
        cat.draw(screen)
        pygame.display.update()

        clock.tick(120)

    pygame.quit()


main()
