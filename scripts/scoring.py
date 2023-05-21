import pygame


class Score:
    def __init__(self, round):
        self.score = 1000
        self.round = round
        self.round_score = 0
        self.hint = False
        self.score_font = pygame.font.Font('./font/Cascadia.ttf', 32)

    def hint_update(self):
        if self.hint:
            self.score -= 500
            self.hint = False

    def round_update(self, correct):
        if correct == 0:
            self.round_score += 100  # Correct answer
        elif correct == 1:
            self.round_score -= 150  # Wrong answer
        elif correct == 2:
            self.round_score -= 200  # Time runs out

    def draw(self, screen):
        score_text = self.score_font.render(
            f"Score: {self.score}", True, (255, 255, 255))
        round_text = self.score_font.render(
            f"Round: {self.round}", True, (255, 255, 255))
        round_score_text = self.score_font.render(
            f"Round Score: {self.round_score}", True, (255, 255, 255))
        hint_text = self.score_font.render(
            "Hint", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(round_text, (10, 50))
        # screen.blit(round_score_text, (10, 90))

        hint_button = pygame.Rect(10, 130, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), hint_button)
        screen.blit(hint_text, (20, 140))

        mouse_pos = pygame.mouse.get_pos()
        if hint_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 200, 0), hint_button, 3)
            if pygame.mouse.get_pressed()[0]:
                self.hint = True
                self.hint_update()


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
