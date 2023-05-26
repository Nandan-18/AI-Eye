import os
import requests
import httpx
import io
from io import BytesIO
import pygame as pygame
from replicate.prediction import Prediction
import threading

from dotenv import load_dotenv
load_dotenv()
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')
# replicate must be imported after load_dotenv
import replicate

class StableDiffusionClient:
    def __init__(
        self,
        model: str = "stability-ai/stable-diffusion",
        version: str = "27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
        image_dimensions: list = [128, 128],
    ):
        self.model = model
        self.version = version
        self.api_token = REPLICATE_API_KEY
        self.image_dimensions = image_dimensions
        self.session = requests.Session()

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
        response = self.session.get(urls[0])
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
            input={"prompt": prompt, "image_dimensions": self.image_dimensions, "num_inference_steps": 10, "guidance_scale" : 3},
        ) 
        return prediction
    
    def poll_prediction(self, prediction: Prediction, prompt : str) -> BytesIO:
        event = threading.Event()

        def poll(prediction):
            while prediction.status != "succeeded":
                prediction.wait()
                if prediction.status == "Failed" or prediction.status == "failed":
                    print(f"Failed: {prompt}")
                    prediction = self.start_process(prompt)
            event.set()

        threading.Thread(target=poll, daemon=True, args=(prediction,)).start()
        # poll(prediction)

        event.wait()  # Wait for the prediction to finish

        urls = prediction.output
        image_bytes = self.load_image(urls)
        return image_bytes

    def run(
        self, 
        prompt: str,
    ) -> BytesIO:
        prediction = self.start_process(prompt)
        image_bytes = self.poll_prediction(prediction, prompt)
        return image_bytes

stable_diffusion_client = StableDiffusionClient()


