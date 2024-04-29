# Snake Game in Python

A classic snake game implemented in Python using the Pygame library.

## Installation

### Prerequisites

- Python
- Pygame

To install Pygame, use the command `pip install pygame`.

### Running Locally

To run the game, navigate to the directory containing `main.py` and execute the script using Python.

### Running in a Web Browser with pygbag

You can also run the game in a web browser. Convert the game to WebAssembly by using pygbag. First, install pygbag via pip, then navigate to your game directory and run the conversion command provided by pygbag.

## Deploying on Cloud (AWS)

Deploy this game on AWS by following these steps:

1. Convert the game to WebAssembly using pygbag.
2. Navigate to the `build` folder.
3. Upload the contents to an AWS S3 bucket.
4. Enable Static Website Hosting on S3.
5. Set the bucket policy to allow public read access.
6. Use the provided Endpoint URL to access the game.

Make sure all files are public on your S3 bucket to allow for game access.

## Author

Sanket Kulkarni

Feel free to fork, star, and contribute to this repository.
