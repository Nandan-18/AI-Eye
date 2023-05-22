import pygame as pg


class LoadingBar:
    def __init__(self, screen, work_duration):
        self.screen = screen
        self.CLOCK = pg.time.Clock()
        self.WORK_DURATION = work_duration
        self.font = pg.font.Font('./font/Cascadia.ttf', 32)

        # Background

        self.LOADING_BG = pg.image.load('./assets/load_bg.png')

        self.LOADING_BG_RECT = self.LOADING_BG.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Loading Bar and variables

        self.loading_bar = pg.image.load('./assets/load_bar.png')
        self.loading_bar_rect = self.loading_bar.get_rect(
            midleft=(self.screen.get_width() // 2 - 200, self.screen.get_height() // 2))

        self.loading_finished = False
        self.loading_progress = 0
        self.loading_bar_width = 8

        # Countdown
        self.countdown_time = self.WORK_DURATION
        self.start_time = pg.time.get_ticks()

    def work(self):
        # Do work based on time
        start_ticks = pg.time.get_ticks()
        while True:
            elapsed_time = (pg.time.get_ticks() - start_ticks) / 1000
            if elapsed_time >= self.WORK_DURATION:
                break

            self.loading_progress = int(
                (elapsed_time / self.WORK_DURATION) * 100)

        self.loading_finished = True

    def update(self):

        # self.work()
        # self.screen.fill("#0d0e2e")

        if not self.loading_finished:
            elapsed_time = (pg.time.get_ticks() - self.start_time) / 1000
            remaining_time = max(self.countdown_time - elapsed_time, 0)
            self.loading_bar_width = self.loading_progress / 100 * 400

            loading_bar_scaled = pg.transform.scale(
                self.loading_bar, (int(self.loading_bar_width), 50))
            loading_bar_rect = loading_bar_scaled.get_rect(
                midleft=(self.screen.get_width() // 2 - 200, self.screen.get_height() // 2))

            self.screen.blit(self.LOADING_BG, self.LOADING_BG_RECT)
            self.screen.blit(loading_bar_scaled, loading_bar_rect)

            # Display countdown text
            countdown_text = self.font.render(
                str(round(remaining_time, 1)), True, "white")
            countdown_rect = countdown_text.get_rect(
                center=(self.screen.get_width() // 2 + 10, self.screen.get_height() // 2 + 100))
            self.screen.blit(countdown_text, countdown_rect)

        pg.display.update()
        self.CLOCK.tick(60)

    def draw(self):
        while True:
            self.update()
