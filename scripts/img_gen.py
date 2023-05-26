from clients.stable_diffusion import StableDiffusionClient
from clients.utils import FileUtils
import pygame as pg
import threading
from loguru import logger


class ImageGenerator:
    def __init__(self, image_dimensions: list = [512, 512], active : bool = False) -> None:
        self.client = StableDiffusionClient(image_dimensions=image_dimensions)
        self.image = pg.Surface(tuple(image_dimensions), pg.SRCALPHA)
        # self.image.convert_alpha()
        # self.image.fill((0, 0, 0, 0))
        # Change this to change the style of art generated.
        self.preprompt = None
        self.has_generated_image = False
        self.image_dimensions = image_dimensions
        self.image_gen_thread = None
        self.game_num = 0
        self.round_images = []
        self.prompts = []
        self.visible = False
        self.active = active

    def gen_prompt(self, length, round):
        if round == 1:
            self.preprompt = "cartoon image of "
        elif round == 2:
            self.preprompt = "cyberpunk "
        elif round == 3:
            self.preprompt = "voxel "
        random_word = FileUtils.get_random_word(str(length))  # Get a random word from the list
        self.prompt = self.preprompt + random_word
        return random_word, self.prompt

    def round_img_gen(self, round):
        if self.active:
            lengths = [3, 4, 5, 6, 7]
            self.prompts = []


            self.round_images = [ None for i in range(5)]

            for i, length in enumerate(lengths):
                word, prompt = self.gen_prompt(length, round)
                self.round_images[i] = threading.Thread(target=self.generate_image, args=(prompt,i,)) 
                self.prompts.append(word)
                self.round_images[i].start()

            for thread in self.round_images:
                if not isinstance(thread, pg.Surface):
                    thread.join()
            
            self.game_num = 0
            return self.prompts[self.game_num]
    
    # def skip_game(self, round):
    #     if round == 5:
    #         self.

    def next_image(self):
        if self.active:
            self.game_num = (self.game_num +1) % len(self.prompts)
            return self.prompts[self.game_num]
        else:
            return "pizza"


    def get_cur_prompt(self):
        if self.active:
            return self.prompts[self.game_num]
        else:
            return "pizza"

    def update(self, events, user_input):
        """
        user_input = self.text_input.get_cur_word()
        """

        pass

    def generate_image(self, prompt, i):
        logger.info(f"UPDATE: starting processing for {prompt.split(' ')[-1]}!")
        image_bytes = self.client.run(
            prompt=prompt,
        )
        # Pygame needs a name for the image file even if it's
        # not going to be saved, so we just use a placeholder.
        self.image = pg.image.load(
            image_bytes, "assets/placeholder.svg"
        )
        logger.info(f"Image generated for {prompt}!")
        self.has_generated_image = True

        self.round_images[i] = self.image

    def draw(self, win: pg.Surface):
        if self.visible and self.active:
            pos = (
                win.get_width()/2 - self.image.get_width()//2,
                win.get_height()/3 - self.image.get_height()//2,
            )
            # print(self.round_images[self.game_num].get_size())
            if isinstance(self.round_images[self.game_num], pg.Surface):
                win.blit(pg.transform.scale(self.round_images[self.game_num], self.image_dimensions), pos)
             # Create a border around the image if image has been generated.
            if self.has_generated_image == True:
                # Isla, change the two variables below to change the border around the image
                border_color = (0,0,79)
                border_thickness = 30

                pg.draw.rect(
                    win, border_color, (*pos, *self.image_dimensions), border_thickness, border_radius= 30
                )
