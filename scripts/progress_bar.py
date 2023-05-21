import pygame
import threading


class LoadingBar:
    def __init__(self, screen, work_duration):
        self.screen = screen
        self.WORK_DURATION = work_duration

        # Loading Bar and variables
        self.loading_bar = pygame.Surface((8, 150))
        self.loading_bar.fill((255, 255, 255))
        self.loading_bar_rect = self.loading_bar.get_rect(midleft=(280, 360))
        self.loading_finished = False
        self.loading_progress = 0

        # Start the work thread
        threading.Thread(target=self.doWork).start()

    def doWork(self):
        for i in range(self.WORK_DURATION):
            # Do some work here
            self.loading_progress = i + 1

        self.loading_finished = True

    def update(self):
        if not self.loading_finished:
            loading_bar_width = (self.loading_progress /
                                 self.WORK_DURATION) * 720
            self.loading_bar = pygame.Surface((loading_bar_width, 150))
            self.loading_bar.fill((255, 255, 255))
            self.loading_bar_rect = self.loading_bar.get_rect(
                midleft=(280, 360))

            self.screen.blit(self.loading_bar, self.loading_bar_rect)
        else:
            pass  # Add code for handling loading finished state

    def run(self):
        while True:
            self.update()
            pygame.display.update()

    def draw(self):
        self.update()
