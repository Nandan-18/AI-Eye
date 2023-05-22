import pygame as pg


class ProgressBar:
    def __init__(self, width, height, countdown_time):
        self.width = width
        self.height = height
        self.countdown_time = countdown_time
        self.remaining_time = countdown_time
        pg.font.init()
        self.font = pg.font.Font('./font/Cascadia.ttf', 24)
        self.is_complete = False

    def update(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_complete = True

    def draw(self, surface, x, y):
        pg.draw.rect(surface, (13, 14, 46),
                        (x, y, self.width, self.height), border_radius=10)

        progress_width = int(
            (1 - self.remaining_time / self.countdown_time) * (self.width - 4))

        progress_rect = pg.Rect(
            x + 2, y + 2, progress_width, self.height - 4)

        pg.draw.rect(surface, (235, 69, 95),
                        progress_rect, border_radius=10)

        text = self.font.render(
            str(round(int(self.remaining_time/6)*0.1, 2)), True, (235, 235, 235))
        text_rect = text.get_rect(
            center=(x + self.width // 2, y + self.height // 2))

        surface.blit(text, text_rect)



#     def run(self):
#         pg.init()
#         clock = pg.time.Clock()

#         window_width = 400
#         window_height = 200
#         window = pg.display.set_mode((window_width, window_height))

#         while not self.is_complete:
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     pg.quit()
#                     sys.exit()

#             self.update()
#             self.draw()

#             window.fill((13, 14, 46))
#             # Blit the progress bar surface onto the main window
#             window.blit(self.surface, (window_width // 2 - self.width // 2, window_height // 2 - self.height // 2))
#             pg.display.flip()
#             clock.tick(1)


# # Example usage
# # Initialize progress bar with width: 200, height: 30, countdown_time: 20 seconds
# progress_bar = ProgressBar(200, 30, 10)
# progress_bar.run()  # Run the progress bar
