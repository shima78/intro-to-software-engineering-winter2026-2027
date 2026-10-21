import pygame
import random
from game_graphics import draw_vehicle, draw_road, draw_game_over, draw_hud

# Initial parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 750
pygame.font.init()
font = pygame.font.Font(None, 50)

# Colors
WHITE = (255, 255, 255)
BLACK= (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255,165,0)
BLUE = (0,0,255)


# Player class
class player(pygame.sprite.Sprite):
    def __init__(self):
        # Define initial parameters
        self.color = BLUE
        self.width = 50
        self.height= 100
        self.vel = 50
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Draw a car facing upwards
        self.image = draw_vehicle(self.width, self.height, self.color)

        # Fetch the rectangle around the car (used for position and collisions)
        self.rect = self.image.get_rect()

        # Set the initial position
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT - self.height

    # Move the block depending on keyboard input
    def move(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()

        # Move to the left if its not on the leftmost side
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= self.vel

        # Move to the right if its not on the rightmost side
        elif keys[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.vel


#### TODO1: Write a "traffic" class that simulates oncoming traffic 
### Hint: draw_vehicle(width, height, color, kind, facing_down=True) from game_graphics.py gives it a look
###
###
###
###
###
###


#### TODO2: Add two traffic subclasses "car" and "truck" with different proportions and velocities
###
###
###
###
###
###

# Display 'game over' and wait: SPACE/ENTER plays again, ESC or closing the window quits
def game_over(win, crash_point, stats):
    draw_game_over(win, crash_point, stats)
    pygame.display.flip()

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                return True
            if event.key == pygame.K_ESCAPE:
                return False
    


def run():
    # initialize pygame
    pygame.init()

    # Set display
    # Resizable window; SCALED stretches the 600x750 game to the window size
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

    # Set clock
    clock = pygame.time.Clock()

    # Play rounds until the player quits, keeping the best score between rounds
    best_score = 0
    play_again = True
    while play_again:
        play_again, best_score = play(win, clock, best_score)
    pygame.quit()


# Play one round; returns (play again?, best score)
def play(win, clock, best_score):
    # Initialize player and traffic(s)
    player1 = player()
    #TODO: here

    # Create sprite groups
    all_traffic = pygame.sprite.Group()
    #TODO: add traffic(s)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    #TODO: add traffic(s)

    # Stats of this round
    start_time = pygame.time.get_ticks()
    stats = {"score": 0, "time": 0.0, "speed": 0, "best": best_score, "new_best": False}

    # Run the game
    scroll = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, stats["best"]
           
        # Move all objects; traffic that jumps back to the top has been dodged
        old_y = {t: t.rect.y for t in all_traffic}
        for sprite in all_sprites:
            sprite.move()
        stats["score"] += sum(1 for t in all_traffic if t.rect.y < old_y[t])

        # Update the stats
        stats["time"] = (pygame.time.get_ticks() - start_time) / 1000
        stats["speed"] = max([t.vel for t in all_traffic], default=0)
        if stats["score"] > best_score:
            stats["best"] = stats["score"]
            stats["new_best"] = True

        # If player and traffic collides display game over screen
        collision = pygame.sprite.spritecollideany(player1, all_traffic)
        if collision:
            # Show the crash scene first, then the game over panel on top
            draw_road(win, scroll)
            all_sprites.draw(win)
            return game_over(win, player1.rect.clip(collision.rect).center, stats), stats["best"]

        else:
            scroll += 15
            draw_road(win, scroll)
            all_sprites.draw(win)
            draw_hud(win, stats)
            all_sprites.update()

        # display changes
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    run()
