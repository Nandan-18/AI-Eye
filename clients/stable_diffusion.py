import os
import requests
import httpx
import io
from io import BytesIO
import pygame as pygame
from replicate.prediction import Prediction

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

    def get_client(
        self,
    ):
        """
        Returns a replicate.Client object
        """
        return replicate.Client(api_token=self.api_token)

    def start_process(
        self, 
        prompt: str,
    ) -> Prediction:
        """
        Runs Stable Diffusion in background.
        Returns a Prediction object, which can be polled for status.
        """
        replicate_client = self.get_client()
        model = replicate_client.models.get(self.model)
        version = model.versions.get(self.version)
        prediction = replicate_client.predictions.create(
            version=version,
            input={"prompt": prompt, "image_dimensions": self.image_dimensions},
        ) 
        return prediction
    
    def poll_prediction(
        self,
        prediction: Prediction,
    ) -> BytesIO:
        """
        Polls a Prediction object for status.
        Returns a BytesIO object, which can be loaded into pygame.
        """
        while prediction.status != "succeeded":
            # https://www.pygame.org/docs/ref/event.html#pygame.event.wait
            # Must call pygame.event.wait() to prevent pygame from freezing
            pygame.event.wait()
            # Here we wait 0.5sec then poll the prediction for status
            prediction.wait()
        urls = prediction.output
        image_bytes = self.load_image(urls)
        return image_bytes

    def run(
        self, 
        prompt: str,
    ) -> BytesIO:
        prediction = self.start_process(prompt)
        image_bytes = self.poll_prediction(prediction)
        return image_bytes

    # Not used
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

    # Not used
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


