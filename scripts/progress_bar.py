import pygame
import sys
import threading


class LoadingBar:
    def __init__(self, screen_width, screen_height, work_duration, loading_bar_image, loading_bg_image, font_name, font_size):
        pygame.init()

        # Screen and font
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Loading Bar!")

        self.FONT = pygame.font.SysFont(font_name, font_size)

        # Clock
        self.CLOCK = pygame.time.Clock()

        # Work
        self.WORK_DURATION = work_duration

        # Loading BG
        self.LOADING_BG = pygame.image.load(loading_bg_image)
        self.LOADING_BG_RECT = self.LOADING_BG.get_rect(
            center=(screen_width // 2, screen_height // 2))

        # Loading Bar and variables
        self.loading_bar = pygame.image.load(loading_bar_image)
        self.loading_bar_rect = self.loading_bar.get_rect(
            midleft=(screen_width // 2 - 200, screen_height // 2))
        self.loading_finished = False
        self.loading_progress = 0
        self.loading_bar_width = 8

        # Countdown variables
        self.countdown_time = self.WORK_DURATION
        self.start_time = pygame.time.get_ticks()

        # Start the work thread
        threading.Thread(target=self.doWork).start()

    def doWork(self):
        # Do work based on time
        start_ticks = pygame.time.get_ticks()
        while True:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
            if elapsed_time >= self.WORK_DURATION:
                break

            self.loading_progress = int(
                (elapsed_time / self.WORK_DURATION) * 100)

        self.loading_finished = True

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill("#0d0e2e")

        if not self.loading_finished:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            remaining_time = max(self.countdown_time - elapsed_time, 0)
            self.loading_bar_width = self.loading_progress / 100 * 400

            loading_bar_scaled = pygame.transform.scale(
                self.loading_bar, (int(self.loading_bar_width), 50))
            loading_bar_rect = loading_bar_scaled.get_rect(
                midleft=(self.screen.get_width() // 2 - 200, self.screen.get_height() // 2))

            self.screen.blit(self.LOADING_BG, self.LOADING_BG_RECT)
            self.screen.blit(loading_bar_scaled, loading_bar_rect)

            # Display countdown text
            countdown_text = self.FONT.render(
                str(round(remaining_time, 1)), True, "white")
            countdown_rect = countdown_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
            self.screen.blit(countdown_text, countdown_rect)
        else:
            self.screen.blit(self.finished_text, self.finished_text_rect)

        pygame.display.update()
        self.CLOCK.tick(60)

    def run(self):
        while True:
            self.update()


if __name__ == "__main__":
    loading_bar = LoadingBar(1280, 720, 20, "../assets/Loading Bar.png",
                             "../assets/Loading Bar Background.png", "Roboto", 100)
    loading_bar.run()
