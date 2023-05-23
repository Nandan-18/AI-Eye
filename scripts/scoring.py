import pygame as pg


class Score:
    def __init__(self, round):
        self.score = 1000
        self.round = round
        self.score_font = pg.font.Font('./font/Cascadia.ttf', 32)
        self.coin_img = pg.image.load("assets/coin.png")
        self.coin_img = pg.transform.scale(self.coin_img, (50,50))


    def game_update(self, correct):
        if correct == 0:
            self.score += 100  # Correct answer
        elif correct == 1:
            self.score -= 150  # Wrong answer
        elif correct == 2:
            self.score -= 200  # Time runs out

    def draw(self, screen):

        score_text = self.score_font.render(
            f"{self.score}", True, (255, 255, 255))

        screen.blit(self.coin_img, (10,10))
        screen.blit(score_text, (self.coin_img.get_width() + 20,  self.coin_img.get_height()//2-10))

# # Initialize Pygame
# pygame.init()

# # Create a screen surface
# screen = pygame.display.set_mode((800, 600))

# # Create an instance of the Score class
# score = Score(1)

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Example usage:
#     score.round_update(0)  # Update the score for a correct answer

#     # Draw the score on the screen
#     score.draw(screen)

#     pygame.display.update()

# # Quit Pygame
# pygame.quit()
