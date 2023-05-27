# AI Eye - An AI-Based Trivia Game

AI Eye is an immersive trivia game that challenges players to decipher the secrets hidden within AI-generated images. With each round, players are presented with intriguing images created using stable diffusion, and their task is to guess what the AI-generated image represents. The game incorporates different prompts to dynamically alter the appearance of the image, ensuring a unique and captivating experience for every playthrough.

## Installation

To run AI Eye on your local machine, follow these steps:

1. Create an account on [Replicate](https://replicate.com/).

2. Copy your API Token from your profile settings in Replicate. You can find your API Token at [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens).

3. Download or clone this repository onto your local machine.

4. Inside the downloaded folder, create a new file named ```.env```.

5. Open the ```.env``` file and paste the following code, replacing ```<API_Token>``` with your actual Replicate API Token:

```
REPLICATE_API_KEY=<API_Token>
```

6. Save the `.env` file.

7. Make sure you have the dependencies installed before running the game. Run the below command on the terminal:
```
pip install -r requirements.txt
```

8. Run `main.py` to start the game!

## Demo

Watch a demo of AI Eye in action on YouTube: [https://youtu.be/ap9_HST7CQA](https://youtu.be/ap9_HST7CQA)

## Contributing

We welcome contributions to AI Eye! If you have any ideas, improvements, or bug fixes, feel free to open an issue or submit a pull request on GitHub. Let's collaborate and make AI Eye even better together!

## License

AI Eye is released under the [MIT License](https://opensource.org/licenses/MIT). You can find the details in the [LICENSE](LICENSE) file.

## Acknowledgements

We would like to express our gratitude to the creators of the deep learning models and image processing algorithms used in AI Eye. Their contributions have been instrumental in making this game possible.

## Contact

If you have any questions, suggestions, or feedback, please don't hesitate to contact me at [nandan@ualberta.ca](mailto:nandan@ualberta.ca). I would love to hear from you or have a chat!




