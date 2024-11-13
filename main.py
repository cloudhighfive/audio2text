import os
import subprocess
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OpenAI API key not found. Make sure OPENAI_API_KEY is set in the .env file.")
    exit(1)

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    exit(1)

input_folder = "audio"
output_folder = "audio_converted"

os.makedirs(output_folder, exist_ok=True)

# Define allowed audio file extensions
audio_extensions = {".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"}

# Loop through all audio files in the input folder
for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in audio_extensions):
        file_base_name = os.path.splitext(filename)[0]
        input_file_path = os.path.join(input_folder, filename)
        ogg_file_path = os.path.join(output_folder, f"{file_base_name}.ogg")
        txt_file_path = os.path.join(output_folder, f"{file_base_name}.txt")

        # Convert the audio file to OGG format using ffmpeg
        ffmpeg_command = [
            "ffmpeg", "-i", input_file_path, "-vn", "-map_metadata", "-1", 
            "-ac", "1", "-c:a", "libopus", "-b:a", "12k", "-application", "voip", ogg_file_path
        ]

        try:
            subprocess.run(ffmpeg_command, check=True)
            logger.info(f"Converted {filename} to {ogg_file_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting {filename} to OGG: {e}")
            continue
        except FileNotFoundError:
            logger.error("ffmpeg not found. Please make sure ffmpeg is installed and available in PATH.")
            continue

        # Open the converted ogg file and transcribe it
        try:
            with open(ogg_file_path, "rb") as f:
                transcript = client.audio.transcriptions.create(file=f, model="whisper-1")
            logger.info(f"Transcription successful for {ogg_file_path}")
        except Exception as e:
            logger.error(f"Error transcribing {ogg_file_path}: {e}")
            continue

        # Save the transcription to a text file
        try:
            with open(txt_file_path, "w") as output_file:
                output_file.write(transcript.text)
            logger.info(f"Transcription saved to {txt_file_path}")
        except Exception as e:
            logger.error(f"Error saving transcription to {txt_file_path}: {e}")
            continue

logger.info("Batch processing complete.")
