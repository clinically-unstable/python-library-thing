import pygame
import random
import math


class Laser:
    def __init__(self, box_left, box_top, box_right, box_bottom):
        self.box_left = box_left
        self.box_top = box_top
        self.box_right = box_right
        self.box_bottom = box_bottom

        self.direction = random.choice(["horizontal", "vertical"])
        self.thickness = 8
        self.speed = 3  
        self.warn_duration = 800   
        self.active_duration = 500 
        self.state = "warning"  
        self.spawn_time = pygame.time.get_ticks()

        if self.direction == "horizontal":
            self.pos = random.randint(box_top + 20, box_bottom - 20)
        else:
            self.pos = random.randint(box_left + 20, box_right - 20)

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time
        if self.state == "warning" and elapsed >= self.warn_duration:
            self.state = "active"
            self.active_start = now
        elif self.state == "active":
            if now - self.active_start >= self.active_duration:
                self.state = "done"

    def draw(self, screen, offset_x, offset_y):
        if self.state == "warning":
            now = pygame.time.get_ticks()
            flash = int((now // 100) % 2)
            color = (255, 50, 50, 120) if flash else (255, 200, 200, 60)
            alpha_surf = pygame.Surface(
                (self.box_right - self.box_left, self.box_bottom - self.box_top),
                pygame.SRCALPHA
            )
            if self.direction == "horizontal":
                rel_y = self.pos - self.box_top
                pygame.draw.rect(alpha_surf, color,
                                 (0, rel_y - self.thickness // 2,
                                  self.box_right - self.box_left, self.thickness))
            else:
                rel_x = self.pos - self.box_left
                pygame.draw.rect(alpha_surf, color,
                                 (rel_x - self.thickness // 2, 0,
                                  self.thickness, self.box_bottom - self.box_top))
            screen.blit(alpha_surf, (self.box_left - offset_x, self.box_top - offset_y))

        elif self.state == "active":
            if self.direction == "horizontal":
                y = self.pos - offset_y
                pygame.draw.rect(screen, (255, 0, 0),
                                 (self.box_left - offset_x, y - self.thickness // 2,
                                  self.box_right - self.box_left, self.thickness))
        
                glow_surf = pygame.Surface(
                    (self.box_right - self.box_left, self.thickness * 4),
                    pygame.SRCALPHA
                )
                pygame.draw.rect(glow_surf, (255, 80, 80, 60),
                                 (0, 0, self.box_right - self.box_left, self.thickness * 4))
                screen.blit(glow_surf, (self.box_left - offset_x, y - self.thickness * 2))
            else:
                x = self.pos - offset_x
                pygame.draw.rect(screen, (255, 0, 0),
                                 (x - self.thickness // 2, self.box_top - offset_y,
                                  self.thickness, self.box_bottom - self.box_top))
                glow_surf = pygame.Surface(
                    (self.thickness * 4, self.box_bottom - self.box_top),
                    pygame.SRCALPHA
                )
                pygame.draw.rect(glow_surf, (255, 80, 80, 60),
                                 (0, 0, self.thickness * 4, self.box_bottom - self.box_top))
                screen.blit(glow_surf, (x - self.thickness * 2, self.box_top - offset_y))

    def hits(self, cat_x, cat_y, cat_w=100, cat_h=60):
        if self.state != "active":
            return False
        if self.direction == "horizontal":
            laser_top = self.pos - self.thickness // 2
            laser_bot = self.pos + self.thickness // 2
            if cat_y < laser_bot and cat_y + cat_h > laser_top:
                return True
        else:
            laser_left = self.pos - self.thickness // 2
            laser_right = self.pos + self.thickness // 2
            if cat_x < laser_right and cat_x + cat_w > laser_left:
                return True
        return False


class Cat:
    SPRITE_W = 100
    SPRITE_H = 60

    def __init__(self, screen):
        self.screen = screen
        self.facing_left = False
        self.original_image = pygame.image.load("adam.png")
        self.image = self.original_image
        self.display = pygame.transform.scale(self.image, (self.SPRITE_W, self.SPRITE_H))
        self.x = 520
        self.y = 520

        
        self.skill_ready = True
        self.skill_cooldown = 3000 
        self.skill_duration = 1000
        self.last_skill_time = 0
        self.skill_active = False

  
        self.dead = False
        self.hit_flash_time = 0

    def _he_so_blue(self):
        base = pygame.transform.scale(self.original_image, (self.SPRITE_W, self.SPRITE_H))
        if self.facing_left:
            base = pygame.transform.flip(base, True, False)
        tinted = base.copy()
        blue_overlay = pygame.Surface((self.SPRITE_W, self.SPRITE_H), pygame.SRCALPHA)
        blue_overlay.fill((0, 120, 255, 140))
        tinted.blit(blue_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        blue_add = pygame.Surface((self.SPRITE_W, self.SPRITE_H), pygame.SRCALPHA)
        blue_add.fill((0, 80, 200, 80))
        tinted.blit(blue_add, (0, 0))
        return tinted

    def _make_normal_surface(self):
        base = pygame.transform.scale(self.original_image, (self.SPRITE_W, self.SPRITE_H))
        if self.facing_left:
            base = pygame.transform.flip(base, True, False)
        return base
        
    def activate_skill(self):
        self.skill_active = True
        self.skill_ready = False
        self.last_skill_time = pygame.time.get_ticks()
        self.display = self._he'()

    def update(self):
        if self.dead:
            return
        now = pygame.time.get_ticks()
        if self.skill_active:
            if now - self.last_skill_time >= self.skill_duration:
                self.skill_active = False
                self.display = self._make_normal_surface()
        if not self.skill_ready:
            if now - self.last_skill_time >= self.skill_cooldown:
                self.skill_ready = True

    def draw(self, offset_x, offset_y):
        screen_x = self.x - offset_x
        screen_y = self.y - offset_y

        self.screen.blit(self.display, (screen_x, screen_y))

    def handle_keys(self, box_left, box_top, box_right, box_bottom):
        if self.dead:
            return
        key = pygame.key.get_pressed()
        dist = 3
        new_x, new_y = self.x, self.y

        moved = False
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            new_y += dist;  moved = True
        if key[pygame.K_UP] or key[pygame.K_w]:
            new_y -= dist;  moved = True
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            new_x -= dist;  moved = True
            if not self.facing_left:
                self.facing_left = True
                self.display = (self._he'() if self.skill_active
                                else self._make_normal_surface())
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            new_x += dist;  moved = True
            if self.facing_left:
                self.facing_left = False
                self.display = (self._he'() if self.skill_active
                                else self._make_normal_surface())

        self.x = max(box_left, min(new_x, box_right - self.SPRITE_W))
        self.y = max(box_top,  min(new_y, box_bottom - self.SPRITE_H))

        if key[pygame.K_e] and self.skill_ready and not self.skill_active:
            self.activate_skill()


def draw_hud(screen, cat, width, height, score):
    font = pygame.font.SysFont("consolas", 20, bold=True)
# this doesnt work and i spent last night trying to find out why :pray:
    bar_x, bar_y, bar_w, bar_h = 20, height - 40, 200, 20
    pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
    now = pygame.time.get_ticks()
    if cat.skill_active:
        fill = 1.0
        bar_color = (0, 160, 255)
    else:
        elapsed_since = now - cat.last_skill_time
        fill = min(elapsed_since / cat.skill_cooldown, 1.0)
        bar_color = (0, 200, 100) if fill >= 1.0 else (180, 180, 0)
    pygame.draw.rect(screen, bar_color, (bar_x, bar_y, int(bar_w * fill), bar_h))
    pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 2)

    label = "E - ABILITY" if cat.skill_ready and not cat.skill_active else (
            "ACTIVE" if cat.skill_active else "COOLDOWN")
    screen.blit(font.render(label, True, (230, 230, 230)), (bar_x + 4, bar_y + 2))

    
    screen.blit(font.render(f"SURVIVED: {score}s", True, (230, 230, 230)), (width - 200, 16))



def you_dead(screen, width, height, score):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((180, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    big = pygame.font.SysFont("consolas", 60, bold=True)
    med = pygame.font.SysFont("consolas", 28)
    screen.blit(big.render("YOU DIED", True, (255, 255, 255)),
                (width // 2 - 150, height // 2 - 80))
    screen.blit(med.render(f"Survived {score} seconds", True, (255, 200, 200)),
                (width // 2 - 130, height // 2 + 10))
    screen.blit(med.render("Press R to restart", True, (255, 200, 200)),
                (width // 2 - 120, height // 2 + 50))


def main():
    pygame.init()
    width, height = 960, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("nasty cretin")

    BOX_LEFT, BOX_TOP     = 200, 100
    BOX_RIGHT, BOX_BOTTOM = 800, 600
    BOX_THICKNESS = 4

    def make_cat():
        c = Cat(screen)
        c.x = (BOX_LEFT + BOX_RIGHT) // 2 - Cat.SPRITE_W // 2
        c.y = (BOX_TOP + BOX_BOTTOM) // 2 - Cat.SPRITE_H // 2
        return c

    cat = make_cat()
    clock = pygame.time.Clock()

    lasers = []
    last_laser_spawn = pygame.time.get_ticks()
    laser_interval = 1800   

    SURGE_INTERVAL = 15000   
    SURGE_COUNT    = 10      
    last_surge_time = pygame.time.get_ticks()
    whole_lotta_lasers_until = 0  

    start_time = pygame.time.get_ticks()
    score = 0

    running = True
    while running:
        dt = clock.tick(120)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and cat.dead:
                    cat = make_cat()
                    lasers.clear()
                    last_laser_spawn = now
                    last_surge_time = now
                    whole_lotta_lasers_until = 0
                    start_time = now
                    score = 0

        if not cat.dead:
            cat.handle_keys(BOX_LEFT, BOX_TOP, BOX_RIGHT, BOX_BOTTOM)
            cat.update()

            score = (now - start_time) // 1000

            laser_interval = max(700, 1800 - score * 20)

            if now - last_laser_spawn >= laser_interval:
                lasers.append(Laser(BOX_LEFT, BOX_TOP, BOX_RIGHT, BOX_BOTTOM))
                last_laser_spawn = now

            if now - last_surge_time >= SURGE_INTERVAL:
                surge_count = SURGE_COUNT + (score // 15) * 2  # more lasers the longer you survive
                for _ in range(surge_count):
                    lasers.append(Laser(BOX_LEFT, BOX_TOP, BOX_RIGHT, BOX_BOTTOM))
                last_surge_time = now
                whole_lotta_lasers_until = now + 1500  # show banner for 1.5s

        for laser in lasers:
            laser.update()
        lasers = [l for l in lasers if l.state != "done"]

        if not cat.dead and not cat.skill_active:
            for laser in lasers:
                if laser.hits(cat.x, cat.y):
                    cat.dead = True

        screen.fill((30, 30, 35))

        interior = pygame.Surface((BOX_RIGHT - BOX_LEFT, BOX_BOTTOM - BOX_TOP), pygame.SRCALPHA)
        interior.fill((255, 255, 255, 18))
        screen.blit(interior, (BOX_LEFT, BOX_TOP))

        for laser in lasers:
            laser.draw(screen, 0, 0)

        cat.draw(0, 0)

        box_rect = pygame.Rect(BOX_LEFT, BOX_TOP,
                               BOX_RIGHT - BOX_LEFT, BOX_BOTTOM - BOX_TOP)
        pygame.draw.rect(screen, (220, 220, 220), box_rect, BOX_THICKNESS)

        # no worky :(
        draw_hud(screen, cat, width, height, score)

        if now < whole_lotta_lasers_until:
            big = pygame.font.SysFont("consolas", 52, bold=True)
            elapsed_frac = (now - (whole_lotta_lasers_until - 1500)) / 1500
            alpha = max(0, int(255 * (1 - elapsed_frac ** 2)))
            txt_surf = big.render("christian says dodge", True, (255, 80, 0))
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (width // 2 - txt_surf.get_width() // 2, height // 2 - 30))

        if cat.dead:
            you_dead(screen, width, height, score)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
