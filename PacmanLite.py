import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Lite - Slower Smart Ghost & Win Message")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
ROYALBLUE = (65, 105, 225)
SALMON = (250, 128, 114)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Game variables
score = 0
lives = 3
power_timer = 0

# Pacman
pacman = pygame.Rect(100, 200, 20, 20)
pacman_dx, pacman_dy = 2, 0
mouth_open = True
mouth_timer = 0

# Dots
dots = [pygame.Rect(x, y, 8, 8) for x in range(20, 400, 60) for y in [63, 343]]

# Power dot
power_dot = pygame.Rect(270, 343, 15, 15)
power_dot_visible = True

# Ghosts with different movement styles
ghosts = [
    {"rect": pygame.Rect(350, 200, 25, 25), "dx": -2, "dy": 0, "color": MAGENTA, "type": "horizontal"},
    {"rect": pygame.Rect(50, 150, 25, 25), "dx": 0, "dy": 2, "color": CYAN, "type": "vertical"},
    {"rect": pygame.Rect(200, 100, 25, 25), "dx": 1, "dy": 1, "color": ORANGE, "type": "smart"}
]

# Maze walls
walls = [
    pygame.Rect(0, 0, WIDTH, 10), pygame.Rect(0, HEIGHT-10, WIDTH, 10),
    pygame.Rect(0, 0, 10, HEIGHT), pygame.Rect(WIDTH-10, 0, 10, HEIGHT)
]

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, ROYALBLUE, wall)

running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -2
    if keys[pygame.K_RIGHT]:
        dx = 2
    if keys[pygame.K_UP]:
        dy = -2
    if keys[pygame.K_DOWN]:
        dy = 2

    # Check collisions with walls before moving
    next_pacman = pacman.move(dx, dy)
    if not any(next_pacman.colliderect(w) for w in walls):
        pacman = next_pacman

    # Pacman mouth animation
    mouth_timer += 1
    if mouth_timer % 10 == 0:
        mouth_open = not mouth_open

    # Move ghosts
    for ghost in ghosts:
        if ghost["type"] == "horizontal":
            ghost["rect"].x += ghost["dx"]
            if ghost["rect"].left <= 10 or ghost["rect"].right >= WIDTH-10:
                ghost["dx"] *= -1

        elif ghost["type"] == "vertical":
            ghost["rect"].y += ghost["dy"]
            if ghost["rect"].top <= 10 or ghost["rect"].bottom >= HEIGHT-10:
                ghost["dy"] *= -1

        elif ghost["type"] == "smart":
            # Slower smart AI: 50% chance to chase Pacman
            if random.random() < 0.5:
                ghost["dx"] = 1 if pacman.centerx > ghost["rect"].centerx else -1
                ghost["dy"] = 1 if pacman.centery > ghost["rect"].centery else -1
            else:  # random movement
                if random.randint(0, 10) == 0:
                    ghost["dx"] = random.choice([-1, 1])
                    ghost["dy"] = random.choice([-1, 1])

            ghost["rect"].x += ghost["dx"]
            ghost["rect"].y += ghost["dy"]

            # Bounce off walls
            if ghost["rect"].left <= 10 or ghost["rect"].right >= WIDTH-10:
                ghost["dx"] *= -1
            if ghost["rect"].top <= 10 or ghost["rect"].bottom >= HEIGHT-10:
                ghost["dy"] *= -1

        # Ghost collision with Pacman
        if pacman.colliderect(ghost["rect"]):
            if ghost["color"] == ROYALBLUE:
                ghost["rect"].width = 0
                ghost["rect"].height = 0
            else:
                lives -= 1
                pacman.x, pacman.y = 100, 200
                if lives <= 0:
                    screen.fill(BLACK)
                    draw_text("GAME OVER!", 120, 180, color=WHITE)
                    draw_text(f"Final Score: {score}", 110, 220, color=WHITE)
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    running = False

    # Dot collision
    for dot in dots[:]:
        if pacman.colliderect(dot):
            dots.remove(dot)
            score += 10

    # Power dot collision
    if power_dot_visible and pacman.colliderect(power_dot):
        for ghost in ghosts:
            ghost["color"] = ROYALBLUE
        power_dot_visible = False
        power_timer = 300  # ghost blue duration

    # Power timer countdown
    if power_timer > 0:
        power_timer -= 1
    elif power_timer == 0:
        ghosts[0]["color"] = MAGENTA
        ghosts[1]["color"] = CYAN
        ghosts[2]["color"] = ORANGE

    # Draw walls
    draw_walls()

    # Draw pacman
    pygame.draw.circle(screen, YELLOW, pacman.center, 10)

    # Draw ghosts
    for ghost in ghosts:
        if ghost["rect"].width > 0:
            pygame.draw.rect(screen, ghost["color"], ghost["rect"])

    # Draw dots
    for dot in dots:
        pygame.draw.circle(screen, SALMON, dot.center, 4)

    # Draw power dot
    if power_dot_visible:
        pygame.draw.circle(screen, SALMON, power_dot.center, 8)

    # Draw score and lives
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", 300, 10)

    # Win condition
    if not dots:
        screen.fill(BLACK)
        draw_text("YOU WIN!", 130, 180, color=YELLOW)
        draw_text(f"Final Score: {score}", 110, 220, color=WHITE)
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()