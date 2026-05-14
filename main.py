import pygame

class Cat:
    def __init__(self, screen):
        self.screen = screen
        self.moved = False
        self.facing_left = False

        self.original_image = pygame.image.load("adam.png")
        self.skill_image = pygame.image.load("Apple_Cat.jpg")

        self.image = self.original_image
        self.display = pygame.transform.scale(self.image, (140, 100))

        self.x = 520
        self.y = 520

        # cooldowns
        self.skill_ready = True
        self.skill_cooldown = 2000
        self.last_skill_time = 0

    def draw(self):
        self.screen.blit(self.display, (self.x, self.y))

    def skill_one(self):
        self.image = self.skill_image
        self.display = pygame.transform.scale(self.image, (140, 100))
        print("used")

    def reset_image(self):
        self.image = self.original_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.original_image, True, False)

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

        # cooldown logic
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
    width, height = 960, 720

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("nasty cretin")

    # additional scenes will be added, and hitboxes
    scene_x = 0
    scene_y = 0

    def load_scene(x, y):
        return pygame.image.load(f"scene_{x}_{y}.png")

    background = load_scene(scene_x, scene_y)

    cat = Cat(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cat.handle_keys()

        if cat.x < 0:
            scene_x -= 1
            cat.x = width - 20
            background = load_scene(scene_x, scene_y)

        elif cat.x > width:
            scene_x += 1
            cat.x = 20
            background = load_scene(scene_x, scene_y)

        if cat.y < 0:
            scene_y -= 1
            cat.y = height - 20
            background = load_scene(scene_x, scene_y)

        elif cat.y > height:
            scene_y += 1
            cat.y = 20
            background = load_scene(scene_x, scene_y)

        # draw background
        screen.blit(background, (0, 0))

        # draw cat
        cat.draw()

        pygame.display.update()
        clock.tick(120)

    pygame.quit()


if __name__ == "__main__":
    main()
