import os
import requests
import httpx
import io
from io import BytesIO
import pygame as pygame

from dotenv import load_dotenv
load_dotenv()
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')

# replicate must be imported after load_dotenv
import replicate

# Example usage
# stable_diffusion_client = StableDiffusionClient()
# stable_diffusion_client.run("A cat holding a gameboy console")
class StableDiffusionClient:
    def __init__(
        self,
        model: str = "stability-ai/stable-diffusion",
        version: str = "27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
        image_dimensions: list = [512, 512],
    ):
        self.model = model
        self.version = version
        self.api_token = REPLICATE_API_KEY
        self.image_dimensions = image_dimensions

    def load_image(
        self,
        urls: list,
    ) -> BytesIO:
        """
        Loads image synchronously

        Example:
            image_bytes = load_image(urls)
            image = pygame.image.load(image_bytes)
        """
        response = requests.get(urls[0])
        image_bytes = io.BytesIO(response.content)
        return image_bytes

    async def aload_image(
        self,
        urls: list,
    ) -> BytesIO:
        """
        Loads image asynchronously

        Example:
            image_bytes = load_image(urls)
            image = pygame.image.load(image_bytes)
        """
        response = httpx.get(urls[0])
        image_bytes = io.BytesIO(response.content)
        return image_bytes

    def run(
        self, 
        prompt: str,
    ) -> BytesIO:
        """
        Runs Stable Diffusion synchronously
        """
        replicate_client = replicate.Client(api_token=self.api_token)
        replicate_model = f"{self.model}:{self.version}"
        urls = replicate_client.run(
            replicate_model,
            input={"prompt": prompt, "image_dimensions": self.image_dimensions},
        )
        image_bytes = self.load_image(urls)
        return image_bytes

    async def arun(
        self, 
        prompt: str,
    ) -> BytesIO:
        """
        Runs Stable Diffusion asynchronously
        """
        replicate_client = replicate.Client(api_token=self.api_token)
        replicate_model = f"{self.model}:{self.version}"
        urls = replicate_client.run(
            replicate_model,
            input={"prompt": prompt, "image_dimensions": self.image_dimensions},
        )
        image_bytes = await self.aload_image(urls)
        return image_bytes

stable_diffusion_client = StableDiffusionClient()


