# main.py
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# ========== Constants ==========
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Snake Game"

# ========== Setup ==========
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# ========== Snake Class ==========
class Snake:
    def __init__(self):
        self.block_size = 20
        self.body = [
            [100, 100],
            [80, 100],
            [60, 100]
        ]
        self.direction = 'RIGHT'
        self.color = (0, 255, 0)

    def move(self, grow=False):
        head_x, head_y = self.body[0]

        if self.direction == 'UP':
            head_y -= self.block_size
        elif self.direction == 'DOWN':
            head_y += self.block_size
        elif self.direction == 'LEFT':
            head_x -= self.block_size
        elif self.direction == 'RIGHT':
            head_x += self.block_size

        new_head = [head_x, head_y]
        self.body.insert(0, new_head)

        if not grow:
            self.body.pop()  # remove tail unless eating

    def change_direction(self, new_dir):
        # Prevent direct reversal
        opposite = {
            'UP': 'DOWN', 'DOWN': 'UP',
            'LEFT': 'RIGHT', 'RIGHT': 'LEFT'
        }
        if new_dir != opposite[self.direction]:
            self.direction = new_dir

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(
                surface, self.color,
                pygame.Rect(segment[0], segment[1], self.block_size, self.block_size)
            )

    def check_collisions(self, screen_width, screen_height):
        head = self.body[0]

        # Wall collision
        if (
            head[0] < 0 or head[0] >= screen_width or
            head[1] < 0 or head[1] >= screen_height
        ):
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        return False

# ========== Food Class ==========
class Food:
    def __init__(self, screen_width, screen_height, block_size):
        self.block_size = block_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (255, 0, 0)
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, (self.screen_width - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.screen_height - self.block_size) // self.block_size) * self.block_size
        return [x, y]

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(self.position[0], self.position[1], self.block_size, self.block_size)
        )

    def respawn(self):
        self.position = self.generate_position()

def show_game_over(screen, font, score):
    game_over_text = font.render("Game Over! Press R to Restart or Q to Quit", True, (255, 255, 255))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 0))

    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
    pygame.display.flip()

# ========== Game Loop ==========
def main():
    snake = Snake()
    food = Food(WINDOW_WIDTH, WINDOW_HEIGHT, snake.block_size)
    font = pygame.font.SysFont('arial', 24)
    
    base_fps = 10
    speed_increment = 2
    speed_level = 0

    score = 0
    running = True
    game_over = False
    last_speedup_score = 0  # Track last score when speed was increased

    while running:
        # Dynamic FPS based on score
        current_fps = base_fps + speed_level * speed_increment
        clock.tick(current_fps)

        # ========== Event Handling ==========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction('RIGHT')
                else:
                    if event.key == pygame.K_r:
                        return main()  # Restart the game
                    elif event.key == pygame.K_q:
                        running = False

        if not game_over:
            # ========== Game Logic ==========
            grow = (snake.body[0] == food.position)

            if grow:
                food.respawn()
                score += 1

            # Increase speed every 5 points, but only once per threshold
            if score % 5 == 0 and score != 0 and score != last_speedup_score:
                speed_level += 1
                last_speedup_score = score

            snake.move(grow)

            if snake.check_collisions(WINDOW_WIDTH, WINDOW_HEIGHT):
                game_over = True

        # ========== Rendering ==========
        screen.fill((0, 0, 0))

        if not game_over:
            snake.draw(screen)
            food.draw(screen)

            # Draw score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            speed_text = font.render(f"Speed: {current_fps} FPS", True, (255, 255, 255))
            screen.blit(speed_text, (10, 40))
        else:
            show_game_over(screen, font, score)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()