import json
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent

class FileUtils:
    @classmethod
    def read_json(cls, path: str):
        with open(path) as f:
            data = json.load(f)
        return data

    @classmethod
    def get_random_word(
        cls,
        path: str = str(ROOT / "assets" / "words.json"),
        category: str = "physical_objects",
    ) -> str:
        file_dict = cls.read_json(path)
        return random.choice(file_dict[category])
