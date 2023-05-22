from clients.stable_diffusion import StableDiffusionClient
from clients.utils import FileUtils
import pygame as pg
import logging

class ImageGen:
    def __init__(self, size: tuple = (512,512)) -> None:
        self.client = StableDiffusionClient(image_dimensions=size)
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        # Change this to change the style of art generated.
        self.preprompt = "Isometic voxel art of "
        self.has_generated_image = False
        self.size = size
        self.word = FileUtils.get_random_word()

    
    def update(self, events, user_input):
        if self.has_generated_image == False:
                prompt = self.preprompt + self.word

                logging.info("Generating image...")
                image_bytes = self.client.run(
                    prompt=prompt,
                )

                # Pygame needs a name for the image file even if it's
                # not going to be saved, so we just use a placeholder.
                self.image = pg.image.load(
                    image_bytes, "assets/placeholder.svg"
                )
                logging.info("Image generated!")
                self.has_generated_image = True
        else:
            if user_input == self.word:

                # Add points to score
                # Add success dialogue here

                self.word = FileUtils.get_random_word()
                prompt = self.preprompt + self.word
                image_bytes = self.client.run(
                    prompt=prompt,
                )
                self.image = pg.image.load(
                    image_bytes, "assets/placeholder.svg"
                )

    def draw(self, win : pg.Surface):
        pos = (win.get_width()/2 - self.image.get_width()//2, win.get_height()/3 - self.image.get_height()//2)
        win.blit(pg.transform.scale(self.image,self.size), pos)