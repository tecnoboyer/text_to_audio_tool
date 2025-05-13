import openai
import os
import requests
from pathlib import Path

# Configuration
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
INPUT_FILE = 'wowWords.txt'  # Name of your input text file
OUTPUT_FILE = 'children_story.mp3'

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the text-to-speech API endpoint
TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"

# Create directories if they don't exist
Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def generate_story_audio():
    # Read the story text from input file
    input_path = os.path.join(INPUT_DIR, INPUT_FILE)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            story_text = file.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        print(f"Please create the '{INPUT_DIR}' directory and add a '{INPUT_FILE}' file with your story.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Define the headers for the API request
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    # Define the payload for the API request
    # Using a more child-friendly voice and ensuring proper formatting
    payload = {
        "model": "tts-1",
        "input": story_text,
        "voice": "nova",  # 'nova' is warm and expressive, good for children's stories
        "response_format": "mp3",
        "speed": 0.9  # Slightly slower for better comprehension by children
    }

    # Make the API request
    response = requests.post(TTS_ENDPOINT, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the audio in the output directory
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        with open(output_path, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"Children's story audio successfully saved to {output_path}")
    else:
        print(f"Failed to generate audio. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    generate_story_audio()