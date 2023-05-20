import os
from dotenv import load_dotenv
load_dotenv()
REPLICATE_API_KEY = os.getenv('REPLICATE_API_KEY')

# replicate must be imported after load_dotenv
import replicate
from replicate import Client

class StableDiffusionClient:
    # Example usage
    # client = StableDiffusionClient()
    # stable_diffusion_client.run("A cat holding a gameboy console")

    def __init__(
        self,
        model: str = "stability-ai/stable-diffusion",
        version: str = "27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
    ):
        self.model = model
        self.version = version
        self.api_token = REPLICATE_API_KEY

    async def run(
        self, 
        prompt: str,
    ):
        replicate_client = replicate.Client(api_token=self.api_token)
        replicate_model = f"{self.model}:{self.version}"
        output = replicate_client.run(
            replicate_model,
            input={"prompt": prompt},
        )
        return output


