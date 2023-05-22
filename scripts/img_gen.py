from clients.stable_diffusion import StableDiffusionClient
from clients.utils import FileUtils
import pygame as pg
import threading
from loguru import logger


class ImageGenerator:
    def __init__(self, image_dimensions: list = [512, 512]) -> None:
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

    def round_img_gen(self, round):
        lengths = [3, 4, 5, 6, 7]
        self.round_images = []
        self.prompts = []
        if round == 1:
            self.preprompt = "simple, recognizable, clear voxel art of "
        elif round == 2:
            self.preprompt = "isometric, slighly blurred, voxel art of "
        elif round == 3:
            self.preprompt = "complex, unrecognizable voxel art of "

        for length in lengths:
            random_word = FileUtils.get_random_word(
                str(length))  # Get a random word from the list
            prompt = self.preprompt + random_word
            self.prompts.append(random_word)
            self.round_images.append(self.generate_image(prompt))
        
        self.game_num = 0
        return self.prompts[self.game_num]

    def next_image(self):
        self.game_num = (self.game_num +1) % len(self.prompts)
        return self.prompts[self.game_num]
    
    def get_cur_prompt(self):
        return self.prompts[self.game_num]

    def update(self, events, user_input):
        """
        user_input = self.text_input.get_cur_word()
        """

        pass

    def generate_image(self, prompt):
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

        return self.image

    def draw(self, win: pg.Surface):
        if self.visible:
            pos = (
                win.get_width()/2 - self.image.get_width()//2,
                win.get_height()/3 - self.image.get_height()//2,
            )
            win.blit(pg.transform.scale(self.round_images[self.game_num], self.image_dimensions), pos)
             # Create a border around the image if image has been generated.
            if self.has_generated_image == True:
                # Isla, change the two variables below to change the border around the image
                border_color = (0,0,79)
                border_thickness = 30

                pg.draw.rect(
                    win, border_color, (*pos, *self.image_dimensions), border_thickness, border_radius= 30
                )
