import pygame
import random
import os

# ---------- GAME CONSTANTS ----------
WIDTH, HEIGHT = 800, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_Y = 250
GRAVITY = 1.2

# ---------- LOAD IMAGES ----------
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
TREX_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "girl.png"))
OBSTACLE_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH, "RedFlag.png"))

TREX_IMAGE = pygame.transform.scale(TREX_IMAGE, (40, 40))
OBSTACLE_IMAGE = pygame.transform.scale(OBSTACLE_IMAGE, (20, 40))

# ---------- T-REX CHARACTER ----------
class TRex:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = 100
        self.y = GROUND_Y - self.height
        self.jump_velocity = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.jump_velocity = -18
            self.jumping = True

    def update(self):
        self.y += self.jump_velocity
        self.jump_velocity += GRAVITY

        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.jumping = False

    def draw(self, screen):
        screen.blit(TREX_IMAGE, (self.x, self.y))

# ---------- OBSTACLES ----------
class Obstacle:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.x = WIDTH
        self.y = GROUND_Y - self.height
        self.speed = 9

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(OBSTACLE_IMAGE, (self.x, self.y))

    def off_screen(self):
        return self.x + self.width < 0

    def collide(self, trex):
        return (
            self.x < trex.x + trex.width and
            self.x + self.width > trex.x and
            self.y < trex.y + trex.height and
            self.y + self.height > trex.y
        )

# ---------- MAIN GAME CLASS ----------
class TRexGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PosePlay | T-Rex Game")
        self.clock = pygame.time.Clock()
        self.trex = TRex()
        self.obstacles = []
        self.score = 0
        self.font = pygame.font.SysFont(None, 30)
        self.is_game_over = False

        # 🎵 Load music
        self.gameplay_music = os.path.join(ASSETS_PATH, "gameplay.mp3")
        self.gameover_sound = os.path.join(ASSETS_PATH, "gameover.mp3")

        pygame.mixer.music.load(self.gameplay_music)
        pygame.mixer.music.play(-1)  # loop forever

    def jump(self):
        self.trex.jump()

    def update(self):
        self.clock.tick(60)
        self.screen.fill(WHITE)

        self.trex.update()
        self.trex.draw(self.screen)

        if len(self.obstacles) == 0 or self.obstacles[-1].x < WIDTH - 300:
            self.obstacles.append(Obstacle())

        for obstacle in self.obstacles[:]:
            obstacle.update()
            obstacle.draw(self.screen)
            if obstacle.off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1
            elif obstacle.collide(self.trex) and not self.is_game_over:
                self.game_over()

        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        pygame.display.update()

    def game_over(self):
        if not self.is_game_over:
            self.is_game_over = True
            pygame.mixer.music.stop()

            gameover = pygame.mixer.Sound(self.gameover_sound)
            gameover.play()

            # 🔲 Centered Game Over card
            card_width, card_height = 400, 120
            card_x = WIDTH // 2 - card_width // 2
            card_y = HEIGHT // 2 - card_height // 2

            # Shadow
            shadow = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 150), shadow.get_rect(), border_radius=10)
            self.screen.blit(shadow, (card_x + 5, card_y + 5))

            # Card
            pygame.draw.rect(self.screen, (255, 255, 255), (card_x, card_y, card_width, card_height), border_radius=10)

            title = self.font.render("GAME OVER", True, (255, 0, 0))
            subtitle = self.font.render("Press 'R' to Restart", True, BLACK)

            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, card_y + 30))
            self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, card_y + 65))

            pygame.display.update()

    def show_start_screen(self):
        self.screen.fill(WHITE)
        title = self.font.render("PosePlay | T-Rex Game", True, BLACK)
        instructions = self.font.render("Make a Fist or Press Space to Start", True, BLACK)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2))

        pygame.display.update()
